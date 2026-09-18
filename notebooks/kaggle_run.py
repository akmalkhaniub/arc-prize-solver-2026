"""Kaggle ARC Prize entry point — offline, dependency-light (numpy only).

On Kaggle, the evaluation challenges live under /kaggle/input. This finds the
challenges file, solves every task, and writes /kaggle/working/submission.json.
Runs locally too (falls back to ./ and writes ./submission.json).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from arcsolver.submission import write_submission  # noqa: E402

CANDIDATES = [
    "/kaggle/input/arc-prize-2026/arc-agi_test_challenges.json",
    "/kaggle/input/arc-prize-2026/arc-agi_evaluation_challenges.json",
    "arc-agi_test_challenges.json",
]


def find_challenges() -> str | None:
    for c in CANDIDATES:
        if Path(c).exists():
            return c
    hits = list(Path("/kaggle/input").glob("**/*challenges*.json")) if Path("/kaggle/input").exists() else []
    return str(hits[0]) if hits else None


def main() -> int:
    src = find_challenges()
    if src is None:
        print("No challenges file found; nothing to do.")
        return 0
    out = "/kaggle/working/submission.json" if Path("/kaggle/working").exists() else "submission.json"
    start = time.time()
    sub = write_submission(src, out)
    print(f"Solved {len(sub)} tasks -> {out} in {time.time() - start:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
