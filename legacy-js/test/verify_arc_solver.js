import assert from 'assert';
import { ArcSolver } from '../src/arc_solver.js';
import { ArcDSL } from '../src/arc_dsl.js';
import { TTCRefinementLoop } from '../src/ttc_refinement_loop.js';

console.log('🧪 Starting Neuro-Symbolic ARC Solver Automated Verification Suite (ARC Prize 2026)...\n');

const solver = new ArcSolver();
const ttc = new TTCRefinementLoop();

// Task 1: Horizontal Reflection Task
console.log('1️⃣ Testing Task 1: Horizontal Reflection Task...');
const task1 = {
  train: [
    {
      input: [[1, 0, 0], [1, 2, 0]],
      output: [[0, 0, 1], [0, 2, 1]]
    },
    {
      input: [[3, 1], [0, 2]],
      output: [[1, 3], [2, 0]]
    }
  ],
  test: [
    {
      input: [[2, 1, 0], [0, 0, 3]]
    }
  ]
};

const res1 = solver.solve(task1);
assert(res1.status === 'SOLVED', 'Task 1 must be solved');
assert(res1.programDescription === 'reflectH', 'Must infer reflectH program');
const expectedTest1 = [[0, 1, 2], [3, 0, 0]];
assert(ArcDSL.isEqual(res1.predictions[0], expectedTest1), 'Test prediction must match ground truth');
console.log(`   ✅ Solved at depth ${res1.programDepth} using synthesized program "${res1.programDescription}".`);

// Task 2: Color Substitution Task (1 -> 2)
console.log('2️⃣ Testing Task 2: Color Substitution Task (Blue to Red)...');
const task2 = {
  train: [
    {
      input: [[1, 0], [0, 1]],
      output: [[2, 0], [0, 2]]
    },
    {
      input: [[1, 1], [0, 0]],
      output: [[2, 2], [0, 0]]
    }
  ],
  test: [
    {
      input: [[0, 1, 1], [1, 0, 0]]
    }
  ]
};

const res2 = solver.solve(task2);
assert(res2.status === 'SOLVED', 'Task 2 must be solved');
assert(res2.programDescription.includes('replaceColor(1->2)'), 'Must infer color substitution');
const expectedTest2 = [[0, 2, 2], [2, 0, 0]];
assert(ArcDSL.isEqual(res2.predictions[0], expectedTest2), 'Test prediction must match ground truth');
console.log(`   ✅ Solved at depth ${res2.programDepth} using synthesized program "${res2.programDescription}".`);

// Task 3: Composite Program Synthesis (Gravity Down ∘ ReflectH)
console.log('3️⃣ Testing Task 3: Composite Multi-Step Transformation (Gravity Down ∘ ReflectH)...');
const task3 = {
  train: [
    {
      input: [
        [1, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
      ],
      output: [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 1]
      ]
    },
    {
      input: [
        [2, 0, 0],
        [3, 0, 0],
        [0, 0, 0]
      ],
      output: [
        [0, 0, 0],
        [0, 0, 2],
        [0, 0, 3]
      ]
    }
  ],
  test: [
    {
      input: [
        [1, 2, 0],
        [0, 0, 0],
        [0, 0, 0]
      ]
    }
  ]
};

const res3 = solver.solve(task3);
assert(res3.status === 'SOLVED', 'Task 3 must be solved');
assert(res3.programDepth === 2, 'Must solve with depth 2 composition');
console.log(`   ✅ Composite Solved: "${res3.programDescription}"`);
console.log('   Test Output Grid:', JSON.stringify(res3.predictions[0]));

// Task 4: Test-Time Compute (TTC) Refinement Loop
console.log('4️⃣ Testing Test-Time Compute (TTC) Refinement Loop...');
const ttcResult = ttc.refineSolution(task3);
assert(ttcResult.status === 'SOLVED', 'TTC refinement must solve task3');
assert(ttcResult.confidence === 1.0, 'TTC confidence must be 1.0 on task3');
console.log(`   ⚡ TTC Refinement Loop solved task in ${ttcResult.computeTimeMs}ms with program: "${ttcResult.programDescription}"`);

console.log('\n🎉 ALL ARC PRIZE 2026 NEURO-SYMBOLIC SOLVER TESTS PASSED WITH 100% SUCCESS!\n');
