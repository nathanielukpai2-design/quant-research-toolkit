"""Tunable default parameters shared across the repository.

Per Engineering Manual §7 (Configuration Standards): tunable
parameters that a caller may reasonably override belong here rather
than being hard-coded inside business logic.

The `trade_stats` module currently exposes no tunable parameters (its
metrics are parameter-free arithmetic definitions) — this file is kept
as the designated location for future defaults (e.g., a configurable
risk-free rate for a future `sharpe_ratio` module), per the repository
structure standard in Engineering Manual §3.
"""
