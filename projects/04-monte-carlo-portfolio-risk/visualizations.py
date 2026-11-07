import numpy as np
import matplotlib.pyplot as plt


def plot_simulation_paths(portfolio_paths, initial_value):
    plt.figure(figsize=(12, 6))

    for path in portfolio_paths[:100]:
        plt.plot(path, alpha=0.2)

    plt.axhline(
        initial_value,
        color="black",
        linestyle="--",
        label="Initial Capital"
    )

    plt.title("Monte Carlo Portfolio Simulations")
    plt.xlabel("Trading Days")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.grid(alpha=0.2)
    plt.tight_layout()


def plot_final_distribution(final_values, initial_value):
    plt.figure(figsize=(12, 6))

    plt.hist(
        final_values,
        bins=70,
        edgecolor="black",
        alpha=0.75
    )

    plt.axvline(
        initial_value,
        color="red",
        linestyle="--",
        label="Initial Capital"
    )

    fifth_percentile = np.percentile(
        final_values, 5
    )

    plt.axvline(
        fifth_percentile,
        color="orange",
        linestyle="--",
        label="5th Percentile"
    )

    plt.title("Distribution of Final Portfolio Values")
    plt.xlabel("Final Portfolio Value ($)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(alpha=0.2)
    plt.tight_layout()


def plot_drawdown_distribution(max_drawdowns):
    plt.figure(figsize=(12, 6))

    plt.hist(
        max_drawdowns * 100,
        bins=60,
        edgecolor="black",
        alpha=0.75
    )

    plt.title("Distribution of Maximum Drawdowns")
    plt.xlabel("Maximum Drawdown (%)")
    plt.ylabel("Frequency")
    plt.grid(alpha=0.2)
    plt.tight_layout()


def plot_loss_distribution(final_values, initial_value):
    losses = initial_value - final_values

    plt.figure(figsize=(12, 6))
    plt.hist(losses, bins=60, edgecolor="black", alpha=0.75)

    for confidence in (0.95, 0.99):
        var = max(0.0, np.percentile(losses, confidence * 100))

        plt.axvline(
            var,
            linestyle="--",
            label=f"{confidence:.0%} VaR: ${var:,.2f}"
        )

    plt.title("Portfolio Loss Distribution")
    plt.xlabel("Loss ($) — negative values represent gains")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()


def plot_percentile_paths(portfolio_paths, initial_value):
    lower, median, upper = np.percentile(
        portfolio_paths, [5, 50, 95], axis=0
    )

    days = np.arange(portfolio_paths.shape[1])

    plt.figure(figsize=(12, 6))

    plt.fill_between(
        days, lower, upper,
        alpha=0.2,
        label="5th–95th Percentile Range"
    )

    plt.plot(days, median, label="Median Portfolio Value")

    plt.axhline(
        initial_value,
        linestyle="--",
        label="Initial Capital"
    )

    plt.title("Monte Carlo Portfolio Percentile Paths")
    plt.xlabel("Trading Days")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.tight_layout()


def generate_all_plots(
    portfolio_paths,
    initial_value,
    risk_results
):
    plot_simulation_paths(
        portfolio_paths, initial_value
    )

    plot_final_distribution(
        risk_results["final_values"], initial_value
    )

    plot_drawdown_distribution(
        risk_results["max_drawdowns"]
    )

    plot_loss_distribution(
        risk_results["final_values"], initial_value
    )

    plot_percentile_paths(
        portfolio_paths, initial_value
    )

    plt.show()
