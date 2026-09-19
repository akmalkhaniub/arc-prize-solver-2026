# 🧩 Neuro-Symbolic ARC Solver — ARC Prize 2026

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org)
[![NumPy](https://img.shields.io/badge/NumPy-program%20synthesis-013243.svg)](https://numpy.org)
[![Kaggle](https://img.shields.io/badge/Kaggle-ARC%20Prize%202026-20BEFF.svg)](https://www.kaggle.com/competitions)

> **Built for the [ARC Prize 2026](https://www.kaggle.com/competitions) (Kaggle code competition).**

A symbolic **program-synthesis** solver for ARC-AGI grid-reasoning tasks. For each task it
searches compositions of DSL primitives for a program that reproduces **every** training
pair exactly, then applies it to the test inputs — emitting the two attempts the
competition scores.

> **Note:** this project was rebuilt from an earlier Node.js prototype (kept under
> [`legacy-js/`](./legacy-js)) into the correct stack — a **Python** package that produces
> a Kaggle `submission.json`, which is what an ARC *code competition* actually requires.

## How it works

```
task.train pairs ─▶ ArcSolver.search
                     ├─ depth-1: try each DSL primitive (rotations, reflections,
                     │            transpose, gravity, crop, tile, colour swaps)
                     ├─ colour-map inference (consistent per-colour relabeling)
                     └─ depth-2: try every op2 ∘ op1 composition
                    keep the first program that is 100% consistent on training
task.test inputs ─▶ attempt_1 = program(test), attempt_2 = D4 fallback variant
```

The DSL (`arcsolver/dsl.py`) is pure NumPy; the search (`arcsolver/solver.py`) verifies
candidates against the demonstrations; `arcsolver/submission.py` builds and validates the
`{task_id: [{"attempt_1", "attempt_2"}, ...]}` submission structure.

## Run

```bash
pip install -r requirements-dev.txt && pip install -e .
pytest -q                                   # solver + submission-format tests

# Generate a submission from a challenges file:
python -m arcsolver.submission path/to/arc-agi_test_challenges.json -o submission.json
# Kaggle entry point (auto-discovers /kaggle/input, writes /kaggle/working):
python notebooks/kaggle_run.py
```

## Benchmark (measured)

`python -m arcsolver.benchmark` generates tasks per transformation family and reports exact-match solve-rate (the competition's criterion):

```
solve rate 0.857 (48/56)
  rotate180 8/8  reflect_h 8/8  transpose 8/8
  gravity_down 8/8  color_map 8/8  compose_recolor_rotate 8/8  hard_noise 0/8
```

Every DSL-expressible family is solved; the unlearnable `hard_noise` family is missed by design — the honest ceiling of a purely symbolic solver, and exactly why an LLM code-gen branch is the next lever. Benchmarked via `tests/test_benchmark.py`.

## Scope & honesty

This is a **symbolic** solver: it excels at tasks expressible as short DSL programs
(geometric transforms, recolourings, simple compositions) and returns a well-formed
two-attempt answer for every task, but it does **not** include the LLM code-generation
branch or test-time training that top ARC entries add — so it is a strong, fast baseline
rather than a leaderboard winner. It runs fully offline (NumPy only), well within Kaggle's
compute limits. Tests validate correctness on synthetic tasks and the exact submission
schema; real scoring happens on Kaggle's hidden set.
