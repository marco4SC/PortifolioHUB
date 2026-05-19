from dataclasses import dataclass, field
from typing import List
import os

@dataclass
class Config:
    # APIs
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    brapi_token: str = os.getenv("BRAPI_TOKEN", "")
    alpha_vantage_key: str = os.getenv("ALPHA_VANTAGE_KEY", "")
    telegram_token: str = os.getenv("TELEGRAM_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")

    # Banco
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///investment.db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # Portfólio
    initial_capital: float = float(os.getenv("INITIAL_CAPITAL", "10000"))
    max_position_pct: float = 0.20
    max_drawdown_pct: float = 0.15
    rebalance_threshold: float = 0.05

    # Ativos monitorados
    stocks_br: List[str] = field(default_factory=lambda: [
        "PETR4", "VALE3", "ITUB4", "BBDC4", "WEGE3",
        "RENT3", "LREN3", "MGLU3", "ABEV3", "B3SA3"
    ])
    cryptos: List[str] = field(default_factory=lambda: [
        "BTC", "ETH", "SOL"
    ])
    fixed_income: List[str] = field(default_factory=lambda: [
        "TESOURO_SELIC", "TESOURO_IPCA_2029", "CDB_110_CDI"
    ])

    # Agentes
    llm_model: str = "claude-sonnet-4-20250514"
    agent_confidence_threshold: float = 0.6

config = Config()