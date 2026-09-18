# Changelog

## [Unreleased]

### Rebuilt in Python for Kaggle (2026-09-18)
An ARC *code competition* is scored by a notebook that emits `submission.json`, so the
project was rebuilt from the Node prototype (preserved under `legacy-js/`) into a Python
package that produces and validates that submission.

### Added
- `arcsolver/` package: `dsl.py` (NumPy grid primitives), `solver.py` (depth-1/-2 program
  synthesis + colour-map inference, two-attempt output), `submission.py` (build + validate
  Kaggle ARC-AGI `submission.json`).
- `notebooks/kaggle_run.py` — offline Kaggle entry point (auto-discovers challenges under
  `/kaggle/input`, writes `/kaggle/working/submission.json`).
- `tests/test_arcsolver.py` — 6 pytest cases: rotation/reflection/depth-2 composition,
  colour-map inference, unsolved fallback, and submission-schema validation.
- `pyproject.toml`, `requirements*.txt`, CI on Python 3.10–3.12.

### Notes
- Symbolic solver only (no LLM code-gen / test-time training), so it is a fast, correct
  baseline rather than a leaderboard winner. Runs offline with NumPy alone.
