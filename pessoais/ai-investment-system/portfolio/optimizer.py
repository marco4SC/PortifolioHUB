"""
Otimização de portfólio: Markowitz e Risk Parity.
"""
import numpy as np
import pandas as pd
from typing import Dict

try:
    from scipy.optimize import minimize
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

def optimize_portfolio_markowitz(
    returns: pd.DataFrame,
    risk_free_rate: float = 0.105,
    target: str = "max_sharpe"
) -> Dict[str, float]:
    if not SCIPY_AVAILABLE:
        n = len(returns.columns)
        return {col: 1/n for col in returns.columns}

    mu = returns.mean() * 252
    cov = returns.cov() * 252
    n = len(returns.columns)

    def portfolio_performance(weights):
        ret = np.dot(weights, mu)
        std = np.sqrt(weights @ cov.values @ weights)
        sharpe = (ret - risk_free_rate) / std if std > 0 else 0
        return ret, std, sharpe

    def neg_sharpe(weights):
        return -portfolio_performance(weights)[2]

    def portfolio_variance(weights):
        return weights @ cov.values @ weights

    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
    bounds = tuple((0.0, 0.25) for _ in range(n))
    w0 = np.ones(n) / n

    obj = neg_sharpe if target == "max_sharpe" else portfolio_variance
    result = minimize(obj, w0, method="SLSQP", bounds=bounds, constraints=constraints)

    if result.success:
        weights = result.x
        weights[weights < 0.01] = 0
        weights /= weights.sum()
    else:
        weights = np.ones(n) / n

    return dict(zip(returns.columns, weights.round(4)))

def equal_risk_contribution(cov_matrix: pd.DataFrame) -> Dict[str, float]:
    n = len(cov_matrix)
    w0 = np.ones(n) / n

    def risk_contributions(weights):
        cov = cov_matrix.values
        portfolio_var = weights @ cov @ weights
        marginal_contrib = cov @ weights
        return weights * marginal_contrib / portfolio_var

    def objective(weights):
        rc = risk_contributions(weights)
        target = np.ones(n) / n
        return np.sum((rc - target) ** 2)

    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
    bounds = tuple((0.01, 0.40) for _ in range(n))

    result = minimize(objective, w0, method="SLSQP", bounds=bounds, constraints=constraints)
    weights = result.x / result.x.sum() if result.success else w0
    return dict(zip(cov_matrix.columns, weights.round(4)))