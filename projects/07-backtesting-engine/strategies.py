"""Reusable, long-only trading signal generators. Signals are known at the close."""
import pandas as pd


def moving_average_crossover(data: pd.DataFrame, fast: int = 20, slow: int = 50) -> pd.Series:
    """Return a 0/1 long-only signal using information through each closing price."""
    if not 0 < fast < slow:
        raise ValueError("Require 0 < fast < slow")
    if "Close" not in data:
        raise ValueError("Data must have a Close column")

    close = data["Close"].astype(float)
    short_ma = close.rolling(fast, min_periods=fast).mean()
    long_ma = close.rolling(slow, min_periods=slow).mean()
    signals = ((short_ma > long_ma) & long_ma.notna()).astype(int)
    return signals.rename("signal")
