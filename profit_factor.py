"""Profit factor calculation for a sequence of trades."""

import logging
from typing import Sequence

from ._validation import classify_trade, validate_trade_sequence

logger = logging.getLogger(__name__)


def profit_factor(trades: Sequence[float]) -> float:
    """Compute the profit factor of a sequence of trades.

    Args:
        trades: Sequence of trade profit/loss values, in the order the
            trades occurred. Must be non-empty.

    Returns:
        The profit factor as a non-negative float. Returns
        ``float("inf")`` when there are winning trades but no losing
        trades. Returns 0.0 when there are neither winning nor losing
        trades (all breakeven).

    Raises:
        TypeError: If `trades` is not a sequence of numbers.
        ValueError: If `trades` is empty.

    Notes:
        Formula:
            profit_factor = (gross profit) / abs(gross loss)
            gross profit = sum(P&L for trades classified "win")
            gross loss   = sum(P&L for trades classified "loss")

        A profit factor > 1.0 indicates gross profits exceed gross
        losses; a value of exactly 1.0 indicates breakeven performance.
        Breakeven trades (see `_validation.classify_trade`, using
        `math.isclose` per Engineering Manual §11) contribute to
        neither term.

        Per Engineering Manual §11 (Infinite value handling), the
        `float("inf")` result documented above is an explicit,
        intentional return value, not an error condition.

        Determinism (Engineering Manual §27): pure, order-independent
        reduction; no stochastic component; identical input always
        produces identical output.

        Logging (Engineering Manual §14): a warning is logged when the
        result is infinite or zero (edge cases worth surfacing); this
        never affects the returned value.

    Research Standards (Engineering Manual §26):
        Assumptions: Trades are independent, already-realized P&L
            observations in a consistent unit; costs (spread,
            commission, slippage) are assumed to already be reflected
            in each P&L value.
        Data source: Not applicable — general-purpose arithmetic
            definition with no fitted parameters.
        Validation period: Not applicable, for the same reason.
        Out-of-sample testing: Not applicable — no free parameters to
            overfit.
        Limitations: Unbounded above and undefined in magnitude when
            gross loss is 0 (returns `inf`); should not be used alone
            to compare systems with very different trade counts, since
            a small sample can produce an extreme profit factor that
            is not representative of long-run performance.
        References: Standard trading-system evaluation metric.

    Example:
        >>> profit_factor([10, -5, 20, -1])
        5.0
    """
    validate_trade_sequence(trades)
    gross_profit = sum(pnl for pnl in trades if classify_trade(pnl) == "win")
    gross_loss = abs(sum(pnl for pnl in trades if classify_trade(pnl) == "loss"))
    if gross_loss == 0.0:
        if gross_profit > 0.0:
            logger.warning("profit_factor: zero gross loss with positive gross profit; returning inf")
            return float("inf")
        logger.warning("profit_factor: zero gross profit and zero gross loss; returning 0.0")
        return 0.0
    result = gross_profit / gross_loss
    logger.debug("profit_factor: gross_profit=%.6f gross_loss=%.6f -> %.6f", gross_profit, gross_loss, result)
    return result
