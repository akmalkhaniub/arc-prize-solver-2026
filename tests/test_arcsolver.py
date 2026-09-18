"""ARC solver tests on synthetic tasks with known transformations."""
import numpy as np

from arcsolver import ArcSolver, dsl
from arcsolver.submission import validate_submission


def _pair(inp, fn):
    g = dsl.to_grid(inp)
    return {"input": dsl.to_list(g), "output": dsl.to_list(fn(g))}


BASE = [[1, 2, 0], [0, 3, 0], [4, 0, 0]]
BASE2 = [[5, 0], [0, 6]]


def _task(fn):
    return {"train": [_pair(BASE, fn), _pair(BASE2, fn)], "test": [{"input": BASE}]}


def test_solves_rotation():
    sol = ArcSolver().search([(dsl.to_grid(BASE), dsl.rotate90(dsl.to_grid(BASE)))])
    assert sol is not None and "rotate90" in sol.program


def test_solves_reflection_via_task():
    solver = ArcSolver()
    preds = solver.solve_task(_task(dsl.reflect_h))
    expected = dsl.to_list(dsl.reflect_h(dsl.to_grid(BASE)))
    assert preds[0]["attempt_1"] == expected


def test_solves_depth2_composition():
    # rotate then recolor (in-palette) — not reducible to any single primitive.
    fn = lambda g: dsl.replace_color(dsl.rotate90(g), 4, 3)
    sol = ArcSolver().search([(dsl.to_grid(BASE), fn(dsl.to_grid(BASE))), (dsl.to_grid(BASE2), fn(dsl.to_grid(BASE2)))])
    assert sol is not None and sol.depth == 2
    # And the found program reproduces the transformation exactly.
    assert dsl.grids_equal(sol.predict(dsl.to_grid(BASE)), fn(dsl.to_grid(BASE)))


def test_infers_color_map():
    fn = lambda g: dsl.apply_color_map(g, {1: 7, 2: 8})
    solver = ArcSolver()
    sol = solver.search([(dsl.to_grid(BASE), fn(dsl.to_grid(BASE)))])
    assert sol is not None and "color_map" in sol.program


def test_unsolved_returns_none_and_falls_back_to_two_attempts():
    # A task with no consistent DSL program still yields a well-formed 2-attempt output.
    task = {"train": [{"input": [[1]], "output": [[2]]}, {"input": [[1]], "output": [[3]]}], "test": [{"input": [[1]]}]}
    preds = ArcSolver().solve_task(task)
    assert "attempt_1" in preds[0] and "attempt_2" in preds[0]


def test_submission_format_valid():
    challenges = {
        "task_reflect": _task(dsl.reflect_h),
        "task_rot": _task(dsl.rotate180),
    }
    solver = ArcSolver()
    submission = {tid: solver.solve_task(t) for tid, t in challenges.items()}
    validate_submission(submission, challenges)  # raises on any shape error
    # rot task must be solved exactly
    assert submission["task_rot"][0]["attempt_1"] == dsl.to_list(dsl.rotate180(dsl.to_grid(BASE)))
