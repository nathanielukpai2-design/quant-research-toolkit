"""Unit tests for trade_stats.profit_factor."""

import pytest

from trade_stats.profit_factor import profit_factor


class TestProfitFactor:
    def test_normal_mixed_trades(self):
        assert profit_factor([10, -5, 20, -1]) == pytest.approx(5.0)

    def test_breakeven_when_profit_equals_loss(self):
        assert profit_factor([10, -10]) == pytest.approx(1.0)

    def test_no_losses_returns_infinity(self):
        assert profit_factor([1, 2, 3]) == float("inf")

    def test_no_wins_and_no_losses_returns_zero(self):
        assert profit_factor([0, 0, 0]) == pytest.approx(0.0)

    def test_all_losses_returns_zero(self):
        assert profit_factor([-1, -2, -3]) == pytest.approx(0.0)

    def test_single_trade_win(self):
        assert profit_factor([5]) == float("inf")

    def test_empty_raises_value_error(self):
        with pytest.raises(ValueError):
            profit_factor([])

    def test_invalid_type_raises_type_error(self):
        with pytest.raises(TypeError):
            profit_factor(42)

    def test_regression_breakeven_trades_excluded_from_terms(self):
        # Regression: ensure a breakeven trade (0) does not skew gross
        # profit or gross loss.
        assert profit_factor([10, -5, 0, 0]) == pytest.approx(2.0)
