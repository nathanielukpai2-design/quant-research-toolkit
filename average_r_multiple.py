"""Average R-multiple calculation."""

import logging
from typing import Sequence

from ._validation import validate_trade_sequence

logger = logging.getLogger(__name__)


def average_r_multiple(r_multiples: Sequence[float]) -> float:
    """Compute the average R-multiple across a sequence of trades.

    An R-multiple expresses a trade's profit or loss as a multiple of
    the initial risk taken on that trade. For example, a trade risking
    $100 that made $250 has an R-multiple of 2.5.

    Args:
        r_multiples: Sequence of R-multiple values, one per trade, in
            the order the trades occurred. Must be non-empty.

    Returns:
        The arithmetic mean R-multiple.

    Raises:
        TypeError: If `r_multiples` is not a sequence of numbers.
        ValueError: If `r_multiples` is empty.

    Notes:
        Formula:
            average_r_multiple = sum(r_multiples) / len(r_multiples)

        Unlike `average_win`/`average_loss`, this function does not
        separate winners from losers: it averages every value it is
        given, since the R-multiple framework is typically applied to
        an entire trade sequence at once.

        Determinism (Engineering Manual §27): pure, order-independent
        reduction; no stochastic component; identical input always
        produces identical output.

        Logging (Engineering Manual §14): a debug-level summary is
        logged; this never affects the returned value.

    Research Standards (Engineering Manual §26):
        Assumptions: Each R-multiple was computed against a
            consistently-defined initial risk (e.g., stop-loss
            distance at entry); mixing R-multiples computed under
            different risk definitions will silently produce a
            meaningless average.
        Data source: Not applicable — general-purpose arithmetic
            definition with no fitted parameters.
        Validation period: Not applicable, for the same reason.
        Out-of-sample testing: Not applicable — no free parameters to
            overfit.
        Limitations: Like `expectancy`, this is a point estimate that
            is noisy on small samples and says nothing about the
            variance or drawdown profile of the underlying returns.
        References: Standard R-multiple framework; see, e.g., Van
            Tharp, "Trade Your Way to Financial Freedom."

    Example:
        >>> average_r_multiple([2.0, -1.0, 1.5, -1.0])
        0.375
    """
    validate_trade_sequence(r_multiples, name="r_multiples")
    result = sum(r_multiples) / len(r_multiples)
    logger.debug("average_r_multiple: %d value(s) -> %.6f", len(r_multiples), result)
    return result
