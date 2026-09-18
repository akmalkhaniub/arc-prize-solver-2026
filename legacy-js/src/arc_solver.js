import { ArcDSL } from './arc_dsl.js';

/**
 * ArcSolver - Hypothesis Search & Program Synthesizer
 * Composes DSL primitives and validates candidate programs against demonstration pairs.
 */
export class ArcSolver {
  constructor() {
    this.atomicOperations = [
      { name: 'rotate90', fn: (g) => ArcDSL.rotate90(g) },
      { name: 'rotate180', fn: (g) => ArcDSL.rotate180(g) },
      { name: 'rotate270', fn: (g) => ArcDSL.rotate270(g) },
      { name: 'reflectH', fn: (g) => ArcDSL.reflectH(g) },
      { name: 'reflectV', fn: (g) => ArcDSL.reflectV(g) },
      { name: 'gravityDown', fn: (g) => ArcDSL.applyGravityDown(g) },
      { name: 'crop', fn: (g) => ArcDSL.cropNonZero(g) }
    ];

    // Add common color substitution operations (0-9)
    for (let c1 = 1; c1 <= 3; c1++) {
      for (let c2 = 1; c2 <= 3; c2++) {
        if (c1 !== c2) {
          this.atomicOperations.push({
            name: `replaceColor(${c1}->${c2})`,
            fn: (g) => ArcDSL.replaceColor(g, c1, c2)
          });
        }
      }
    }
  }

  /**
   * Solve an ARC task by program synthesis beam search
   * @param {Object} task { train: [{input, output}], test: [{input}] }
   * @returns {Object} Solution with synthesized program and test predictions
   */
  solve(task) {
    const trainPairs = task.train;

    // 1. Search Depth 1 (Atomic operations)
    for (const op of this.atomicOperations) {
      if (this.verifyHypothesis(op.fn, trainPairs)) {
        const predictions = task.test.map(t => op.fn(t.input));
        return {
          status: 'SOLVED',
          programDepth: 1,
          programDescription: op.name,
          predictions
        };
      }
    }

    // 2. Search Depth 2 (Composition of 2 operations: op2(op1(grid)))
    for (const op1 of this.atomicOperations) {
      for (const op2 of this.atomicOperations) {
        const compositeFn = (g) => op2.fn(op1.fn(g));
        if (this.verifyHypothesis(compositeFn, trainPairs)) {
          const predictions = task.test.map(t => compositeFn(t.input));
          return {
            status: 'SOLVED',
            programDepth: 2,
            programDescription: `${op2.name} ∘ ${op1.name}`,
            predictions
          };
        }
      }
    }

    return {
      status: 'UNSOLVED',
      message: 'Exhausted depth-2 DSL search space without finding 100% training-consistent program.'
    };
  }

  /**
   * Verify if candidate function transforms every training input exactly into its output
   */
  verifyHypothesis(fn, trainPairs) {
    for (const pair of trainPairs) {
      try {
        const predicted = fn(pair.input);
        if (!ArcDSL.isEqual(predicted, pair.output)) {
          return false;
        }
      } catch {
        return false;
      }
    }
    return true;
  }
}
