"""Deterministic tests: no live downloads or market-data dependencies."""
import unittest

import numpy as np
import pandas as pd

from backtest import run_backtest
from metrics import performance_metrics
from strategies import moving_average_crossover


class BacktestTests(unittest.TestCase):
    def setUp(self):
        dates = pd.bdate_range("2025-01-02", periods=8)
        self.data = pd.DataFrame({
            "Open": [100, 100, 110, 121, 121, 120, 120, 120],
            "Close": [100, 110, 120, 120, 110, 100, 100, 100],
        }, index=dates)

    def test_next_open_execution(self):
        signal = pd.Series([0, 1, 1, 0, 0, 0, 0, 0], index=self.data.index)
        result = run_backtest(self.data, signal, cost_bps=0)
        # Signal on day 2 close => hold from day 3 open (110) to day 5 open (121).
        self.assertEqual(result.daily["position"].tolist(), [0, 0, 1, 1, 0, 0, 0, 0])
        self.assertAlmostEqual(result.daily["equity"].iloc[-1], 11000)
        self.assertEqual(len(result.trades), 1)
        self.assertAlmostEqual(result.trades["gross_return"].iloc[0], 0.1)

    def test_costs_on_entry_and_exit(self):
        signal = pd.Series([0, 1, 1, 0, 0, 0, 0, 0], index=self.data.index)
        result = run_backtest(self.data, signal, cost_bps=10)
        self.assertAlmostEqual(result.daily["equity"].iloc[-1], 10000 * 1.1 * 0.999**2)
        self.assertEqual(result.daily["turnover"].sum(), 2)

    def test_no_same_day_signal(self):
        signal = pd.Series([1] * len(self.data), index=self.data.index)
        result = run_backtest(self.data, signal, cost_bps=0)
        self.assertEqual(result.daily["position"].iloc[0], 0)
        self.assertEqual(result.daily["position"].iloc[1], 1)
        self.assertEqual(result.daily["position"].iloc[-1], 0)

    def test_sma_signals(self):
        signal = moving_average_crossover(self.data, fast=2, slow=3)
        self.assertEqual(signal.iloc[:2].tolist(), [0, 0])
        self.assertTrue(signal.isin([0, 1]).all())

    def test_constant_cash(self):
        signal = pd.Series(0, index=self.data.index)
        result = run_backtest(self.data, signal)
        self.assertAlmostEqual(result.daily["equity"].iloc[-1], 10000)
        self.assertEqual(performance_metrics(result)["round_trip_trades"], 0)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            run_backtest(self.data, pd.Series([0, 1], index=self.data.index[:2]))
        with self.assertRaises(ValueError):
            moving_average_crossover(self.data, fast=50, slow=20)


if __name__ == "__main__":
    unittest.main()
