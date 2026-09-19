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


# --- Additional standard ARC primitives (all total, grid -> grid) ---

def scale2(g: Grid) -> Grid:
    return np.repeat(np.repeat(g, 2, axis=0), 2, axis=1).copy()


def scale3(g: Grid) -> Grid:
    return np.repeat(np.repeat(g, 3, axis=0), 3, axis=1).copy()


def tile_h(g: Grid) -> Grid:
    return np.tile(g, (1, 2)).copy()


def tile_v(g: Grid) -> Grid:
    return np.tile(g, (2, 1)).copy()


def concat_h_mirror(g: Grid) -> Grid:
    return np.concatenate([g, np.fliplr(g)], axis=1).copy()


def concat_v_mirror(g: Grid) -> Grid:
    return np.concatenate([g, np.flipud(g)], axis=0).copy()


def trim_border(g: Grid) -> Grid:
    return g[1:-1, 1:-1].copy() if g.shape[0] > 2 and g.shape[1] > 2 else g.copy()


def top_half(g: Grid) -> Grid:
    return g[: g.shape[0] // 2 or 1].copy()


def bottom_half(g: Grid) -> Grid:
    return g[g.shape[0] // 2:].copy()


def left_half(g: Grid) -> Grid:
    return g[:, : g.shape[1] // 2 or 1].copy()


def right_half(g: Grid) -> Grid:
    return g[:, g.shape[1] // 2:].copy()


def most_common_color(g: Grid) -> int:
    vals, counts = np.unique(g, return_counts=True)
    return int(vals[int(np.argmax(counts))])


def swap_two_most_common(g: Grid) -> Grid:
    """Swap the two most frequent colors — a common ARC recolor pattern."""
    vals, counts = np.unique(g, return_counts=True)
    if vals.size < 2:
        return g.copy()
    order = np.argsort(counts)[::-1]
    a, b = int(vals[order[0]]), int(vals[order[1]])
    res = g.copy()
    res[g == a] = b
    res[g == b] = a
    return res


def _label_components(mask: Grid) -> tuple[Grid, int]:
    """4-connected connected-component labeling in pure NumPy (BFS). mask is boolean."""
    labels = np.zeros(mask.shape, dtype=np.int32)
    n = 0
    h, w = mask.shape
    for r in range(h):
        for c in range(w):
            if mask[r, c] and labels[r, c] == 0:
                n += 1
                stack = [(r, c)]
                labels[r, c] = n
                while stack:
                    y, x = stack.pop()
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and labels[ny, nx] == 0:
                            labels[ny, nx] = n
                            stack.append((ny, nx))
    return labels, n


def largest_object(g: Grid, background: int = 0) -> Grid:
    """Crop to the bounding box of the largest connected non-background component."""
    labels, n = _label_components(g != background)
    if n == 0:
        return g.copy()
    sizes = [int((labels == i).sum()) for i in range(1, n + 1)]
    best = int(np.argmax(sizes)) + 1
    ys, xs = np.where(labels == best)
    return g[ys.min():ys.max() + 1, xs.min():xs.max() + 1].copy()


def symmetrize_h(g: Grid, background: int = 0) -> Grid:
    """Make left-right symmetric by overlaying the horizontal mirror onto background cells."""
    res = g.copy()
    mirror = np.fliplr(g)
    fill = (res == background) & (mirror != background)
    res[fill] = mirror[fill]
    return res


def grids_equal(a: Grid | None, b: Grid | None) -> bool:
    if a is None or b is None:
        return False
    return a.shape == b.shape and bool(np.array_equal(a, b))


def to_grid(obj) -> Grid:
    return np.asarray(obj, dtype=np.int16)


def to_list(g: Grid) -> list[list[int]]:
    return [[int(v) for v in row] for row in np.asarray(g)]
