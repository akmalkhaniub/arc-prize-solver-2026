"""Solve-rate benchmark assertions — the solver must solve DSL-expressible families
and (honestly) miss the unlearnable ones."""
from arcsolver.benchmark import benchmark


def test_solvable_families_are_solved():
    r = benchmark(seed=0, per_family=8)
    # Every family that is a single DSL primitive or a depth-2 composition must be 8/8.
    for family in ("rotate180", "reflect_h", "transpose", "gravity_down", "color_map", "compose_recolor_rotate"):
        solved, total = r.by_family[family]
        assert solved == total, f"{family}: {solved}/{total}"


def test_hard_family_is_mostly_missed():
    r = benchmark(seed=0, per_family=8)
    solved, total = r.by_family["hard_noise"]
    # Unlearnable tasks have no consistent program; the symbolic solver should miss them.
    assert solved <= 1, f"hard_noise unexpectedly solved {solved}/{total}"


def test_overall_solve_rate_is_high_on_generated_set():
    r = benchmark(seed=1, per_family=6)
    # 6 solvable families + 1 hard family → ceiling ~6/7 ≈ 0.857.
    assert r.solve_rate >= 0.80, f"solve_rate too low: {r.solve_rate}"
    assert r.total == 7 * 6
