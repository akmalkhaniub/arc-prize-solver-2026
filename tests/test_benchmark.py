"""Solve-rate benchmark assertions — the expanded DSL + depth-3 search must solve
DSL-expressible families (incl. scale/mirror/half and a depth-3 composition) and
(honestly) miss the unlearnable ones."""
from arcsolver.benchmark import benchmark


SOLVABLE = (
    "rotate180", "reflect_h", "transpose", "gravity_down", "color_map",
    "compose_recolor_rotate", "scale2", "concat_h_mirror", "top_half",
    "swap_two_most_common", "compose3",
)


def test_solvable_families_are_solved():
    r = benchmark(seed=0, per_family=6)
    for family in SOLVABLE:
        solved, total = r.by_family[family]
        assert solved == total, f"{family}: {solved}/{total}"


def test_depth3_composition_family_is_solved():
    # compose3 = concat_h_mirror ∘ rotate180 ∘ scale2 — only reachable with depth-3 search.
    r = benchmark(seed=2, per_family=5)
    solved, total = r.by_family["compose3"]
    assert solved == total, f"compose3 depth-3 search failed: {solved}/{total}"


def test_hard_family_is_mostly_missed():
    r = benchmark(seed=0, per_family=6)
    solved, total = r.by_family["hard_noise"]
    assert solved <= 1, f"hard_noise unexpectedly solved {solved}/{total}"


def test_overall_solve_rate_improved():
    r = benchmark(seed=1, per_family=6)
    # 11 solvable families + 1 hard family → ceiling ~11/12 ≈ 0.917.
    assert r.solve_rate >= 0.88, f"solve_rate regressed: {r.solve_rate}"
