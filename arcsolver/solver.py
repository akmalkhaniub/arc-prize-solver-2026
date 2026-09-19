"""Neuro-symbolic ARC solver: depth-bounded program synthesis over the DSL.

Searches compositions of DSL primitives (depth 1 then depth 2) for a program that
reproduces every training pair exactly, plus a data-driven color-map inference step.
Produces the two attempts the ARC-AGI submission format expects.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from . import dsl
from .dsl import Grid, Program


@dataclass
class NamedProgram:
    name: str
    fn: Program


def _base_ops() -> list[NamedProgram]:
    ops: list[NamedProgram] = [
        NamedProgram("identity", dsl.identity),
        NamedProgram("rotate90", dsl.rotate90),
        NamedProgram("rotate180", dsl.rotate180),
        NamedProgram("rotate270", dsl.rotate270),
        NamedProgram("reflect_h", dsl.reflect_h),
        NamedProgram("reflect_v", dsl.reflect_v),
        NamedProgram("transpose", dsl.transpose),
        NamedProgram("anti_transpose", dsl.anti_transpose),
        NamedProgram("gravity_down", dsl.gravity_down),
        NamedProgram("crop_nonzero", dsl.crop_nonzero),
        NamedProgram("tile2x2", dsl.tile2x2),
        # Standard ARC shape/scale/mirror/half primitives.
        NamedProgram("scale2", dsl.scale2),
        NamedProgram("scale3", dsl.scale3),
        NamedProgram("tile_h", dsl.tile_h),
        NamedProgram("tile_v", dsl.tile_v),
        NamedProgram("concat_h_mirror", dsl.concat_h_mirror),
        NamedProgram("concat_v_mirror", dsl.concat_v_mirror),
        NamedProgram("trim_border", dsl.trim_border),
        NamedProgram("top_half", dsl.top_half),
        NamedProgram("bottom_half", dsl.bottom_half),
        NamedProgram("left_half", dsl.left_half),
        NamedProgram("right_half", dsl.right_half),
        NamedProgram("swap_two_most_common", dsl.swap_two_most_common),
    ]
    # A handful of explicit color swaps among the low palette.
    for a in range(1, 5):
        for b in range(1, 5):
            if a != b:
                ops.append(NamedProgram(f"replace({a}->{b})", lambda g, a=a, b=b: dsl.replace_color(g, a, b)))
    return ops


# Curated op subset for the (expensive) depth-3 search — the geometric/scale/recolor
# primitives that most often compose, kept small to bound the O(n^3) cost.
_DEPTH3_OPS = {
    "rotate90", "rotate180", "reflect_h", "reflect_v", "transpose",
    "gravity_down", "crop_nonzero", "scale2", "tile_h", "tile_v",
    "concat_h_mirror", "concat_v_mirror", "swap_two_most_common",
}


@dataclass
class Solution:
    status: str          # "SOLVED" | "UNSOLVED"
    program: str
    depth: int
    predict: Callable[[Grid], Grid]


def _infer_color_map(train: list[tuple[Grid, Grid]]) -> dict[int, int] | None:
    """If every pair is same-shape and related by a consistent per-color relabeling, return it."""
    mapping: dict[int, int] = {}
    for inp, out in train:
        if inp.shape != out.shape:
            return None
        for src, dst in zip(inp.flatten().tolist(), out.flatten().tolist()):
            if src in mapping and mapping[src] != dst:
                return None
            mapping[src] = dst
    # Must actually change something, otherwise it's just identity.
    return mapping if any(k != v for k, v in mapping.items()) else None


class ArcSolver:
    def __init__(self) -> None:
        self.ops = _base_ops()

    @staticmethod
    def _verify(fn: Program, train: list[tuple[Grid, Grid]]) -> bool:
        for inp, out in train:
            try:
                if not dsl.grids_equal(fn(inp), out):
                    return False
            except Exception:
                return False
        return True

    def search(self, train: list[tuple[Grid, Grid]]) -> Solution | None:
        # Depth 1
        for op in self.ops:
            if self._verify(op.fn, train):
                return Solution("SOLVED", op.name, 1, op.fn)
        # Data-driven color map
        cmap = _infer_color_map(train)
        if cmap is not None:
            fn = lambda g, m=cmap: dsl.apply_color_map(g, m)
            if self._verify(fn, train):
                return Solution("SOLVED", f"color_map{cmap}", 1, fn)
        # Depth 2
        for op1 in self.ops:
            for op2 in self.ops:
                fn = lambda g, a=op1.fn, b=op2.fn: b(a(g))
                if self._verify(fn, train):
                    return Solution("SOLVED", f"{op2.name}∘{op1.name}", 2, fn)

        # Depth 3 — bounded to a curated subset so runtime stays within Kaggle limits.
        # Only reached when depth-1/-2 fail; keeps the common case fast.
        core = [o for o in self.ops if o.name in _DEPTH3_OPS]
        for op1 in core:
            for op2 in core:
                for op3 in core:
                    fn = lambda g, a=op1.fn, b=op2.fn, c=op3.fn: c(b(a(g)))
                    if self._verify(fn, train):
                        return Solution("SOLVED", f"{op3.name}∘{op2.name}∘{op1.name}", 3, fn)
        return None

    def solve_task(self, task: dict) -> list[dict[str, list[list[int]]]]:
        """Return one {"attempt_1", "attempt_2"} per test input, per ARC-AGI format."""
        train = [(dsl.to_grid(p["input"]), dsl.to_grid(p["output"])) for p in task["train"]]
        tests = [dsl.to_grid(t["input"]) for t in task["test"]]

        solution = self.search(train)
        # Second attempt: a distinct fallback (D4 variant) so we submit two guesses.
        secondary: Callable[[Grid], Grid] = dsl.rotate180 if solution and solution.program != "rotate180" else dsl.reflect_h

        out: list[dict[str, list[list[int]]]] = []
        for t in tests:
            if solution is not None:
                try:
                    a1 = dsl.to_list(solution.predict(t))
                except Exception:
                    a1 = dsl.to_list(t)
            else:
                a1 = dsl.to_list(t)
            try:
                a2 = dsl.to_list(secondary(t))
            except Exception:
                a2 = a1
            out.append({"attempt_1": a1, "attempt_2": a2})
        return out
