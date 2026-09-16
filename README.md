# 🧩 ARC Prize Solver 2026 — Neuro-Symbolic Test-Time Compute (TTC) Engine

[![ARC Prize](https://img.shields.io/badge/ARC_Prize-2026_AGI_Benchmark-red.svg)](https://arcprize.org/)
[![Benchmark](https://img.shields.io/badge/Benchmark-François_Chollet_ARC--AGI-blueviolet.svg)](https://github.com/fchollet/ARC-AGI)
[![Methodology](https://img.shields.io/badge/Paradigm-Neuro--Symbolic_Program_Synthesis-blue.svg)](#neuro-symbolic-synthesis)
[![Test-Time Compute](https://img.shields.io/badge/Scaling-Test--Time_Compute_(TTC)-orange.svg)](#test-time-compute-ttc-refinement-loop)
[![Invariance](https://img.shields.io/badge/Group_Theory-D4_Dihedral_Symmetry-teal.svg)](#dsl-primitives--geometric-invariances)
[![Tests Passing](https://img.shields.io/badge/Tests-4%2F4_Passed_100%25-brightgreen.svg)](#test-verification)

> **Autonomous abstract reasoning engine for the François Chollet ARC-AGI Challenge.** Combines a typed 2D grid Domain-Specific Language (DSL) with **Test-Time Compute (TTC) refinement loops**, synthesizing verifiable transformation programs from only 2 to 4 demonstration pairs without gradient fine-tuning.

---

## 📌 Executive Summary & Hackathon Pitch

François Chollet's **Abstraction and Reasoning Corpus (ARC-AGI)** measures true broad AI generalization. Unlike conventional language benchmarks, ARC cannot be memorized:
- Each task presents an entirely novel spatial/algorithmic puzzle never seen during training.
- Only **2 to 4 input/output grid demonstrations** are given per task.
- Massive LLMs struggle because autoregressive next-token prediction lacks explicit spatial invariants and geometric reasoning.

### The Neuro-Symbolic & Test-Time Compute Solution
Instead of treating grid puzzles as raw token sequences or continuous latent vectors, this solver frames reasoning as **search over program hypotheses**:
1. **Domain-Specific Language (DSL)**: Hardens core human Core Knowledge Priors (objectness, $D_4$ dihedral group reflections/rotations, topological gravity, bounding box alignment, color isomorphism).
2. **Test-Time Compute (TTC) Exploration**: Allocates runtime compute dynamically to evaluate candidate program graphs against training pairs.
3. **Execution-Guided Verification**: Any candidate program must achieve $100.00\%$ loss-free reconstruction on every training grid before being allowed to synthesize predictions for unseen test grids.

---

## 🏛️ System Architecture

```
  +-----------------------------------------------------------------------------------------+
  |                               ARC-AGI TASK INPUT DEMONSTRATIONS                         |
  |                                                                                         |
  |    Train Pair 1: [ Grid In 1 ] ──> [ Grid Out 1 ]                                       |
  |    Train Pair 2: [ Grid In 2 ] ──> [ Grid Out 2 ]                                       |
  |    Test Input:   [ Grid In ? ] ──> [ ??? Target ]                                       |
  +-------------------------------------------+---------------------------------------------+
                                              |
                                              v
  +-----------------------------------------------------------------------------------------+
  |                         TEST-TIME COMPUTE (TTC) REFINEMENT ENGINE                       |
  |                                                                                         |
  |   +--------------------------+    +---------------------------+    +----------------+   |
  |   | DSL Program Synthesizer  |--->|  Hypothesis Beam Search   |<---| Heuristic Cost |   |
  |   | (D4, Gravity, Topology)  |    |  (Depth 1..K Composition) |    | Distance Metric|   |
  |   +--------------------------+    +-------------+-------------+    +----------------+   |
  +-------------------------------------------------|---------------------------------------+
                                                    |
                                                    v
  +-----------------------------------------------------------------------------------------+
  |                           EXECUTION VERIFICATION HARNESS                                |
  |                                                                                         |
  |              Is P(Train_In_i) == Train_Out_i for ALL demonstration pairs?               |
  |                         [ YES ]                                [ NO ]                   |
  |                            |                                      |                     |
  |                            v                                      v                     |
  |             +-------------------------------+        +--------------------------+       |
  |             | Program Hypothesis Confirmed  |        | Backtrack & Refine Hypothesis    |
  |             +---------------+---------------+        +--------------------------+       |
  +-----------------------------|-----------------------------------------------------------+
                                |
                                v
  +-----------------------------------------------------------------------------------------+
  |                          DETERMINISTIC TEST GRID SYNTHESIS                              |
  |                                                                                         |
  |                      Output = P_verified( Test_In ) (Zero Hallucination)                |
  +-----------------------------------------------------------------------------------------+
```

---

## 🔬 Core Engineering Modules

| Module | Source File | Functionality |
| :--- | :--- | :--- |
| **ARC DSL Primitives** | [`src/arc_dsl.js`](src/arc_dsl.js) | Full primitive library: $D_4$ rotations ($90^\circ, 180^\circ, 270^\circ$), reflections (horizontal, vertical, diagonal), gravity drop, color remapping, bounding box cropping. |
| **ARC Solver** | [`src/arc_solver.js`](src/arc_solver.js) | Program candidate synthesizer, execution validator, and multi-step composition generator ($f \circ g$). |
| **TTC Refinement Loop** | [`src/ttc_refinement_loop.js`](src/ttc_refinement_loop.js) | Test-Time Compute scheduler prioritizing lightweight transformations first before scaling beam search budget. |
| **Interactive Grid Visualizer** | [`src/server.js`](src/server.js) + [`src/public/index.html`](src/public/index.html) | Live interactive web IDE rendering ARC 10-color palettes, interactive grid drawing, and real-time program synthesis logs. |

---

## ⚡ Quickstart Guide

### 1. Installation
```bash
git clone https://github.com/akmalkhaniub/arc-prize-solver-2026.git
cd arc-prize-solver-2026
npm install
```

### 2. Run Automated Verification Test Suite
```bash
npm test
```

### 3. Launch Interactive Operations Dashboard
```bash
node src/server.js
```
Open **`http://localhost:3006`** in your browser:
- Load standard ARC challenge tasks (Reflection, Color Substitution, Multi-Step Physics Gravity).
- Inspect synthesized AST programs (e.g. `reflectH >> applyGravityDown`).
- Verify execution outputs side-by-side on the interactive color-coded 2D grid canvas.

---

## 🧪 Test Verification

The neuro-symbolic program synthesizer and TTC loop are tested across representative challenge categories:

```text
> arc-prize-solver@1.0.0 test
> node test/verify_arc_solver.js

🧪 Starting Neuro-Symbolic ARC Solver Automated Verification Suite (ARC Prize 2026)...

1️⃣ Testing Task 1: Horizontal Reflection Task...
   ✅ Solved at depth 1 using synthesized program "reflectH".
2️⃣ Testing Task 2: Color Substitution Task (Blue to Red)...
   ✅ Solved at depth 1 using synthesized program "replaceColor(1->2)".
3️⃣ Testing Task 3: Composite Multi-Step Transformation (Gravity Down ∘ ReflectH)...
   ✅ Composite Solved: "gravityDown ∘ reflectH"
   Test Output Grid: [[0,0,0],[0,0,0],[0,2,1]]
4️⃣ Testing Test-Time Compute (TTC) Refinement Loop...
   ⚡ TTC Refinement Loop solved task in 3ms with program: "reflectH >> applyGravityDown"

🎉 ALL ARC PRIZE 2026 NEURO-SYMBOLIC SOLVER TESTS PASSED WITH 100% SUCCESS!
```

---

## 🚀 Benchmark Roadmap & LLM Hybridization

- **Hybrid LLM Hypothesis Seeding**: Integration with Claude 3.5 Sonnet / DeepSeek R1 to generate high-level semantic hints, which are then passed into the formal DSL verifier.
- **Kaggle Notebook Submission**: Packaged as an offline inference kernel running under 9 hours on 2x T4 or 1x P100 GPU environments.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
