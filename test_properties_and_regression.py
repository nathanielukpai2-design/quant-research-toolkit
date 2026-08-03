"""Property, regression, tolerance, cross-validation, and performance
tests for `trade_stats`, per Engineering Manual §15.

Per Engineering Manual §27 (Deterministic Research Rules), the
property-style tests below use Python's `random` module with a fixed
seed, so they are fully reproducible across runs and machines.
"""

import math
import random
import statistics as stdlib_statistics
import time

import pytest

from trade_stats.average_loss import average_loss
from trade_stats.average_win import average_win
from trade_stats.expectancy import expectancy
from trade_stats.loss_rate import loss_rate
from trade_stats.profit_factor import profit_factor
from trade_stats.win_rate import win_rate

# Fixed seed per Engineering Manual §27: "Random seeds must be fixed."
PROPERTY_TEST_SEED = 42
PROPERTY_TEST_TRIALS = 200


def _random_trade_sequence(rng: random.Random, length: int) -> list:
    """Generate a deterministic pseudo-random trade sequence for a given rng."""
    return [round(rng.uniform(-100.0, 100.0), 4) for _ in range(length)]


class TestProperties:
    """Property tests: invariants that must hold across many generated inputs."""

    def test_win_rate_plus_loss_rate_never_exceeds_one(self):
        rng = random.Random(PROPERTY_TEST_SEED)
        for _ in range(PROPERTY_TEST_TRIALS):
            trades = _random_trade_sequence(rng, rng.randint(1, 50))
            assert win_rate(trades) + loss_rate(trades) <= 1.0 + 1e-9

    def test_win_rate_and_loss_rate_stay_in_unit_interval(self):
        rng = random.Random(PROPERTY_TEST_SEED)
        for _ in range(PROPERTY_TEST_TRIALS):
            trades = _random_trade_sequence(rng, rng.randint(1, 50))
            assert 0.0 <= win_rate(trades) <= 1.0
            assert 0.0 <= loss_rate(trades) <= 1.0

    def test_average_loss_is_never_positive(self):
        rng = random.Random(PROPERTY_TEST_SEED)
        for _ in range(PROPERTY_TEST_TRIALS):
            trades = _random_trade_sequence(rng, rng.randint(1, 50))
            assert average_loss(trades) <= 1e-9

    def test_average_win_is_never_negative(self):
        rng = random.Random(PROPERTY_TEST_SEED)
        for _ in range(PROPERTY_TEST_TRIALS):
            trades = _random_trade_sequence(rng, rng.randint(1, 50))
            assert average_win(trades) >= -1e-9

    def test_profit_factor_is_never_negative(self):
        rng = random.Random(PROPERTY_TEST_SEED)
        for _ in range(PROPERTY_TEST_TRIALS):
            trades = _random_trade_sequence(rng, rng.randint(1, 50))
            assert profit_factor(trades) >= 0.0

    def test_expectancy_matches_arithmetic_mean(self):
        rng = random.Random(PROPERTY_TEST_SEED)
        for _ in range(PROPERTY_TEST_TRIALS):
            trades = _random_trade_sequence(rng, rng.randint(1, 50))
            assert expectancy(trades) == pytest.approx(sum(trades) / len(trades), abs=1e-9)


class TestNumericalRegression:
    """Pinned input/output pairs so future changes cannot silently alter results."""

    def test_win_rate_regression(self):
        assert win_rate([10, -5, 20, -1, 0]) == pytest.approx(0.4)

    def test_average_win_regression(self):
        assert average_win([10, -5, 20, -1, 0]) == pytest.approx(15.0)

    def test_average_loss_regression(self):
        assert average_loss([10, -5, 20, -1, 0]) == pytest.approx(-3.0)

    def test_profit_factor_regression(self):
        assert profit_factor([10, -5, 20, -1, 0]) == pytest.approx(5.0)

    def test_expectancy_regression(self):
        assert expectancy([10, -5, 20, -1, 0]) == pytest.approx(4.8)


class TestFloatingPointTolerance:
    """Tests using math.isclose() rather than exact equality, per Engineering Manual §11."""

    def test_win_rate_tolerance(self):
        result = win_rate([0.1, 0.1, 0.1, -0.1, -0.1])
        assert math.isclose(result, 0.6, rel_tol=1e-9)

    def test_expectancy_tolerance_with_float_accumulation(self):
        trades = [0.1] * 7 + [-0.3] * 3  # prone to float accumulation error
        result = expectancy(trades)
        expected = sum(trades) / len(trades)
        assert math.isclose(result, expected, rel_tol=1e-9, abs_tol=1e-12)

    def test_breakeven_boundary_within_tolerance(self):
        # A value just inside TRADE_PNL_EPSILON must be breakeven, not a win/loss.
        assert win_rate([1e-13]) == pytest.approx(0.0)
        assert loss_rate([1e-13]) == pytest.approx(0.0)


class TestCrossValidation:
    """Cross-validation against an independent reference implementation."""

    def test_expectancy_against_stdlib_mean(self):
        trades = [12.5, -7.25, 30.0, -2.1, 0.0, -15.0, 8.8]
        assert expectancy(trades) == pytest.approx(stdlib_statistics.mean(trades))

    def test_expectancy_against_stdlib_mean_random(self):
        rng = random.Random(PROPERTY_TEST_SEED)
        for _ in range(50):
            trades = _random_trade_sequence(rng, rng.randint(2, 50))
            assert expectancy(trades) == pytest.approx(stdlib_statistics.mean(trades), abs=1e-9)


class TestPerformance:
    """Lightweight performance smoke test.

    All functions in this package are documented as O(n) time / O(1)
    extra space (beyond the input itself), per Engineering Manual §13.
    This is not a rigorous benchmark, just a smoke test that a large
    input completes quickly and doesn't blow up memory/time
    unexpectedly (e.g., due to an accidental O(n^2) algorithm).
    """

    def test_expectancy_scales_linearly_enough_for_large_input(self):
        rng = random.Random(PROPERTY_TEST_SEED)
        large_trades = _random_trade_sequence(rng, 200_000)
        start = time.perf_counter()
        expectancy(large_trades)
        elapsed = time.perf_counter() - start
        # Generous ceiling: this should take well under a second on any
        # reasonable machine for a single-pass O(n) computation.
        assert elapsed < 5.0
