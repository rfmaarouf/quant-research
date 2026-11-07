import numpy as np


def calculate_var(profits_losses, confidence=0.95):
    """
    Estimate Value at Risk from simulated P&L.
    Positive results represent potential losses.
    """
    pnl = np.asarray(profits_losses, dtype=float)

    percentile = 100 * (1 - confidence)
    threshold = np.percentile(pnl, percentile)

    return max(0.0, -threshold)


def calculate_cvar(profits_losses, confidence=0.95):
    """
    Estimate Conditional Value at Risk (CVaR)
    using the average loss in the worst tail.
    """
    pnl = np.asarray(profits_losses, dtype=float)

    percentile = 100 * (1 - confidence)
    threshold = np.percentile(pnl, percentile)

    tail_losses = pnl[pnl <= threshold]

    return max(0.0, -tail_losses.mean())


def calculate_max_drawdowns(portfolio_paths):
    """
    Calculate maximum drawdown for every
    simulated portfolio path.

    Expected shape:
    simulations x trading days
    """
    paths = np.asarray(portfolio_paths, dtype=float)

    running_peaks = np.maximum.accumulate(
        paths, axis=1
    )

    drawdowns = (
        paths - running_peaks
    ) / running_peaks

    max_drawdowns = drawdowns.min(axis=1)

    return max_drawdowns


def calculate_risk_report(
    portfolio_paths,
    initial_value,
    confidence_levels=(0.95, 0.99)
):
    """
    Generate risk statistics from all
    simulated portfolio paths.
    """
    final_values = portfolio_paths[:, -1]

    pnl = final_values - initial_value

    max_drawdowns = calculate_max_drawdowns(
        portfolio_paths
    )

    print("\n" + "=" * 45)
    print("MONTE CARLO PORTFOLIO RISK REPORT")
    print("=" * 45)

    print(f"Initial Capital: ${initial_value:,.2f}")
    print(f"Mean Final Value: ${final_values.mean():,.2f}")
    print(f"Median Final Value: ${np.median(final_values):,.2f}")

    print(
        f"Probability of Loss: "
        f"{np.mean(pnl < 0):.2%}"
    )

    for confidence in confidence_levels:
        var = calculate_var(pnl, confidence)
        cvar = calculate_cvar(pnl, confidence)

        print(f"\nConfidence Level: {confidence:.0%}")
        print(f"VaR: ${var:,.2f}")
        print(f"CVaR: ${cvar:,.2f}")

    print("\nDrawdown Statistics:")
    print(
        f"Average Maximum Drawdown: "
        f"{np.mean(max_drawdowns):.2%}"
    )

    print(
        f"5th Percentile Maximum Drawdown: "
        f"{np.percentile(max_drawdowns, 5):.2%}"
    )

    print(
        f"Worst Simulated Maximum Drawdown: "
        f"{np.min(max_drawdowns):.2%}"
    )

    return {
        "final_values": final_values,
        "pnl": pnl,
        "max_drawdowns": max_drawdowns
    }
