"""ARC DSL — pure grid transformations on 2D integer arrays (colors 0-9).

Grids are numpy int arrays. Every primitive is total and side-effect free.
"""
from __future__ import annotations

from typing import Callable

import numpy as np

Grid = np.ndarray
Program = Callable[[Grid], Grid]


def rotate90(g: Grid) -> Grid:
    return np.rot90(g, k=-1).copy()


def rotate180(g: Grid) -> Grid:
    return np.rot90(g, k=2).copy()


def rotate270(g: Grid) -> Grid:
    return np.rot90(g, k=1).copy()


def reflect_h(g: Grid) -> Grid:
    return np.fliplr(g).copy()


def reflect_v(g: Grid) -> Grid:
    return np.flipud(g).copy()


def transpose(g: Grid) -> Grid:
    return g.T.copy()


def anti_transpose(g: Grid) -> Grid:
    return np.rot90(g.T, k=2).copy()


def gravity_down(g: Grid, background: int = 0) -> Grid:
    res = np.full_like(g, background)
    h, w = g.shape
    for c in range(w):
        col = g[:, c]
        vals = col[col != background]
        if vals.size:
            res[h - vals.size:, c] = vals
    return res


def crop_nonzero(g: Grid, background: int = 0) -> Grid:
    mask = g != background
    if not mask.any():
        return np.array([[background]], dtype=g.dtype)
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    return g[rows.min():rows.max() + 1, cols.min():cols.max() + 1].copy()


def replace_color(g: Grid, src: int, dst: int) -> Grid:
    res = g.copy()
    res[g == src] = dst
    return res


def tile2x2(g: Grid) -> Grid:
    return np.tile(g, (2, 2)).copy()


def identity(g: Grid) -> Grid:
    return g.copy()


def apply_color_map(g: Grid, mapping: dict[int, int]) -> Grid:
    res = g.copy()
    for src, dst in mapping.items():
        res[g == src] = dst
    return res


def grids_equal(a: Grid | None, b: Grid | None) -> bool:
    if a is None or b is None:
        return False
    return a.shape == b.shape and bool(np.array_equal(a, b))


def to_grid(obj) -> Grid:
    return np.asarray(obj, dtype=np.int16)


def to_list(g: Grid) -> list[list[int]]:
    return [[int(v) for v in row] for row in np.asarray(g)]
