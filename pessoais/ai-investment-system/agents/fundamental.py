"""
Agente Fundamentalista.
Analisa múltiplos de valuation, qualidade e crescimento.
"""
import json
import requests
from agents.base import BaseAgent, AgentSignal

SYSTEM_PROMPT = """Você é um analista fundamentalista especializado em ações brasileiras.
Receberá dados financeiros de uma empresa e deve avaliar:

1. VALUATION: P/L, P/VPA, EV/EBITDA
2. QUALIDADE: ROE, ROIC, margens
3. CRESCIMENTO: receita, lucro, caixa
4. ENDIVIDAMENTO: Dívida/EBITDA, cobertura de juros
5. DIVIDENDOS: DY, payout, consistência

Retorne APENAS JSON:
{
  "signal": "BUY|SELL|HOLD|AVOID",
  "confidence": 0.0,
  "reasoning": "análise detalhada",
  "fair_value_estimate": 0.0,
  "upside_pct": 0.0
}"""

def get_fundamentals_brapi(ticker: str, token: str = "") -> dict:
    url = f"https://brapi.dev/api/quote/{ticker}"
    params = {
        "modules": "summaryProfile,defaultKeyStatistics,financialData,earningsTrend",
        "token": token,
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()["results"][0]
        return {
            "ticker": ticker,
            "price": data.get("regularMarketPrice"),
            "pe_ratio": data.get("priceEarningsRatio"),
            "pb_ratio": data.get("priceToBook"),
            "roe": data.get("returnOnEquity"),
            "profit_margin": data.get("profitMargins"),
            "revenue_growth": data.get("revenueGrowth"),
            "earnings_growth": data.get("earningsGrowth"),
            "debt_to_equity": data.get("debtToEquity"),
            "current_ratio": data.get("currentRatio"),
            "dividend_yield": data.get("dividendYield"),
            "payout_ratio": data.get("payoutRatio"),
            "market_cap": data.get("marketCap"),
            "enterprise_value": data.get("enterpriseValue"),
            "ebitda": data.get("ebitda"),
            "sector": data.get("sector"),
            "industry": data.get("industry"),
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}

class FundamentalAgent(BaseAgent):
    def __init__(self, brapi_token: str = ""):
        super().__init__("FundamentalAgent", SYSTEM_PROMPT)
        self.brapi_token = brapi_token

    def analyze(self, asset: str, data: dict = None) -> AgentSignal:
        fundamentals = data or get_fundamentals_brapi(asset, self.brapi_token)

        if "error" in fundamentals:
            return AgentSignal(self.name, asset, "HOLD", 0.0, f"Erro nos dados: {fundamentals['error']}", {})

        try:
            from data.sources.macro import get_bcb_series
            selic = float(get_bcb_series("selic_meta", days=30).iloc[-1])
        except:
            selic = 10.5

        prompt = f"""Analise os fundamentos de {asset}:

{json.dumps(fundamentals, indent=2)}

Taxa Selic atual: {selic}% a.a.

Retorne o JSON com signal, confidence, reasoning, fair_value_estimate e upside_pct."""

        try:
            response = self._call_llm(prompt, max_tokens=1200)
            clean = response.strip().strip("```json").strip("```").strip()
            result = json.loads(clean)
            return AgentSignal(
                agent_name=self.name,
                asset=asset,
                signal=result["signal"],
                confidence=float(result["confidence"]),
                reasoning=result["reasoning"],
                data_points={
                    **fundamentals,
                    "selic": selic,
                    "fair_value": result.get("fair_value_estimate"),
                    "upside_pct": result.get("upside_pct"),
                },
            )
        except Exception as e:
            return AgentSignal(self.name, asset, "HOLD", 0.0, f"Erro LLM: {e}", fundamentals)