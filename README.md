# trade_stats

Deterministic trade-performance statistics for quantitative trading systems,
built to the standards of Engineering Manual v1.2.

**Version:** 2.1.0 (see [Changelog](#changelog))

## Overview

This repository computes standard trading-system evaluation metrics from a
sequence of realized trade profit/loss (P&L) values. Every public function is
pure, deterministic, fully type-hinted, validated, logged (per Engineering
Manual §14), and unit tested — including property, regression,
floating-point-tolerance, cross-validation, and performance tests (§15).

## Installation

```bash
pip install -r requirements.txt
```

No dependencies are required to *use* the library itself — `requirements.txt`
covers the development/CI tooling (pytest, ruff, black, mypy, coverage,
pre-commit).

## Folder structure

```
trade-stats/
│
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── .pre-commit-config.yaml
├── .gitignore
├── engineering-manual.md
│
├── .github/
│   └── workflows/
│       └── tests.yml
├── config/
│   ├── __init__.py
│   ├── constants.py          # TRADE_PNL_EPSILON, etc.
│   └── defaults.py           # reserved for future tunable defaults
├── trade_stats/
│   ├── __init__.py
│   ├── _validation.py        # shared validation + classify_trade()
│   ├── win_rate.py
│   ├── loss_rate.py
│   ├── average_win.py
│   ├── average_loss.py
│   ├── profit_factor.py
│   ├── expectancy.py
│   └── average_r_multiple.py
└── tests/
    ├── test_win_loss_rate.py
    ├── test_average_win_loss.py
    ├── test_profit_factor.py
    ├── test_expectancy.py
    ├── test_average_r_multiple.py
    └── test_properties_and_regression.py
```

Package name note (Engineering Manual §20): this package is named
`trade_stats`, not `statistics`, specifically to avoid shadowing Python's
standard-library `statistics` module.

## Usage

```python
from trade_stats import (
    win_rate,
    loss_rate,
    average_win,
    average_loss,
    profit_factor,
    expectancy,
    average_r_multiple,
)

trades = [10, -5, 20, -1, 0]  # P&L per trade

win_rate(trades)            # 0.4
loss_rate(trades)           # 0.4
average_win(trades)         # 15.0
average_loss(trades)        # -3.0  (signed, non-positive)
profit_factor(trades)       # 5.0
expectancy(trades)          # 4.8

r_multiples = [2.0, -1.0, 1.5, -1.0]
average_r_multiple(r_multiples)  # 0.375
```

Enable logging (optional; the library only emits log records, it never
configures handlers itself — Engineering Manual §14):

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Features

- **`win_rate` / `loss_rate`** — fraction of trades that were winners /
  losers. Breakeven trades (within `TRADE_PNL_EPSILON` of zero, checked with
  `math.isclose()`) count toward the total but not toward either rate.
- **`average_win` / `average_loss`** — mean P&L of winning / losing trades.
  `average_loss` is signed (non-positive); use `abs()` for magnitude.
- **`profit_factor`** — gross profit divided by gross loss magnitude. Returns
  `inf` when there are wins and no losses, `0.0` when there are no wins.
- **`expectancy`** — expected P&L per trade:
  `win_rate * average_win + loss_rate * average_loss`. Equivalent to the
  arithmetic mean of `trades` (cross-validated against `statistics.mean` in
  tests).
- **`average_r_multiple`** — arithmetic mean of a sequence of R-multiples
  (P&L expressed as a multiple of initial risk).

## Architecture (Engineering Manual §4)

- All seven metric modules are pure functions: no I/O, no file loading, no
  network calls, no mutation of arguments.
- Validation and trade classification logic is centralized in
  `trade_stats/_validation.py` — nothing is duplicated across modules.
- Tunable/fixed values are centralized in `config/`, not hard-coded in
  business logic.

## Numerical precision (Engineering Manual §11)

- `TRADE_PNL_EPSILON = 1e-12` (`config/constants.py`) is the single
  named tolerance used everywhere a P&L value must be compared "close
  enough" to zero, via `math.isclose(pnl, 0.0, abs_tol=TRADE_PNL_EPSILON)`.
- `profit_factor` explicitly documents and returns `float("inf")` rather
  than raising when gross loss is zero.
- All NaN inputs are rejected with a `ValueError`; there is no silent
  missing-data handling in this package.

## Research Standards & Determinism (Engineering Manual §26–27)

Each module's docstring documents Assumptions, Data source, Validation
period, Out-of-sample testing, Limitations, and References for that metric.
Since every function here is a parameter-free arithmetic definition (not a
fitted model or strategy), most of these fields are explicitly marked "Not
applicable" with a stated reason, rather than filled in with invented
detail — consistent with the Engineering Manual's instruction that "AI
should never invent requirements" (§23).

Every function is a pure, order-independent reduction: identical input
always produces identical output, there is no stochastic component, no
timestamp handling, and no dependence on dictionary/set ordering.

## Testing (Engineering Manual §15)

```bash
pytest
coverage run -m pytest && coverage report
```

Coverage includes, per module: normal inputs, boundary conditions
(the epsilon threshold), empty/invalid inputs, edge cases (all-win,
all-loss, all-breakeven), and package-wide property tests, numerical
regression tests, floating-point tolerance tests, cross-validation
against `statistics.mean`, and a performance smoke test on 200,000
trades. Property tests use a fixed random seed (Engineering Manual §27).

## Continuous Integration (Engineering Manual §16)

`.github/workflows/tests.yml` runs Black, Ruff, MyPy, Pytest, and Coverage
on every push and pull request across Python 3.9–3.12.

## Changelog

- **2.1.0** — Added logging (`logging.getLogger(__name__)` per module),
  moved the epsilon tolerance into `config/constants.py`, switched
  breakeven classification to `math.isclose()`, and added property /
  regression / tolerance / cross-validation / performance tests.
  **Minor**: no public signature, return value, or import path changed.
- **2.0.0** — Renamed package from `statistics` to `trade_stats` (import
  path change) and added Research Standards / Deterministic Research Rules
  documentation to every function. **Major**: the import path change breaks
  existing callers.
- **1.0.0** — Initial implementation as the `statistics` package.

## Roadmap

- Add Sharpe ratio, max drawdown, and Kelly fraction modules.
- Populate `config/defaults.py` once a module has genuinely tunable
  parameters (e.g., an annualization factor or risk-free rate).
- Add regression tests as real trading data surfaces new edge cases.

## License

See repository root `LICENSE` file.
