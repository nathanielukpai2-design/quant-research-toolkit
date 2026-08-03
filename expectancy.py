"""Expectancy (expected value per trade) calculation."""

import logging
from typing import Sequence

from ._validation import validate_trade_sequence
from .average_loss import average_loss
from .average_win import average_win
from .loss_rate import loss_rate
from .win_rate import win_rate

logger = logging.getLogger(__name__)


def expectancy(trades: Sequence[float]) -> float:
    """Compute the expectancy (expected P&L) per trade.

    Args:
        trades: Sequence of trade profit/loss values, in the order the
            trades occurred. Must be non-empty.

    Returns:
        The expected P&L per trade, in the same units as `trades`.

    Raises:
        TypeError: If `trades` is not a sequence of numbers.
        ValueError: If `trades` is empty.

    Notes:
        Formula:
            expectancy = (win_rate * average_win) + (loss_rate * average_loss)

        Since `average_loss` is returned as a signed (non-positive)
        value, this formula correctly nets the loss contribution
        without needing a subtraction. This value is mathematically
        equivalent to the arithmetic mean of `trades`, but is expressed
        via win rate / loss rate / average win / average loss to make
        the trade-off between win frequency and win/loss magnitude
        explicit, which is the standard presentation in trading-system
        evaluation.

        Determinism (Engineering Manual §27): composed entirely of the
        pure, order-independent reductions above; no stochastic
        component; identical input always produces identical output.

        Logging (Engineering Manual §14): a debug-level summary is
        logged; this never affects the returned value.

    Research Standards (Engineering Manual §26):
        Assumptions: Trades are independent, already-realized P&L
            observations in a consistent unit; past trade sequence is
            assumed representative of the distribution being
            estimated (a standard, and non-trivial, assumption for any
            expectancy figure).
        Data source: Not applicable — general-purpose arithmetic
            definition with no fitted parameters.
        Validation period: Not applicable, for the same reason.
        Out-of-sample testing: Not applicable — no free parameters to
            overfit. Note, however, that expectancy computed from a
            small in-sample trade log should still be treated as a
            noisy point estimate, not a guarantee of future edge.
        Limitations: A positive expectancy on a small sample can be
            entirely due to variance; expectancy does not account for
            position sizing, correlation between trades, or drawdown
            risk.
        References: Standard trading-system evaluation metric; see,
            e.g., Van Tharp, "Trade Your Way to Financial Freedom."

    Example:
        >>> expectancy([10, -5, 20, -1, 0])
        4.8
    """
    validate_trade_sequence(trades)
    wr = win_rate(trades)
    lr = loss_rate(trades)
    aw = average_win(trades)
    al = average_loss(trades)
    result = (wr * aw) + (lr * al)
    logger.debug(
        "expectancy: win_rate=%.6f avg_win=%.6f loss_rate=%.6f avg_loss=%.6f -> %.6f",
        wr, aw, lr, al, result,
    )
    return result
