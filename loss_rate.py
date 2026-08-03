"""Loss rate calculation for a sequence of trades."""

import logging
from typing import Sequence

from ._validation import classify_trade, validate_trade_sequence

logger = logging.getLogger(__name__)


def loss_rate(trades: Sequence[float]) -> float:
    """Compute the loss rate of a sequence of trades.

    Args:
        trades: Sequence of trade profit/loss values, in the order the
            trades occurred. Must be non-empty.

    Returns:
        The loss rate as a float in the closed interval [0.0, 1.0].

    Raises:
        TypeError: If `trades` is not a sequence of numbers.
        ValueError: If `trades` is empty.

    Notes:
        Formula:
            loss_rate = (count of trades classified "loss") / (total trade count)

        A trade is classified "breakeven" (see `_validation.classify_trade`,
        using `math.isclose` per Engineering Manual §11) rather than
        "loss" when its P&L is within tolerance of zero. Consequently,
        `win_rate + loss_rate` may be strictly less than 1.0 when
        breakeven trades are present.

        Determinism (Engineering Manual §27): pure, order-independent
        reduction; no stochastic component; identical input always
        produces identical output.

        Logging (Engineering Manual §14): a debug-level summary is
        logged; this never affects the returned value.

    Research Standards (Engineering Manual §26):
        Assumptions: Each element of `trades` is an independent,
            already-realized P&L observation in a consistent unit.
        Data source: Not applicable — general-purpose arithmetic
            definition with no fitted parameters.
        Validation period: Not applicable, for the same reason.
        Out-of-sample testing: Not applicable — no free parameters to
            overfit.
        Limitations: Says nothing about loss magnitude; a low loss
            rate can still coincide with a small number of very large
            losses (see `average_loss`, `profit_factor`).
        References: Standard trading-system evaluation metric.

    Example:
        >>> loss_rate([10, -5, 20, -1, 0])
        0.4
    """
    validate_trade_sequence(trades)
    losses = sum(1 for pnl in trades if classify_trade(pnl) == "loss")
    result = losses / len(trades)
    logger.debug("loss_rate: %d/%d trades classified as losses -> %.6f", losses, len(trades), result)
    return result
