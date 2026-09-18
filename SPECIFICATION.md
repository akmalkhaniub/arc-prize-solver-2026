# Technical Specification: Neuro-Symbolic ARC Solver
**Project Name:** Neuro-Symbolic ARC Solver (ARC Prize 2026)  
**Status:** Rebuilt in Python — produces a Kaggle submission (updated 2026-09-18)  

> **Implementation status (2026-09-18):** Rebuilt from the Node prototype (now under `legacy-js/`) into a Python package (`arcsolver/`). Depth-1/-2 program synthesis over a NumPy DSL with train-pair verification and colour-map inference; `arcsolver/submission.py` builds and validates the ARC-AGI `submission.json` (two attempts per test input) and `notebooks/kaggle_run.py` is the offline Kaggle entry point. 6 pytest cases pass. Not built: the LLM code-synthesis branch, execution sandbox, and full 400-task tuning — this is a fast symbolic baseline, not a leaderboard-winning ensemble.
**Version:** 1.0.0  

---

## 1. System Pipeline
The solver decomposes ARC tasks into object-centric abstractions, discovers hypotheses using a combination of symbolic DSL search and LLM code generation, and executes the top candidates against the unseen test inputs.

```mermaid
graph TD
    A[ARC Task JSON: Train & Test Grids] --> B[Object Perception & Feature Extractor]
    B --> C{Search Strategy Selector}
    C -->|Simple Transformations| D[Symbolic DSL Beam Search]
    C -->|Complex Logic / Counting| E[LLM Code Synthesizer (Reasoning Model)]
    D --> F[Candidate Transformation Programs]
    E --> F
    F --> G[Execution Sandbox & Verifier]
    G -->|Validate 100% on Train Pairs| H[Rank Candidates by Minimum Description Length]
    H --> I[Execute Top 2 Candidates on Test Input]
    I --> J[Kaggle Submission JSON Matrix]
```

---

## 2. Core Functional Modules

### 2.1 Symbolic Domain Specific Language (DSL)
Primitives implemented as deterministic pure functions:
- **Geometry:** `rotate90`, `rotate180`, `rotate270`, `reflect_h`, `reflect_v`, `translate(dx, dy)`, `crop`, `upscale(factor)`.
- **Topology & Objects:** `find_connected_components(connectivity=4|8)`, `color_filter(color)`, `bounding_box(obj)`.
- **Physics & Gravity:** `apply_gravity(direction)`, `collision_detect(obj1, obj2)`.
- **Fill & Color:** `flood_fill(start, color)`, `replace_color(c1, c2)`, `majority_color(grid)`.

### 2.2 LLM Code Synthesis & In-Context Prompting
- Format 2D grids into spatial ASCII representations with 2D character mapping (`0=.`, `1=B`, `2=R`, etc.).
- Instruct the reasoning model to generate a Python function `transform(grid: np.ndarray) -> np.ndarray`.
- Execute within a restricted, sandboxed Python runtime with a 500ms timeout per candidate.

### 2.3 Verification & Consensus Voting
- A candidate function is valid *only* if it achieves 100% exact pixel match across **all** demonstration training pairs.
- If multiple candidate functions pass, rank them by simplicity (code length / AST complexity) and ensemble predictions.

---

## 3. Data Formats

### 3.1 ARC Task Schema
```typescript
interface ARCTask {
  train: Array<{
    input: number[][];
    output: number[][];
  }>;
  test: Array<{
    input: number[][];
    output?: number[][];
  }>;
}
```

### 3.2 Submission Format (`submission.json`)
```json
{
  "task_id_001": [
    { "attempt_1": [[0, 1], [1, 0]], "attempt_2": [[1, 0], [0, 1]] }
  ]
}
```

---

## 4. Acceptance Criteria
1. Symbolic DSL solves > 60% of basic transformation tasks from the official ARC evaluation set.
2. Code synthesis execution sandbox operates with strict memory (< 512MB) and time limits (< 2s) per task.
3. Notebook pipeline successfully outputs valid submission format meeting all Kaggle competition criteria.
