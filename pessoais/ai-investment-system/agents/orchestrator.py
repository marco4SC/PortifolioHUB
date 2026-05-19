"""
Orquestrador — Chief Investment Officer IA.
Agrega sinais de todos os agentes e toma a decisão final.
"""
import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List
import anthropic

from agents.base import AgentSignal
from agents.technical import TechnicalAgent
from agents.fundamental import FundamentalAgent
from agents.sentiment import SentimentAgent
from agents.macro import MacroAgent
from config import config

SYSTEM_PROMPT = """Você é o Chief Investment Officer (CIO) de um fundo quantitativo-fundamentalista.
Receberá os sinais de 4 analistas e deve tomar a DECISÃO FINAL.

Pesos padrão: técnico=25%, fundamentalista=35%, sentimento=20%, macro=20%

Processo:
1. Analise concordâncias e discordâncias
2. Reduza peso de analistas com confiança < 0.5
3. Nunca compre com confiança consolidada < 0.6
4. Gere tese clara com preço-alvo e stop-loss

Retorne APENAS JSON:
{
  "final_signal": "BUY|SELL|HOLD|AVOID",
  "consolidated_confidence": 0.0,
  "position_size_pct": 0.0,
  "price_target": 0.0,
  "stop_loss": 0.0,
  "time_horizon": "short|medium|long",
  "investment_thesis": "tese detalhada",
  "key_risks": ["risco1"],
  "catalysts": ["catalisador1"],
  "consensus_score": 0.0
}"""

@dataclass
class InvestmentDecision:
    asset: str
    final_signal: str
    consolidated_confidence: float
    position_size_pct: float
    price_target: float
    stop_loss: float
    time_horizon: str
    investment_thesis: str
    key_risks: list
    catalysts: list
    agent_signals: list
    consensus_score: float

class Orchestrator:
    def __init__(self):
        self.technical = TechnicalAgent()
        self.fundamental = FundamentalAgent(config.brapi_token)
        self.sentiment = SentimentAgent()
        self.macro = MacroAgent()
        self.client = anthropic.Anthropic(api_key=config.anthropic_api_key)

    def analyze(self, asset: str, data: dict = None) -> InvestmentDecision:
        data = data or {}

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                "technical": executor.submit(self.technical.analyze, asset, data),
                "fundamental": executor.submit(self.fundamental.analyze, asset, data),
                "sentiment": executor.submit(self.sentiment.analyze, asset, data),
                "macro": executor.submit(self.macro.analyze, asset, data),
            }
            signals = {name: future.result() for name, future in futures.items()}

        signals_summary = {
            name: {
                "signal": sig.signal,
                "confidence": sig.confidence,
                "reasoning": sig.reasoning[:500],
            }
            for name, sig in signals.items()
        }

        try:
            from data.sources.market import MarketDataSource
            market = MarketDataSource(config.brapi_token)
            quote = market.get_stock_quote(asset)
            current_price = quote["price"]
        except:
            current_price = 0.0

        prompt = f"""Tome a decisão de portfólio para {asset} (preço atual: R$ {current_price:.2f}):

Sinais dos analistas:
{json.dumps(signals_summary, indent=2, ensure_ascii=False)}

Gere a decisão consolidada com tese, preço-alvo, stop-loss e sizing.
Retorne o JSON."""

        try:
            response = self.client.messages.create(
                model=config.llm_model,
                max_tokens=1500,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = response.content[0].text
            clean = raw.strip().strip("```json").strip("```").strip()
            result = json.loads(clean)
        except Exception as e:
            result = {
                "final_signal": "HOLD",
                "consolidated_confidence": 0.0,
                "position_size_pct": 0.0,
                "price_target": current_price,
                "stop_loss": current_price * 0.92,
                "time_horizon": "medium",
                "investment_thesis": f"Erro na orquestração: {e}",
                "key_risks": [],
                "catalysts": [],
                "consensus_score": 0.0,
            }

        return InvestmentDecision(
            asset=asset,
            final_signal=result["final_signal"],
            consolidated_confidence=result["consolidated_confidence"],
            position_size_pct=min(result.get("position_size_pct", 0), config.max_position_pct),
            price_target=result.get("price_target", 0),
            stop_loss=result.get("stop_loss", 0),
            time_horizon=result.get("time_horizon", "medium"),
            investment_thesis=result.get("investment_thesis", ""),
            key_risks=result.get("key_risks", []),
            catalysts=result.get("catalysts", []),
            agent_signals=list(signals.values()),
            consensus_score=result.get("consensus_score", 0.0),
        )