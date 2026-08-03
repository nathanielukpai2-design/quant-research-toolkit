"""Unit tests for trade_stats.win_rate and trade_stats.loss_rate."""

import pytest

from trade_stats.loss_rate import loss_rate
from trade_stats.win_rate import win_rate


class TestWinRate:
    def test_normal_mixed_trades(self):
        assert win_rate([10, -5, 20, -1, 0]) == pytest.approx(0.4)

    def test_all_wins(self):
        assert win_rate([1, 2, 3]) == pytest.approx(1.0)

    def test_all_losses(self):
        assert win_rate([-1, -2, -3]) == pytest.approx(0.0)

    def test_all_breakeven(self):
        assert win_rate([0, 0, 0]) == pytest.approx(0.0)

    def test_boundary_epsilon_is_not_a_win(self):
        assert win_rate([1e-13, -1e-13]) == pytest.approx(0.0)

    def test_single_trade(self):
        assert win_rate([5]) == pytest.approx(1.0)

    def test_empty_raises_value_error(self):
        with pytest.raises(ValueError):
            win_rate([])

    def test_none_raises_type_error(self):
        with pytest.raises(TypeError):
            win_rate(None)

    def test_non_sequence_raises_type_error(self):
        with pytest.raises(TypeError):
            win_rate(123)

    def test_string_raises_type_error(self):
        with pytest.raises(TypeError):
            win_rate("123")

    def test_non_numeric_element_raises_type_error(self):
        with pytest.raises(TypeError):
            win_rate([1, "two", 3])

    def test_bool_element_raises_type_error(self):
        with pytest.raises(TypeError):
            win_rate([1, True, -3])

    def test_nan_raises_value_error(self):
        with pytest.raises(ValueError):
            win_rate([1.0, float("nan")])


class TestLossRate:
    def test_normal_mixed_trades(self):
        assert loss_rate([10, -5, 20, -1, 0]) == pytest.approx(0.4)

    def test_all_losses(self):
        assert loss_rate([-1, -2, -3]) == pytest.approx(1.0)

    def test_all_wins(self):
        assert loss_rate([1, 2, 3]) == pytest.approx(0.0)

    def test_win_rate_plus_loss_rate_with_breakeven(self):
        trades = [10, -5, 0]
        assert win_rate(trades) + loss_rate(trades) < 1.0

    def test_empty_raises_value_error(self):
        with pytest.raises(ValueError):
            loss_rate([])

    def test_invalid_type_raises_type_error(self):
        with pytest.raises(TypeError):
            loss_rate({"a": 1})
