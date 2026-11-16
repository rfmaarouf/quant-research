"""Performance measures for a daily, open-to-open equity curve."""
import numpy as np
import pandas as pd

from backtest import BacktestResult


def performance_metrics(result: BacktestResult, annual_periods: int = 252) -> dict:
    daily = result.daily
    if annual_periods <= 0:
        raise ValueError("annual_periods must be positive")

    # Last row is terminal liquidation only, not an additional holding day.
    interval_returns = daily["net_return"].iloc[:-1]
    n = len(interval_returns)
    equity = float(daily["equity"].iloc[-1])
    total = equity / result.initial_capital - 1.0
    ann_return = (equity / result.initial_capital) ** (annual_periods / n) - 1.0
    vol = float(interval_returns.std(ddof=1) * np.sqrt(annual_periods)) if n > 1 else 0.0
    sharpe = float(interval_returns.mean() / interval_returns.std(ddof=1) * np.sqrt(annual_periods)) if n > 1 and interval_returns.std(ddof=1) > 0 else 0.0
    return {
        "initial_capital": result.initial_capital,
        "final_equity": equity,
        "total_return": total,
        "annualized_return": ann_return,
        "annualized_volatility": vol,
        "sharpe_ratio_rf0": sharpe,
        "max_drawdown": float(daily["drawdown"].min()),
        "benchmark_return": float(daily["benchmark"].iloc[-1] / result.initial_capital - 1),
        "time_in_market": float(daily["position"].iloc[:-1].mean()),
        "round_trip_trades": len(result.trades),
        "trade_win_rate": float((result.trades["net_return"] > 0).mean()) if len(result.trades) else 0.0,
        "total_turnover": float(daily["turnover"].sum()),
    }


def format_report(metrics: dict) -> str:
    return "\n".join([
        "PROJECT 07 — BACKTESTING ENGINE",
        "=" * 44,
        f"Initial Capital       : ${metrics['initial_capital']:,.2f}",
        f"Final Equity          : ${metrics['final_equity']:,.2f}",
        f"Total Return          : {metrics['total_return']:.2%}",
        f"Annualized Return     : {metrics['annualized_return']:.2%}",
        f"Annualized Volatility : {metrics['annualized_volatility']:.2%}",
        f"Sharpe (rf = 0)       : {metrics['sharpe_ratio_rf0']:.3f}",
        f"Max Drawdown          : {metrics['max_drawdown']:.2%}",
        f"Buy/Hold Return       : {metrics['benchmark_return']:.2%}",
        f"Time in Market        : {metrics['time_in_market']:.2%}",
        f"Round-Trip Trades     : {metrics['round_trip_trades']}",
        f"Trade Win Rate        : {metrics['trade_win_rate']:.2%}",
        f"Total Turnover        : {metrics['total_turnover']:.0f}",
    ])
