"""European option pricing under constant-volatility Black–Scholes assumptions."""
from dataclasses import dataclass
from math import erf, exp, log, sqrt

import numpy as np


@dataclass(frozen=True)
class OptionParameters:
    spot: float = 100.0
    strike: float = 100.0
    rate: float = 0.05
    volatility: float = 0.20
    maturity: float = 1.0

    def validate(self) -> None:
        if self.spot <= 0 or self.strike <= 0:
            raise ValueError("Spot and strike must be positive.")
        if self.volatility <= 0 or self.maturity <= 0:
            raise ValueError("Volatility and maturity must be positive.")


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


def black_scholes(params: OptionParameters, kind: str = "call") -> float:
    params.validate()
    if kind not in ("call", "put"):
        raise ValueError("kind must be 'call' or 'put'")
    s, k, r, sigma, t = (
        params.spot, params.strike, params.rate,
        params.volatility, params.maturity,
    )
    d1 = (log(s / k) + (r + sigma**2 / 2) * t) / (sigma * sqrt(t))
    d2 = d1 - sigma * sqrt(t)
    if kind == "call":
        return s * normal_cdf(d1) - k * exp(-r * t) * normal_cdf(d2)
    return k * exp(-r * t) * normal_cdf(-d2) - s * normal_cdf(-d1)


def monte_carlo(
    params: OptionParameters, simulations: int = 100_000,
    kind: str = "call", seed: int = 42,
) -> float:
    params.validate()
    if simulations < 1:
        raise ValueError("simulations must be positive")
    if kind not in ("call", "put"):
        raise ValueError("kind must be 'call' or 'put'")
    rng = np.random.default_rng(seed)
    shocks = rng.standard_normal(simulations)
    terminal = params.spot * np.exp(
        (params.rate - 0.5 * params.volatility**2) * params.maturity
        + params.volatility * np.sqrt(params.maturity) * shocks
    )
    payoff = np.maximum(
        terminal - params.strike if kind == "call" else params.strike - terminal,
        0.0,
    )
    return float(np.exp(-params.rate * params.maturity) * payoff.mean())
