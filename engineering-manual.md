# Engineering Manual v1.2

## 1. Mission Statement

### Objective

Develop production-quality quantitative finance software that is:

- Deterministic
- Well documented
- Fully tested
- Modular
- Reproducible
- Easy to maintain
- Suitable for open-source publication and professional portfolios

The goal is to build software that demonstrates professional software engineering and quantitative research practices.

## 2. Core Engineering Principles

Every project must follow these principles:

- Correctness before optimization.
- Readability before cleverness.
- Deterministic outputs for identical inputs.
- No duplicated business logic.
- Small, focused modules.
- Every public function must be documented.
- Every public function must be tested.
- Every algorithm must have clearly defined inputs and outputs.
- Every mathematical formula must be documented.
- Production quality over development speed.

## 3. Repository Structure Standard

Every repository should follow this structure:

```
project_name/
│
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── .pre-commit-config.yaml
├── .gitignore
│
├── .github/
│   └── workflows/
│       └── tests.yml
├── config/
│   ├── constants.py
│   └── defaults.py
├── docs/
├── src/
├── tests/
├── examples/
├── data/
├── notebooks/
└── assets/
```

## 4. Architecture Standards

*(New in v1.2)*

- Separate business logic from I/O. Functions that compute a result must not also read files, hit a network, or print to stdout.
- Never mix calculations with file loading. A "load data" function and a "compute metric" function are always distinct.
- Keep pure functions pure: given the same inputs, always return the same outputs, with no side effects and no mutation of arguments.
- Configuration belongs in configuration files (see §7 Configuration Standards), not hard-coded inside business logic.
- Use dependency injection where appropriate — pass collaborators (data sources, clocks, random generators) in as parameters rather than importing/instantiating them inside a function.
- One responsibility per module. If a module needs "and" in its one-sentence description, split it.

## 5. Python Coding Standards

All Python code must:

- Follow PEP 8.
- Use descriptive variable names.
- Use meaningful function names.
- Keep functions focused on a single responsibility.
- Avoid global mutable state.
- Avoid duplicated logic.

## 6. Type Hint Policy

Every public function must include type hints.

Example:

```python
def win_rate(trades: Sequence[float]) -> float:
```

Avoid using `Any` unless absolutely necessary.

## 7. Configuration Standards

*(New in v1.2)*

- Configuration lives in a dedicated `config/` package, not scattered across business-logic modules.
  - `config/constants.py` — fixed, non-tunable definitions (e.g., epsilon thresholds, physical/mathematical constants).
  - `config/defaults.py` — tunable default parameters that a caller may reasonably override (e.g., default lookback windows).
- No magic numbers in business logic: any literal with domain meaning is named and imported from `config/`.
- Constants are written in `UPPERCASE_WITH_UNDERSCORES`.
- Never scatter equivalent configuration values across multiple modules; a value belongs in exactly one place.

## 8. Documentation Standard

Every public function must include:

- Summary
- Parameters
- Returns
- Raises
- Notes
- Mathematical formula (if applicable)
- Example usage

Choose one docstring style (Google, NumPy, or reStructuredText) and use it consistently across all repositories.

## 9. Input Validation

Every public function must validate:

- Input type
- Empty inputs
- Invalid values
- Missing values (where applicable)

Fail fast with clear, informative exceptions.

## 10. Error Handling

- Never fail silently.
- Use meaningful exceptions with descriptive messages.
- Document every exception that can be raised.

## 11. Numerical Precision Standards

*(New in v1.2)*

Financial software requires explicit numerical rules:

- **Floating-point comparisons** must use an explicit tolerance (`math.isclose()` or a named epsilon constant from `config/constants.py`) rather than `==`.
- **NaN handling policy**: functions must explicitly reject NaN inputs (raise `ValueError`) unless the function's documented purpose is to handle missing data, in which case the handling must be spelled out in the docstring.
- **Infinite value handling**: any function that can mathematically produce an infinite result (e.g., a ratio with a zero denominator) must document when this occurs and return `float("inf")`/`float("-inf")` explicitly rather than raising or returning a sentinel like `-1`.
- **Rounding policy**: functions return full floating-point precision; rounding for display is the caller's responsibility unless a function's explicit purpose is formatting/reporting.
- **Explicit epsilon constants**: every tolerance value must be a named constant, documented with its purpose, never an inline unexplained literal.

## 12. Mathematical Standards

Every statistical or financial calculation must include:

- Formula
- Assumptions
- Units
- References (if appropriate)

No "magic numbers" — define constants with meaningful names (see §7 Configuration Standards).

## 13. Performance Standards

For each algorithm, document:

- Time complexity
- Space complexity

Optimize only after correctness has been verified.

## 14. Logging Standards

*(New in v1.2)*

