"""Unit tests for trade_stats.average_win and trade_stats.average_loss."""

import pytest

from trade_stats.average_loss import average_loss
from trade_stats.average_win import average_win


class TestAverageWin:
    def test_normal_mixed_trades(self):
        assert average_win([10, -5, 20, -1, 0]) == pytest.approx(15.0)

    def test_no_wins_returns_zero(self):
        assert average_win([-1, -2, -3]) == pytest.approx(0.0)

    def test_all_wins(self):
        assert average_win([2, 4, 6]) == pytest.approx(4.0)

    def test_single_win(self):
        assert average_win([7]) == pytest.approx(7.0)

    def test_breakeven_excluded(self):
        assert average_win([10, 0]) == pytest.approx(10.0)

    def test_empty_raises_value_error(self):
        with pytest.raises(ValueError):
            average_win([])

    def test_invalid_type_raises_type_error(self):
        with pytest.raises(TypeError):
            average_win(None)


class TestAverageLoss:
    def test_normal_mixed_trades(self):
        assert average_loss([10, -5, 20, -1, 0]) == pytest.approx(-3.0)

    def test_no_losses_returns_zero(self):
        assert average_loss([1, 2, 3]) == pytest.approx(0.0)

    def test_all_losses(self):
        assert average_loss([-2, -4, -6]) == pytest.approx(-4.0)

    def test_single_loss(self):
        assert average_loss([-9]) == pytest.approx(-9.0)

    def test_result_is_signed_not_absolute(self):
        assert average_loss([-3, -5]) < 0.0

    def test_empty_raises_value_error(self):
        with pytest.raises(ValueError):
            average_loss([])

    def test_invalid_type_raises_type_error(self):
        with pytest.raises(TypeError):
            average_loss("not-a-sequence")
