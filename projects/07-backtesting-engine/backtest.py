"""Signal-at-close / trade-next-open backtesting engine."""
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class BacktestResult:
    daily: pd.DataFrame
    trades: pd.DataFrame
    initial_capital: float
    cost_bps: float


def run_backtest(
    data: pd.DataFrame,
    signals: pd.Series,
    initial_capital: float = 10_000.0,
    cost_bps: float = 5.0,
) -> BacktestResult:
    """Trade at the next open after each closing signal; hold open-to-open.

    Adjusted OHLC prices are required for total-return approximations.
    A cost is charged on every position change, including a terminal liquidation.
    """
    if initial_capital <= 0 or cost_bps < 0:
        raise ValueError("Capital must be positive and trading costs nonnegative")
    if not {"Open", "Close"}.issubset(data.columns):
        raise ValueError("Data must have Open and Close columns")

    prices = data[["Open", "Close"]].copy().sort_index()
    if prices.empty or prices.index.has_duplicates:
        raise ValueError("Data must be nonempty with unique dates")
    if prices.isna().any().any() or (prices <= 0).any().any():
        raise ValueError("Prices must be finite and strictly positive")
    if not np.isfinite(prices.to_numpy()).all():
        raise ValueError("Prices must be finite")
    if len(prices) < 3:
        raise ValueError("Need at least three observations")

    signal = signals.reindex(prices.index)
    if signal.isna().any() or not signal.isin([0, 1]).all():
        raise ValueError("Provide a 0/1 signal for each price date")

    # Close of day t determines holdings starting at open t+1.
    position = signal.shift(1, fill_value=0).astype(int)
    # At the final open, liquidate any open position; there is no future interval.
    position.iloc[-1] = 0
    forward_return = prices["Open"].shift(-1) / prices["Open"] - 1
    forward_return.iloc[-1] = 0.0

    prior_position = position.shift(1, fill_value=0)
    turnover = (position - prior_position).abs()
    fee_rate = cost_bps / 10_000.0
    # Fee is paid at the current open, then invested capital earns interval return.
    net_factor = (1.0 - turnover * fee_rate) * (1.0 + position * forward_return)
    if (net_factor <= 0).any():
        raise ValueError("Invalid wealth factor: check input returns and costs")

    equity = initial_capital * net_factor.cumprod()
    benchmark = initial_capital * (1.0 + forward_return).cumprod()
    # Index t means state AFTER costs at open t and AFTER the t -> t+1 interval.
    daily = prices.assign(
        signal=signal.astype(int),
        position=position,
        forward_return=forward_return,
        turnover=turnover,
        net_return=net_factor - 1.0,
        equity=equity,
        benchmark=benchmark,
    )
    daily["drawdown"] = daily["equity"] / daily["equity"].cummax().clip(lower=initial_capital) - 1.0

    trade_rows = []
    entry_date = None
    entry_price = None
    for date in prices.index:
        pos, prev = int(position.loc[date]), int(prior_position.loc[date])
        px = float(prices.at[date, "Open"])
        if prev == 0 and pos == 1:
            entry_date, entry_price = date, px
        elif prev == 1 and pos == 0:
            gross = px / entry_price - 1.0
            net = (1.0 - fee_rate) ** 2 * (px / entry_price) - 1.0
            trade_rows.append({
                "entry_date": entry_date,
                "exit_date": date,
                "entry_price": entry_price,
                "exit_price": px,
                "gross_return": gross,
                "net_return": net,
            })
            entry_date = entry_price = None
    trades = pd.DataFrame(
        trade_rows,
        columns=["entry_date", "exit_date", "entry_price", "exit_price", "gross_return", "net_return"],
    )
    return BacktestResult(daily=daily, trades=trades, initial_capital=initial_capital, cost_bps=cost_bps)
