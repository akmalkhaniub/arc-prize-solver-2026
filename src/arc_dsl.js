/**
 * ARC Domain Specific Language (DSL) Primitives
 * Pure functional transformations operating on 2D integer matrices (0-9).
 */

export class ArcDSL {
  static rotate90(grid) {
    const H = grid.length, W = grid[0].length;
    const res = Array.from({ length: W }, () => new Array(H).fill(0));
    for (let r = 0; r < H; r++) {
      for (let c = 0; c < W; c++) {
        res[c][H - 1 - r] = grid[r][c];
      }
    }
    return res;
  }

  static rotate180(grid) {
    return this.rotate90(this.rotate90(grid));
  }

  static rotate270(grid) {
    return this.rotate90(this.rotate180(grid));
  }

  static reflectH(grid) {
    return grid.map(row => [...row].reverse());
  }

  static reflectV(grid) {
    return [...grid].reverse().map(row => [...row]);
  }

  static replaceColor(grid, fromColor, toColor) {
    return grid.map(row => row.map(cell => cell === fromColor ? toColor : cell));
  }

  static applyGravityDown(grid, background = 0) {
    const H = grid.length, W = grid[0].length;
    const res = Array.from({ length: H }, () => new Array(W).fill(background));

    for (let c = 0; c < W; c++) {
      let targetRow = H - 1;
      for (let r = H - 1; r >= 0; r--) {
        if (grid[r][c] !== background) {
          res[targetRow][c] = grid[r][c];
          targetRow--;
        }
      }
    }
    return res;
  }

  static cropNonZero(grid, background = 0) {
    let minR = grid.length, maxR = -1;
    let minC = grid[0].length, maxC = -1;

    for (let r = 0; r < grid.length; r++) {
      for (let c = 0; c < grid[0].length; c++) {
        if (grid[r][c] !== background) {
          if (r < minR) minR = r;
          if (r > maxR) maxR = r;
          if (c < minC) minC = c;
          if (c > maxC) maxC = c;
        }
      }
    }

    if (maxR === -1) return [[background]]; // empty grid

    const res = [];
    for (let r = minR; r <= maxR; r++) {
      res.push(grid[r].slice(minC, maxC + 1));
    }
    return res;
  }

  static isEqual(g1, g2) {
    if (!g1 || !g2) return false;
    if (g1.length !== g2.length || g1[0].length !== g2[0].length) return false;
    for (let r = 0; r < g1.length; r++) {
      for (let c = 0; c < g1[0].length; c++) {
        if (g1[r][c] !== g2[r][c]) return false;
      }
    }
    return true;
  }
}
