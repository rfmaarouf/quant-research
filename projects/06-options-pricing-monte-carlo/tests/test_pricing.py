"""Sanity checks for Project 06 option pricing."""
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pricing import OptionParameters, black_scholes, monte_carlo


class PricingTests(unittest.TestCase):
    def setUp(self):
        self.params = OptionParameters()

    def test_put_call_parity(self):
        from math import exp
        call = black_scholes(self.params, "call")
        put = black_scholes(self.params, "put")
        parity = self.params.spot - self.params.strike * exp(
            -self.params.rate * self.params.maturity
        )
        self.assertAlmostEqual(call - put, parity, places=10)

    def test_monte_carlo_near_analytical(self):
        for kind in ("call", "put"):
            self.assertLess(
                abs(monte_carlo(self.params, 100_000, kind, seed=42)
                    - black_scholes(self.params, kind)),
                0.25,
            )

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            black_scholes(OptionParameters(volatility=0))

    def test_invalid_option_type(self):
        with self.assertRaises(ValueError):
            monte_carlo(self.params, kind="other")


if __name__ == "__main__":
    unittest.main()