- Use Python's `logging` module; never use `print()` in library code.
- Each module that logs obtains its own logger via `logging.getLogger(__name__)`.
- Log important events: validation failures before raising, unusual-but-valid edge cases (e.g., a ratio hitting infinity), and any fallback behavior.
- Separate log levels by purpose: `DEBUG` for internal computation detail, `INFO` for normal significant events, `WARNING` for unusual-but-recoverable situations, `ERROR` for failures.
- Logging must never change program behavior. A calculation must produce identical results whether or not logging is enabled, and at any log level (Engineering Manual §27 Determinism applies to logging too).
- Libraries do not configure logging handlers or levels themselves (no `logging.basicConfig()` in library code) — that is the application/caller's responsibility.

## 15. Testing Standard

Every module must have corresponding unit tests. Minimum coverage includes:

- Normal inputs
- Boundary conditions
- Empty inputs
- Invalid inputs
- Edge cases
- Regression tests for fixed bugs

For quantitative libraries specifically, also require:

- **Property tests** where appropriate (e.g., "win_rate + loss_rate + breakeven_rate always equals 1.0", checked across many generated inputs).
- **Numerical regression tests** that pin a known input/output pair so future changes cannot silently alter results.
- **Floating-point tolerance tests** using `math.isclose()` rather than exact equality.
- **Performance benchmarks** for any algorithm whose time/space complexity is documented as worse than linear.
- **Cross-validation** against a known analytical result or an independent reference implementation (e.g., comparing an expectancy calculation against the plain arithmetic mean of the same data).

Tests should be automated, repeatable, and — per Engineering Manual §27 — deterministic (any randomized/property-style test must use a fixed seed).

## 16. Continuous Integration

*(New in v1.2)*

Every repository runs a CI pipeline (e.g., `.github/workflows/tests.yml`) that, on every push and pull request:

1. Installs dependencies.
2. Runs formatting checks (Black).
3. Runs linting (Ruff).
4. Runs static type checking (MyPy).
5. Runs the full test suite (Pytest).
6. Reports coverage (Coverage.py).

A pull request may not be merged if any of these steps fail.

## 17. Code Quality Tools

*(New in v1.2)*

Standard tooling across all repositories:

| Purpose | Tool |
|---|---|
| Linting | Ruff |
| Formatting | Black |
| Type checking | MyPy |
| Testing | Pytest |
| Coverage | Coverage.py |
| Git hooks | Pre-commit |

Tool configuration lives in `pyproject.toml` (and `.pre-commit-config.yaml` for hooks) so behavior is identical locally and in CI.

## 18. Security Standards

*(New in v1.2)*

Even research repositories follow basic security hygiene:

- Never commit secrets or API keys. Use `.env` files (git-ignored) for local credentials.
- Validate all external inputs (this is also required generally by §9, but applies with extra weight to anything crossing a trust boundary — file uploads, network responses, broker API payloads).
- Pin dependency versions where appropriate (`requirements.txt` / `pyproject.toml` lockfile) so a compromised or broken upstream release cannot silently change behavior.
- `.gitignore` must exclude `.env`, credential files, and any local secrets by default in every repository, from the first commit.

## 19. Repository Documentation

Every repository must contain:

- Project overview
- Installation instructions
- Usage examples
- Folder structure
- Features
- Roadmap
- License
- Contributing guide (if applicable)

## 20. Repository Naming Convention

*(New in v1.2)*

- Use lowercase, hyphenated names for repository/project directories (e.g., `trade-stats`, `feature-engine`, `risk-manager`, `portfolio-engine`, `walk-forward`, `backtester`).
- Use lowercase, underscored names for importable Python packages within a repository (e.g., `trade_stats/`), since hyphens are not valid in Python identifiers.
- Never choose a package name that shadows a Python standard-library module (e.g., `statistics`, `types`, `queue`, `random`). Check `import <name>` against the standard library before naming any new package.
- Prefer descriptive, specific names (`trade_stats`, `quant_stats`) over generic ones that invite collisions (`stats`, `utils`, `helpers`) as a project grows.

## 21. Git Workflow

- Make small, focused commits.
- Write meaningful commit messages.
- Keep the main branch stable.
- Use feature branches for major work (recommended as projects grow).

Example commit messages:

```
feat: add win rate calculation
fix: handle empty trade list
test: add unit tests for profit factor
docs: update README examples
```

## 22. Code Review Checklist

Before accepting any code, verify:

- Correctness
- Readability
- Type hints
- Documentation
- Tests
- Input validation
- Error handling
- PEP 8 compliance
- Performance considerations
- Configuration (no magic numbers; constants sourced from `config/`)
- Logging (no `print()`; appropriate log levels)
- Security (no secrets committed; external inputs validated)

## 23. AI Development Workflow

