import os
import matplotlib.pyplot as plt


def generate_plots(df):
    os.makedirs("figures", exist_ok=True)

    # Figure 1: Price, moving average, entry/exit points
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df["Close"], label="SPY")
    ax.plot(df.index, df["SMA20"], label="20-Day SMA")

    buys = df[df["Signal"] == 1]
    sells = df[df["Signal"] == -1]

    ax.scatter(
        buys.index, buys["Close"],
        marker="^", color="green", label="Buy"
    )
    ax.scatter(
        sells.index, sells["Close"],
        marker="v", color="red", label="Sell"
    )

    ax.set_title("SPY Mean Reversion - Trading Signals")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("figures/01_trading_signals.png", dpi=150)
    plt.close(fig)

    # Figure 2: Strategy vs. buy-and-hold
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(
        df.index, df["Strategy_Equity"],
        label="Mean Reversion"
    )
    ax.plot(
        df.index, df["Benchmark_Equity"],
        label="SPY Buy & Hold"
    )

    ax.set_title("Portfolio Equity Comparison")
    ax.set_ylabel("Portfolio Value ($)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("figures/02_equity_curve.png", dpi=150)
    plt.close(fig)

    # Figure 3: Drawdown
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(
        df.index,
        df["Drawdown"] * 100,
        0,
        alpha=0.4
    )

    ax.set_title("Mean Reversion Strategy Drawdown")
    ax.set_ylabel("Drawdown (%)")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("figures/03_drawdown.png", dpi=150)
    plt.close(fig)

    print("\nSaved 3 charts to figures/")
