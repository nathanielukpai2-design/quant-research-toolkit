"""Private input-validation and classification helpers for `trade_stats`.

This module is internal (leading underscore) and is not part of the
public API. It exists so that input-validation and trade-classification
rules are defined once and reused consistently across every public
function in this package, per Engineering Manual §2 ("No duplicated
business logic").

Determinism (Engineering Manual §27): this module has no stochastic
component, no timestamp handling, and does not depend on dictionary or
set ordering — it only iterates over the sequence supplied by the
caller, in the order given. Logging calls below never alter control
flow or return values (Engineering Manual §14).
"""

import logging
import math
from typing import Literal, Sequence

from config.constants import TRADE_PNL_EPSILON

logger = logging.getLogger(__name__)

# Re-exported for backward compatibility with callers/tests that import
# EPSILON directly from this module.
EPSILON: float = TRADE_PNL_EPSILON

TradeClassification = Literal["win", "loss", "breakeven"]


def validate_trade_sequence(values: Sequence[float], name: str = "trades") -> None:
    """Validate a sequence of numeric trade values.

    Args:
        values: Sequence of numeric values (e.g., trade P&L or
            R-multiples) to validate.
        name: Name of the parameter being validated, used to produce
            clear, specific error messages.

    Returns:
        None.

    Raises:
        TypeError: If `values` is None, is not a sequence, is a string
            or bytes object, or contains any element that is not an
            ``int`` or ``float`` (booleans are rejected).
        ValueError: If `values` is empty, or contains a NaN value.

    Notes:
        Strings and bytes are explicitly rejected even though they are
        technically ``Sequence`` instances, since iterating over them
        would yield characters rather than numbers. Booleans are
        rejected even though ``bool`` is a subclass of ``int``, since a
        boolean trade value is almost certainly a caller error.

        Per Engineering Manual §11 (NaN handling policy), NaN is always
        rejected: this package has no documented use for missing data.

    Example:
        >>> validate_trade_sequence([1.0, -2.0, 3.0])
        >>> validate_trade_sequence([])
        Traceback (most recent call last):
            ...
        ValueError: trades must not be empty.
    """
    if values is None:
        logger.error("%s validation failed: value is None", name)
        raise TypeError(f"{name} must not be None.")
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        logger.error(
            "%s validation failed: expected a sequence, got %s",
            name,
            type(values).__name__,
        )
        raise TypeError(
            f"{name} must be a sequence (e.g., list or tuple) of numbers, "
            f"got {type(values).__name__}."
        )
    if len(values) == 0:
        logger.error("%s validation failed: sequence is empty", name)
        raise ValueError(f"{name} must not be empty.")
    for index, value in enumerate(values):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            logger.error(
                "%s validation failed at index %d: got %s",
                name,
                index,
                type(value).__name__,
            )
            raise TypeError(
                f"{name}[{index}] must be an int or float, "
                f"got {type(value).__name__}."
            )
        if value != value:  # NaN is the only value that is not equal to itself.
            logger.error("%s validation failed at index %d: NaN", name, index)
            raise ValueError(f"{name}[{index}] must not be NaN.")
    logger.debug("%s validated: %d element(s)", name, len(values))


def classify_trade(pnl: float, epsilon: float = TRADE_PNL_EPSILON) -> TradeClassification:
    """Classify a single trade P&L value as a win, loss, or breakeven.

    Args:
        pnl: The trade's profit/loss value.
        epsilon: Absolute tolerance used to treat `pnl` as zero. Defaults
            to `TRADE_PNL_EPSILON` from `config.constants`.

    Returns:
        `"win"` if `pnl` is greater than zero (outside tolerance),
        `"loss"` if `pnl` is less than zero (outside tolerance), or
        `"breakeven"` if `pnl` is within `epsilon` of zero.

    Notes:
        Per Engineering Manual §11, this uses `math.isclose()` rather
        than exact equality to decide whether `pnl` is "close enough"
        to zero to be considered breakeven.

    Example:
        >>> classify_trade(10.0)
        'win'
        >>> classify_trade(-5.0)
        'loss'
        >>> classify_trade(1e-13)
        'breakeven'
    """
    if math.isclose(pnl, 0.0, abs_tol=epsilon):
        return "breakeven"
    return "win" if pnl > 0.0 else "loss"
