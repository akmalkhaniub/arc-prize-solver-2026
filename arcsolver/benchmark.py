"""Measurable solve-rate benchmark for the ARC solver on generated tasks.

Generates tasks from known transformations (grouped by family), runs the solver, and
reports the fraction whose attempt_1 exactly matches the held-out test output — the
same exact-match criterion the competition uses. Also includes non-DSL "hard" tasks to
show the honest ceiling of a purely symbolic solver.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np

from . import dsl
from .solver import ArcSolver


def _rand_grid(rng: random.Random, h: int, w: int, colors: int = 4) -> list[list[int]]:
    return [[rng.randint(0, colors) for _ in range(w)] for _ in range(h)]


@dataclass
class BenchmarkResult:
    total: int
    solved: int
    solve_rate: float
    by_family: dict[str, tuple[int, int]]  # family -> (solved, total)


# family name -> transform applied to build (input, output) pairs
_FAMILIES = {
    "rotate180": lambda g: dsl.rotate180(g),
    "reflect_h": lambda g: dsl.reflect_h(g),
    "transpose": lambda g: dsl.transpose(g),
    "gravity_down": lambda g: dsl.gravity_down(g),
    "color_map": lambda g: dsl.apply_color_map(g, {1: 3, 2: 4}),
    "compose_recolor_rotate": lambda g: dsl.replace_color(dsl.rotate90(g), 4, 3),
    # New primitive families (scale / mirror / halves).
    "scale2": lambda g: dsl.scale2(g),
    "concat_h_mirror": lambda g: dsl.concat_h_mirror(g),
    "top_half": lambda g: dsl.top_half(g),
    "swap_two_most_common": lambda g: dsl.swap_two_most_common(g),
    "symmetrize_h": lambda g: dsl.symmetrize_h(g),
    # Depth-3 composition: scale2 -> rotate180 -> mirror-concat.
    "compose3": lambda g: dsl.concat_h_mirror(dsl.rotate180(dsl.scale2(g))),
    # Hard: depends on grid content in a way the DSL can't express (random relabel per task).
    "hard_noise": None,
}


def generate_tasks(seed: int = 0, per_family: int = 8):
    rng = random.Random(seed)
    tasks = []
    for family, fn in _FAMILIES.items():
        for _ in range(per_family):
            h, w = rng.randint(2, 4), rng.randint(2, 4)
            train_inputs = [_rand_grid(rng, h, w) for _ in range(3)]
            test_input = _rand_grid(rng, h, w)
            if fn is None:
                # Unlearnable: each pair uses a *different* random permutation, so no
                # single program is consistent. Expect the solver to miss these.
                outs = [_rand_grid(rng, h, w) for _ in train_inputs]
                expected = _rand_grid(rng, h, w)
            else:
                outs = [dsl.to_list(fn(dsl.to_grid(g))) for g in train_inputs]
                expected = dsl.to_list(fn(dsl.to_grid(test_input)))
            task = {
                "train": [{"input": i, "output": o} for i, o in zip(train_inputs, outs)],
                "test": [{"input": test_input}],
            }
            tasks.append((family, task, expected))
    return tasks


def benchmark(seed: int = 0, per_family: int = 8) -> BenchmarkResult:
    solver = ArcSolver()
    tasks = generate_tasks(seed, per_family)
    by_family: dict[str, list[int]] = {}
    solved = 0
    for family, task, expected in tasks:
        preds = solver.solve_task(task)
        hit = preds[0]["attempt_1"] == expected
        s, t = by_family.setdefault(family, [0, 0])
        by_family[family] = [s + (1 if hit else 0), t + 1]
        if hit:
            solved += 1
    return BenchmarkResult(
        total=len(tasks),
        solved=solved,
        solve_rate=round(solved / len(tasks), 3),
        by_family={k: (v[0], v[1]) for k, v in by_family.items()},
    )


if __name__ == "__main__":  # pragma: no cover
    r = benchmark()
    print(f"ARC solver benchmark — solve rate {r.solve_rate} ({r.solved}/{r.total})")
    for fam, (s, t) in r.by_family.items():
        print(f"  {fam:26s} {s}/{t}")
