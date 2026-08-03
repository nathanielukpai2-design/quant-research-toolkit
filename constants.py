"""Fixed, non-tunable constants shared across the repository.

Per Engineering Manual §7 (Configuration Standards) and §11
(Numerical Precision Standards): every floating-point tolerance used
in business logic must be a named constant defined here, never an
inline unexplained literal.
"""

# Absolute tolerance used when classifying a trade P&L value as a win,
# loss, or breakeven, and more generally whenever a value must be
# compared "close enough" to zero. Chosen to be far smaller than any
# realistic trade P&L (e.g., fractions of a cent) while still absorbing
# ordinary floating-point representation error.
TRADE_PNL_EPSILON: float = 1e-12
