"""
Gestão de risco: stop-loss, drawdown, VaR, sizing.
"""
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime

@dataclass
class Position:
    asset: str
    quantity: float
    avg_price: float
    current_price: float
    stop_loss: float
    target_price: float
    opened_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def market_value(self) -> float:
        return self.quantity * self.current_price

    @property
    def unrealized_pnl(self) -> float:
        return self.quantity * (self.current_price - self.avg_price)

    @property
    def unrealized_pnl_pct(self) -> float:
        return (self.current_price / self.avg_price - 1) * 100

    @property
    def stop_triggered(self) -> bool:
        return self.current_price <= self.stop_loss

    @property
    def target_reached(self) -> bool:
        return self.current_price >= self.target_price

@dataclass
class Portfolio:
    cash: float
    positions: Dict[str, Position] = field(default_factory=dict)
    trade_history: List[dict] = field(default_factory=list)
    peak_value: float = 0.0

    @property
    def total_invested(self) -> float:
        return sum(p.market_value for p in self.positions.values())

    @property
    def total_value(self) -> float:
        return self.cash + self.total_invested

    @property
    def drawdown_pct(self) -> float:
        if self.peak_value == 0:
            return 0.0
        return (self.total_value / self.peak_value - 1) * 100

    def update_peak(self):
        if self.total_value > self.peak_value:
            self.peak_value = self.total_value

class RiskManager:
    def __init__(self, portfolio: Portfolio, max_drawdown_pct: float = -15.0,
                 max_position_pct: float = 0.20):
        self.portfolio = portfolio
        self.max_drawdown_pct = max_drawdown_pct
        self.max_position_pct = max_position_pct

    def check_stops(self) -> List[str]:
        return [asset for asset, pos in self.portfolio.positions.items() if pos.stop_triggered]

    def check_drawdown_breach(self) -> bool:
        return self.portfolio.drawdown_pct <= self.max_drawdown_pct

    def max_buy_value(self, asset: str) -> float:
        total = self.portfolio.total_value
        current_exposure = self.portfolio.positions.get(asset)
        current_value = current_exposure.market_value if current_exposure else 0.0
        return max(0.0, total * self.max_position_pct - current_value)

    def var_95(self, returns: pd.Series) -> float:
        if len(returns) < 30:
            return 0.0
        return float(np.percentile(returns.dropna(), 5))

    def position_size(self, confidence: float, signal_strength: float,
                      available_cash: float) -> float:
        kelly_fractional = (confidence * signal_strength) / 4
        max_value = self.portfolio.total_value * self.max_position_pct
        proposed = self.portfolio.total_value * kelly_fractional
        return min(proposed, max_value, available_cash)

    def rebalance_needed(self, target_weights: Dict[str, float],
                         threshold: float = 0.05) -> Dict[str, float]:
        total = self.portfolio.total_value
        adjustments = {}
        for asset, target_pct in target_weights.items():
            current_value = (self.portfolio.positions[asset].market_value
                           if asset in self.portfolio.positions else 0.0)
            current_pct = current_value / total if total > 0 else 0.0
            deviation = current_pct - target_pct
            if abs(deviation) > threshold:
                adjustments[asset] = -deviation
        return adjustments