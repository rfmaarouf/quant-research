"""Project 06 baseline: compare Black–Scholes with Monte Carlo option pricing."""
import csv
from pathlib import Path

import matplotlib.pyplot as plt

from pricing import OptionParameters, black_scholes, monte_carlo


def main() -> None:
    params = OptionParameters()
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(exist_ok=True)

    sizes = [100, 1_000, 10_000, 100_000]
    rows = []
    for kind in ("call", "put"):
        analytical = black_scholes(params, kind)
        for n in sizes:
            simulated = monte_carlo(params, simulations=n, kind=kind, seed=42)
            rows.append({
                "option_type": kind,
                "simulations": n,
                "black_scholes": analytical,
                "monte_carlo": simulated,
                "absolute_error": abs(simulated - analytical),
            })
            print(f"{kind.upper():4} | paths={n:>6,} | BS=${analytical:.4f} | MC=${simulated:.4f} | error=${abs(simulated-analytical):.4f}")

    with (output / "pricing_comparison.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    for kind in ("call", "put"):
        subset = [row for row in rows if row["option_type"] == kind]
        plt.plot([r["simulations"] for r in subset],
                 [r["absolute_error"] for r in subset],
                 marker="o", label=kind.title())
    plt.xscale("log")
    plt.xlabel("Simulated paths (log scale)")
    plt.ylabel("Absolute pricing error ($)")
    plt.title("Monte Carlo convergence vs Black–Scholes")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output / "convergence.png", dpi=160)
    plt.close()
    print(f"Saved results to: {output}")


if __name__ == "__main__":
    main()
