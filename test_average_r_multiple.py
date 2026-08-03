"""Unit tests for trade_stats.average_r_multiple."""

import pytest

from trade_stats.average_r_multiple import average_r_multiple


class TestAverageRMultiple:
    def test_normal_mixed_r_multiples(self):
        assert average_r_multiple([2.0, -1.0, 1.5, -1.0]) == pytest.approx(0.375)

    def test_all_positive(self):
        assert average_r_multiple([1.0, 2.0, 3.0]) == pytest.approx(2.0)

    def test_all_negative(self):
        assert average_r_multiple([-1.0, -1.0, -1.0]) == pytest.approx(-1.0)

    def test_single_value(self):
        assert average_r_multiple([3.0]) == pytest.approx(3.0)

    def test_zero_r_multiple_included(self):
        assert average_r_multiple([0.0, 2.0]) == pytest.approx(1.0)

    def test_empty_raises_value_error(self):
        with pytest.raises(ValueError):
            average_r_multiple([])

    def test_invalid_type_raises_type_error(self):
        with pytest.raises(TypeError):
            average_r_multiple("2.0")

    def test_error_message_uses_parameter_name(self):
        with pytest.raises(ValueError, match="r_multiples"):
            average_r_multiple([])
