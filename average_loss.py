"""Average losing-trade calculation."""

import logging
from typing import Sequence

from ._validation import classify_trade, validate_trade_sequence

logger = logging.getLogger(__name__)


def average_loss(trades: Sequence[float]) -> float:
    """Compute the average loss of losing trades.

    Args:
        trades: Sequence of trade profit/loss values, in the order the
            trades occurred. Must be non-empty.

    Returns:
        The arithmetic mean P&L of losing trades, as a non-positive
        float (i.e., zero or negative). Returns 0.0 if there are no
        losing trades.

    Raises:
        TypeError: If `trades` is not a sequence of numbers.
        ValueError: If `trades` is empty.

    Notes:
        Formula:
            average_loss = sum(P&L for trades classified "loss") / (count of "loss")

        The result is returned as a negative number (the actual signed
        average), not its absolute value. Callers that need the loss
        magnitude should take ``abs(average_loss(trades))``. Changing
        this return convention to an absolute value in the future
        would be a **Major** version change (Engineering Manual §25),
        since it breaks the documented contract relied upon by
        `expectancy`. Breakeven trades (see `_validation.classify_trade`,
        using `math.isclose` per Engineering Manual §11) are excluded
        from both the numerator and denominator.

        Determinism (Engineering Manual §27): pure, order-independent
        reduction; no stochastic component; identical input always
        produces identical output.

        Logging (Engineering Manual §14): a warning is logged if there
        are no losing trades (an unusual-but-valid edge case); this
        never affects the returned value.

    Research Standards (Engineering Manual §26):
        Assumptions: Losing trades are independent, already-realized
            P&L observations in a consistent unit.
        Data source: Not applicable — general-purpose arithmetic
            definition with no fitted parameters.
        Validation period: Not applicable, for the same reason.
        Out-of-sample testing: Not applicable — no free parameters to
            overfit.
        Limitations: Sensitive to outliers with a small sample of
            losing trades; a single very large loss can dominate the
            average.
        References: Standard trading-system evaluation metric.

    Example:
        >>> average_loss([10, -5, 20, -1, 0])
        -3.0
    """
    validate_trade_sequence(trades)
    losses = [pnl for pnl in trades if classify_trade(pnl) == "loss"]
    if not losses:
        logger.warning("average_loss: no losing trades among %d trade(s); returning 0.0", len(trades))
        return 0.0
    result = sum(losses) / len(losses)
    logger.debug("average_loss: %d losing trade(s) -> %.6f", len(losses), result)
    return result
