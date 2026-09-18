"""Build a Kaggle ARC-AGI ``submission.json`` from a challenges file.

Input challenges format (Kaggle ARC Prize):
    { task_id: { "train": [{"input","output"}...], "test": [{"input"}...] }, ... }

Output submission format:
    { task_id: [ {"attempt_1": grid, "attempt_2": grid}, ... one per test input ], ... }
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from .solver import ArcSolver


def solve_challenges(challenges: dict) -> dict:
    solver = ArcSolver()
    submission: dict = {}
    solved = 0
    for task_id, task in challenges.items():
        preds = solver.solve_task(task)
        submission[task_id] = preds
        # Count as "solved" when a non-fallback program was found.
        if solver.search([(_g(p["input"]), _g(p["output"])) for p in task["train"]]) is not None:
            solved += 1
    submission["_meta_solved"] = solved  # convenience; removed by validate() if strict
    return submission


def _g(obj):
    from .dsl import to_grid

    return to_grid(obj)


def write_submission(challenges_path: str | Path, out_path: str | Path = "submission.json") -> dict:
    challenges = json.loads(Path(challenges_path).read_text())
    solver = ArcSolver()
    submission = {tid: solver.solve_task(task) for tid, task in challenges.items()}
    Path(out_path).write_text(json.dumps(submission))
    return submission


def validate_submission(submission: dict, challenges: dict) -> None:
    """Raise if the submission does not match the required shape."""
    for task_id, task in challenges.items():
        assert task_id in submission, f"missing task {task_id}"
        preds = submission[task_id]
        assert isinstance(preds, list) and len(preds) == len(task["test"]), f"{task_id}: one entry per test input"
        for entry in preds:
            assert "attempt_1" in entry and "attempt_2" in entry, f"{task_id}: needs attempt_1 & attempt_2"
            for key in ("attempt_1", "attempt_2"):
                grid = entry[key]
                assert isinstance(grid, list) and grid and all(isinstance(r, list) for r in grid), f"{task_id}.{key}: 2D grid"
                assert all(isinstance(v, int) and 0 <= v <= 9 for row in grid for v in row), f"{task_id}.{key}: colors 0-9"


if __name__ == "__main__":  # pragma: no cover
    import argparse

    ap = argparse.ArgumentParser(description="Generate an ARC-AGI submission.json")
    ap.add_argument("challenges", help="Path to *_challenges.json")
    ap.add_argument("-o", "--out", default="submission.json")
    args = ap.parse_args()
    start = time.time()
    sub = write_submission(args.challenges, args.out)
    print(f"Wrote {args.out} for {len(sub)} tasks in {time.time() - start:.2f}s")
