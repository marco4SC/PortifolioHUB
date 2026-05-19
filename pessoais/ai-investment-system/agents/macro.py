"""
Agente Macro & Risco.
Avalia o ambiente macroeconômico e risco sistêmico.
"""
import json
from agents.base import BaseAgent, AgentSignal
from data.sources.macro import get_macro_snapshot, get_bcb_series

SYSTEM_PROMPT = """Você é um economista e gestor de risco especializado no mercado brasileiro.
Receberá dados macroeconômicos e deve avaliar:

1. AMBIENTE MACRO: Selic vs. inflação → taxa real
2. CÂMBIO: USD/BRL impacta exportadoras positivamente, importadoras negativamente
3. RISCO: Ambiente fiscal, político
4. POSICIONAMENTO: O cenário macro favorece risco ou defensiva?

Para renda fixa:
- Se Selic > IPCA + 4%, renda fixa está muito atraente

Retorne APENAS JSON:
{
  "signal": "BUY|SELL|HOLD|AVOID",
  "confidence": 0.0,
  "macro_score": 0.0,
  "reasoning": "análise detalhada",
  "risk_factors": ["fator1"],
  "tailwinds": ["vento favorável 1"]
}"""

class MacroAgent(BaseAgent):
    def __init__(self):
        super().__init__("MacroAgent", SYSTEM_PROMPT)

    def _classify_asset(self, asset: str) -> str:
        if asset in ["BTC", "ETH", "SOL"]:
            return "cryptocurrency"
        if any(f in asset for f in ["TESOURO", "CDB", "LCI", "LCA"]):
            return "fixed_income"
        return "brazilian_stock"

    def analyze(self, asset: str, data: dict = None) -> AgentSignal:
        macro = get_macro_snapshot()

        selic = macro.get("selic_meta", {}).get("latest", 10.5)
        ipca_mensal = macro.get("ipca_mensal", {}).get("latest", 0.4)
        ipca_anual = ipca_mensal * 12
        taxa_real = selic - ipca_anual

        macro_context = {
            **macro,
            "taxa_real_estimada_anual": round(taxa_real, 2),
            "asset": asset,
            "asset_type": self._classify_asset(asset),
        }

        prompt = f"""Avalie o impacto do cenário macroeconômico atual sobre {asset}:

{json.dumps(macro_context, indent=2)}

Taxa real estimada: {taxa_real:.1f}% a.a.
Custo de oportunidade: Selic {selic:.1f}%

Retorne o JSON."""

        try:
            response = self._call_llm(prompt, max_tokens=1000)
            clean = response.strip().strip("```json").strip("```").strip()
            result = json.loads(clean)
            return AgentSignal(
                agent_name=self.name,
                asset=asset,
                signal=result["signal"],
                confidence=float(result["confidence"]),
                reasoning=result["reasoning"],
                data_points={
                    "macro_snapshot": macro_context,
                    "macro_score": result.get("macro_score"),
                    "risk_factors": result.get("risk_factors", []),
                    "tailwinds": result.get("tailwinds", []),
                },
            )
        except Exception as e:
            return AgentSignal(self.name, asset, "HOLD", 0.0, f"Erro: {e}", macro)