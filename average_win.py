"""Average winning-trade calculation."""

import logging
from typing import Sequence

from ._validation import classify_trade, validate_trade_sequence

logger = logging.getLogger(__name__)


def average_win(trades: Sequence[float]) -> float:
    """Compute the average profit of winning trades.

    Args:
        trades: Sequence of trade profit/loss values, in the order the
            trades occurred. Must be non-empty.

    Returns:
        The arithmetic mean P&L of winning trades, as a non-negative
        float. Returns 0.0 if there are no winning trades.

    Raises:
        TypeError: If `trades` is not a sequence of numbers.
        ValueError: If `trades` is empty.

    Notes:
        Formula:
            average_win = sum(P&L for trades classified "win") / (count of "win")

        Breakeven trades (see `_validation.classify_trade`, using
        `math.isclose` per Engineering Manual §11) are excluded from
        both the numerator and denominator.

        Determinism (Engineering Manual §27): pure, order-independent
        reduction; no stochastic component; identical input always
        produces identical output.

        Logging (Engineering Manual §14): a warning is logged if there
        are no winning trades (an unusual-but-valid edge case); this
        never affects the returned value.

    Research Standards (Engineering Manual §26):
        Assumptions: Winning trades are independent, already-realized
            P&L observations in a consistent unit.
        Data source: Not applicable — general-purpose arithmetic
            definition with no fitted parameters.
        Validation period: Not applicable, for the same reason.
        Out-of-sample testing: Not applicable — no free parameters to
            overfit.
        Limitations: Sensitive to outliers with a small sample of
            winning trades; a single very large win can dominate the
            average and misrepresent typical performance.
        References: Standard trading-system evaluation metric.

    Example:
        >>> average_win([10, -5, 20, -1, 0])
        15.0
    """
    validate_trade_sequence(trades)
    wins = [pnl for pnl in trades if classify_trade(pnl) == "win"]
    if not wins:
        logger.warning("average_win: no winning trades among %d trade(s); returning 0.0", len(trades))
        return 0.0
    result = sum(wins) / len(wins)
    logger.debug("average_win: %d winning trade(s) -> %.6f", len(wins), result)
    return result
