import numpy as np
import pandas as pd

WINDOW = 20
ENTRY_Z = -2.0
EXIT_Z = 0.0


def calculate_indicators(df):
    df = df.copy()

    df["SMA20"] = df["Close"].rolling(WINDOW).mean()
    df["Std20"] = df["Close"].rolling(WINDOW).std()
    df["ZScore"] = (
        (df["Close"] - df["SMA20"])
        / df["Std20"].replace(0, np.nan)
    )

    return df


def generate_signals(df):
    df = df.copy()
    positions = []
    signals = []
    holding = 0

    for z in df["ZScore"]:
        signal = 0

        if pd.notna(z):
            if holding == 0 and z <= ENTRY_Z:
                holding = 1
                signal = 1

            elif holding == 1 and z >= EXIT_Z:
                holding = 0
                signal = -1

        positions.append(holding)
        signals.append(signal)

    df["Position"] = positions
    df["Signal"] = signals

    return df