When using Claude, ChatGPT, or another coding assistant:

- Provide the Engineering Manual.
- Provide the repository structure.
- Describe the module to implement.
- Request production-ready code only.
- Request corresponding unit tests.
- Review the output before committing.

AI should never invent requirements. If something is ambiguous, it should ask for clarification.

## 24. Release Checklist

Before each release:

- All tests pass (including CI, §16).
- Documentation is updated.
- README reflects current functionality.
- Examples are verified.
- Version number is updated per §25 Semantic Versioning Policy.
- Changelog is written.

## 25. Semantic Versioning Policy

All repositories follow semantic versioning: `MAJOR.MINOR.PATCH`.

| Segment | Meaning | Example |
|---|---|---|
| **Major** | Breaking changes — public API signatures change, return semantics change, package/import paths change, or existing behavior is removed/altered in an incompatible way. | Renaming the `statistics` package to `trade_stats` (import path change); changing `average_loss` to return an absolute value instead of a signed value. |
| **Minor** | New features — new public functions, modules, or optional parameters added in a backward-compatible way; new documentation standards applied to existing code without changing behavior. | Adding a new `sharpe_ratio` module; adding Research Standards documentation to existing functions. |
| **Patch** | Bug fixes — corrections to incorrect behavior that do not change the public API's documented contract. | Fixing an off-by-one error in a boundary check. |

Rules:

- Increment exactly one segment per release: bumping Major resets Minor and Patch to 0; bumping Minor resets Patch to 0.
- A change is Major if it breaks any documented input/output contract or import path, even if the internal fix is small.
- A change is Minor if it is purely additive and every existing caller continues to work unmodified.
- A change is Patch if it only corrects behavior to match the documented contract (i.e., the bug was a deviation from spec, not a spec change).
- Every version bump must be recorded in the repository changelog, matched against the Release Checklist (§24).

## 26. Research Standards

Because this is quantitative research software, every strategy, signal, or statistical metric — not just implementation code — must document:

- **Assumptions** — what must be true about the data or market for this metric/strategy to be valid (e.g., stationarity, independence, minimum sample size).
- **Data source** — what dataset, timeframe, and instrument the metric/strategy was built and tested against.
- **Validation period** — the exact date range(s) used for in-sample development.
- **Out-of-sample testing** — whether and how the metric/strategy was validated against data not used in development, and the result.
- **Limitations** — known failure modes, regimes where the metric/strategy is expected to underperform or be invalid, and any statistical caveats (e.g., small sample size, multiple-comparison risk).
- **References** — literature, canonical definitions, or prior internal research this is grounded in.

This documentation lives alongside the mathematical formula required by §12, and is what makes a repository suitable for professional/academic review rather than just code review.

## 27. Deterministic Research Rules

*(Especially important for this line of work)*

- **Random seeds must be fixed.** Any process with a stochastic component (bootstrap resampling, clustering initialization, simulation) must accept and document an explicit seed, and default to a fixed constant rather than an unseeded random state.
- **Identical inputs must produce identical outputs.** No hidden state, no reliance on wall-clock time, global counters, or environment variables inside a calculation.
- **Timezone handling must be explicit.** Any function that consumes or produces timestamps must document the assumed timezone (or require timezone-aware inputs) rather than relying on the caller's or system's local time.
- **Data ordering must be deterministic.** Sorting, grouping, and iteration order must be explicitly defined (e.g., sort by timestamp ascending, tie-break by a documented secondary key) rather than left to incidental input order.
- **Never depend on dictionary ordering or other implementation details.** Code must not rely on hash-map iteration order, set ordering, or other language/runtime implementation details to produce correct or reproducible results.

Violating any of these turns a "reproducible research" repository into one where results cannot be trusted or re-derived — this is treated as seriously as a correctness bug.

## 28. Portfolio Quality Standard

Every repository should demonstrate:

- Professional documentation
- Clean architecture
- High test quality
- Reusable code
- Consistent style
- Maintainability

Someone visiting the repository should immediately understand what it does, how to use it, and see evidence of engineering discipline.

## Versioning

Treat this manual as a living document. Version it using the Semantic Versioning Policy in §25.

- **v1.0** — Initial standards.
- **v1.1** — Added Semantic Versioning Policy, Research Standards, and Deterministic Research Rules. Minor bump: purely additive.
- **v1.2** — Added Architecture Standards, Numerical Precision Standards, Logging Standards, Configuration Standards, Continuous Integration, Code Quality Tools, Security Standards, expanded Testing Standard, and Repository Naming Convention; renumbered sections accordingly. Minor bump: purely additive — no existing standard was removed or made incompatible, only renumbered and expanded.

Update it when you make deliberate improvements to your engineering practices, rather than changing it for every project.
