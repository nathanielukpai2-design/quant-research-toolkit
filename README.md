# Trade Stats

Production-quality Python library for deterministic trade performance statistics for quantitative trading systems.

Built to the standards defined in the Engineering Manual.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Why Trade Stats?

Trade performance metrics are the foundation of evaluating every quantitative trading strategy.

Trade Stats provides deterministic implementations of core trading statistics that can be integrated into:

- Quantitative research workflows
- Algorithmic trading systems
- Backtesting frameworks
- Portfolio analytics
- MT5 Expert Advisors
- Performance reporting pipelines

Every calculation is deterministic, fully documented, validated, tested, and designed for production use.

---

## Overview

Trade Stats is a production-quality Python library for computing deterministic trading performance metrics from realized trade profit and loss (P&L) data.

The library is designed around pure functions and reusable modules, allowing each metric to be used independently or integrated into larger quantitative research and trading systems.

Every public function is:

- Pure
- Deterministic
- Fully type hinted
- Fully documented
- Input validated
- Unit tested
- Production ready

---

## Features

### Trading Performance Metrics

- Win Rate
- Loss Rate
- Average Win
- Average Loss
- Profit Factor
- Expectancy
- Average R Multiple

### Engineering Features

- Pure Functional Design
- Shared Validation Framework
- Deterministic Calculations
- Comprehensive Documentation
- Numerical Precision Handling
- Centralized Configuration
- Logging Support
- Continuous Integration Ready

---

## Engineering Highlights

- Deterministic calculations
- Pure functional design
- Modular architecture
- Shared validation logic
- Numerical precision handling
- Comprehensive documentation
- Input validation
- Fully type hinted
- Unit tested
- Production ready

---

## Repository Structure

```text
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
│   ├── constants.py
│   └── defaults.py
├── trade_stats/
│   ├── __init__.py
│   ├── _validation.py
│   ├── win_rate.py
│   ├── loss_rate.py
│   ├── average_win.py
│   ├── average_loss.py
│   ├── profit_factor.py
│   ├── expectancy.py
│   └── average_r_multiple.py
└── tests/
```

---

## Installation

```bash
pip install -r requirements.txt
```

No third-party libraries are required to use Trade Stats.

Development dependencies are provided for testing, formatting, linting, type checking, and continuous integration.

---

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

trades = [10, -5, 20, -1, 0]

print(win_rate(trades))
print(loss_rate(trades))
print(average_win(trades))
print(average_loss(trades))
print(profit_factor(trades))
print(expectancy(trades))

r_multiples = [2.0, -1.0, 1.5, -1.0]

print(average_r_multiple(r_multiples))
```

Optional logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

---

## Testing

```bash
pytest

coverage run -m pytest

coverage report
```

Every module includes:

- Normal-case tests
- Boundary tests
- Empty input tests
- Invalid input tests
- Edge-case tests
- Regression tests
- Floating-point tolerance tests
- Property tests
- Performance tests

---

## Roadmap

- Add Sharpe Ratio
- Add Sortino Ratio
- Add Maximum Drawdown
- Add Calmar Ratio
- Add Recovery Factor
- Add Kelly Criterion
- Expand portfolio-level performance metrics

---

## Repository Ecosystem

Trade Stats is part of a larger quantitative trading software ecosystem.

Engineering Manual

↓

Trade Stats

↓

Feature Engine

↓

Risk Manager

↓

Backtesting Framework

↓

MT5 Expert Advisor

↓

Deterministic Trading Framework

---

## About the Author

Hi, I'm Ceejay.

I'm a Quantitative Trading Research Engineer building deterministic trading systems using Python and MQL5.

My work focuses on:

- Quantitative Trading Research
- Algorithmic Trading
- Feature Engineering
- Backtesting
- Risk Management
- MT5 Expert Advisors

Email:

nathanielukpai2@gmail.com

---

## License

See the repository LICENSE file.
