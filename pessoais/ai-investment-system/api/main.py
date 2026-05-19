"""
API REST — FastAPI.
Execute: uvicorn api.main:app --reload --port 8000
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
 
from agents.orchestrator import Orchestrator
from data.sources.market import MarketDataSource
from data.sources.macro import get_macro_snapshot
from config import config
 
app = FastAPI(
    title="AI Investment System",
    description="Sistema de investimentos com IA multiagente",
    version="1.0.0",
)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
orchestrator = Orchestrator()
market = MarketDataSource(config.brapi_token)
 
@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}
 
@app.get("/market/quotes")
def get_quotes(tickers: str = "PETR4,VALE3,ITUB4"):
    ticker_list = [t.strip() for t in tickers.split(",")]
    try:
        return market.get_multiple_quotes(ticker_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
@app.get("/macro/snapshot")
def macro_snapshot():
    return get_macro_snapshot()
 
@app.post("/analyze/{asset}")
def analyze_asset(asset: str, background_tasks: BackgroundTasks):
    """
    Análise completa com todos os agentes.
    Pode levar 20-60s dependendo das APIs.
    """
    try:
        decision = orchestrator.analyze(asset.upper())
 
        from monitoring.alerts import alert_decision
        background_tasks.add_task(alert_decision, decision)
 
        return {
            "asset": decision.asset,
            "final_signal": decision.final_signal,
            "consolidated_confidence": decision.consolidated_confidence,
            "position_size_pct": decision.position_size_pct,
            "price_target": decision.price_target,
            "stop_loss": decision.stop_loss,
            "time_horizon": decision.time_horizon,
            "investment_thesis": decision.investment_thesis,
            "key_risks": decision.key_risks,
            "catalysts": decision.catalysts,
            "consensus_score": decision.consensus_score,
            "agent_signals": [
                {
                    "agent": s.agent_name,
                    "signal": s.signal,
                    "confidence": s.confidence,
                    "reasoning": s.reasoning,
                }
                for s in decision.agent_signals
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
@app.get("/portfolio/summary")
def portfolio_summary():
    return {
        "total_value": 0.0,
        "cash": 0.0,
        "positions": [],
        "daily_pnl": 0.0,
        "total_return_pct": 0.0,
        "note": "Integre com sua corretora via API (XP, Clear, B3)"
    }