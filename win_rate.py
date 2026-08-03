"""Win rate calculation for a sequence of trades."""

import logging
from typing import Sequence

from ._validation import classify_trade, validate_trade_sequence

logger = logging.getLogger(__name__)


def win_rate(trades: Sequence[float]) -> float:
    """Compute the win rate of a sequence of trades.

    Args:
        trades: Sequence of trade profit/loss values (any consistent
            unit, e.g. currency or R-multiples), in the order the
            trades occurred. Must be non-empty.

    Returns:
        The win rate as a float in the closed interval [0.0, 1.0].

    Raises:
        TypeError: If `trades` is not a sequence of numbers.
        ValueError: If `trades` is empty.

    Notes:
        Formula:
            win_rate = (count of trades classified "win") / (total trade count)

        A trade is classified "breakeven" (see `_validation.classify_trade`,
        which uses `math.isclose` per Engineering Manual §11) rather
        than "win" when its P&L is within tolerance of zero. Breakeven
        trades are included in the denominator but not the numerator.

        Determinism (Engineering Manual §27): this function is a pure,
        order-independent reduction over `trades` — it has no
        stochastic component, no timestamp handling, and identical
        input always produces identical output.

        Logging (Engineering Manual §14): a debug-level summary is
        logged; this never affects the returned value.

    Research Standards (Engineering Manual §26):
        Assumptions: Each element of `trades` is an independent,
            already-realized P&L observation in a consistent unit;
            the metric makes no assumption about the distribution of
            P&L values.
        Data source: Not applicable. This is a general-purpose
            arithmetic definition with no fitted parameters and no
            association with a specific dataset.
        Validation period: Not applicable, for the same reason.
        Out-of-sample testing: Not applicable — there is nothing to
            overfit, since the function has no free parameters.
        Limitations: Win rate alone does not describe the magnitude of
            wins vs. losses; a high win rate with poor average
            win/loss magnitude (see `profit_factor`, `expectancy`) can
            still be an unprofitable system.
        References: Standard trading-system evaluation metric; see,
            e.g., Van Tharp, "Trade Your Way to Financial Freedom."

    Example:
        >>> win_rate([10, -5, 20, -1, 0])
        0.4
    """
    validate_trade_sequence(trades)
    wins = sum(1 for pnl in trades if classify_trade(pnl) == "win")
    result = wins / len(trades)
    logger.debug("win_rate: %d/%d trades classified as wins -> %.6f", wins, len(trades), result)
    return result
