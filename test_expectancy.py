"""Unit tests for trade_stats.expectancy."""

import pytest

from trade_stats.expectancy import expectancy


class TestExpectancy:
    def test_normal_mixed_trades(self):
        assert expectancy([10, -5, 20, -1, 0]) == pytest.approx(4.8)

    def test_equivalent_to_arithmetic_mean_no_breakeven(self):
        trades = [10, -5, 20, -1]
        assert expectancy(trades) == pytest.approx(sum(trades) / len(trades))

    def test_all_wins(self):
        assert expectancy([2, 4, 6]) == pytest.approx(4.0)

    def test_all_losses(self):
        assert expectancy([-2, -4, -6]) == pytest.approx(-4.0)

    def test_all_breakeven(self):
        assert expectancy([0, 0, 0]) == pytest.approx(0.0)

    def test_single_trade(self):
        assert expectancy([5]) == pytest.approx(5.0)

    def test_empty_raises_value_error(self):
        with pytest.raises(ValueError):
            expectancy([])

    def test_invalid_type_raises_type_error(self):
        with pytest.raises(TypeError):
            expectancy(3.14)
