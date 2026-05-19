"""
Entry point — roda uma análise completa no terminal.

Uso:
  python main.py PETR4
  python main.py VALE3
  python main.py BTC
"""
import sys
from dotenv import load_dotenv

load_dotenv()  # carrega o .env

from agents.orchestrator import Orchestrator

def print_decision(decision):
    signal_emoji = {"BUY": "🟢", "SELL": "🔴", "HOLD": "🟡", "AVOID": "⚫"}.get(decision.final_signal, "⚪")

    print("\n" + "="*60)
    print(f"  {signal_emoji}  DECISÃO FINAL: {decision.final_signal} — {decision.asset}")
    print("="*60)
    print(f"  Confiança consolidada : {decision.consolidated_confidence:.0%}")
    print(f"  Tamanho da posição    : {decision.position_size_pct:.0%} do portfólio")
    print(f"  Preço-alvo            : R$ {decision.price_target:.2f}")
    print(f"  Stop-loss             : R$ {decision.stop_loss:.2f}")
    print(f"  Horizonte             : {decision.time_horizon}")
    print(f"  Consenso dos agentes  : {decision.consensus_score:.0%}")

    print("\n--- SINAIS POR AGENTE ---")
    for sig in decision.agent_signals:
        emoji = {"BUY": "🟢", "SELL": "🔴", "HOLD": "🟡", "AVOID": "⚫"}.get(sig.signal, "⚪")
        print(f"  {emoji} {sig.agent_name:<22} {sig.signal:<6} (confiança: {sig.confidence:.0%})")

    print("\n--- TESE DE INVESTIMENTO ---")
    print(f"  {decision.investment_thesis}")

    print("\n--- RISCOS PRINCIPAIS ---")
    for r in decision.key_risks:
        print(f"  ⚠  {r}")

    print("\n--- CATALISADORES ---")
    for c in decision.catalysts:
        print(f"  🚀  {c}")

    print("="*60 + "\n")

if __name__ == "__main__":
    ticker = sys.argv[1].upper() if len(sys.argv) > 1 else "PETR4"
    print(f"\n🤖 Iniciando análise de {ticker} com todos os agentes...")
    print("   (pode levar 30-60 segundos)\n")

    orchestrator = Orchestrator()
    decision = orchestrator.analyze(ticker)
    print_decision(decision)