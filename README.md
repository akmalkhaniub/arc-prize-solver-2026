# ARC Prize 2026 (ARC-AGI-2 & ARC-AGI-3)

- **Official Challenge URL:** [https://www.kaggle.com/competitions](https://www.kaggle.com/competitions) / [https://arcprize.org/](https://arcprize.org/)
- **Organizer:** ARC Prize Foundation & Kaggle
- **Host Platform:** Kaggle Competitions
- **Total Prize Pool:** $850,000+ USD ($2,000,000+ across all active ARC tracks)
- **Format:** Online / Global Code Competition
- **Primary Themes:** Artificial General Intelligence (AGI), Neuro-Symbolic AI, Program Synthesis, Novel Reasoning

---

## 1. Challenge Overview & Problem Statement
The Abstraction and Reasoning Corpus (ARC-AGI), created by François Chollet, is widely recognized as the premier benchmark for measuring true fluid intelligence and general reasoning in artificial intelligence.

Unlike traditional AI benchmarks that test skills acquired through memorization of vast training sets, ARC presents completely novel visual-spatial transformation tasks where the model only receives 3 to 5 demonstration input-output grid pairs, and must infer the latent rule to generate the correct output grid for the test input.

### Key Rules & Constraints
- Grids are 2D matrices of integers `0–9` representing 10 discrete colors, sizing up to `30x30`.
- Exact match metric: A prediction is only scored correct (1.0) if every single pixel in the output grid matches the ground truth.
- Two submission attempts per test task are permitted.

---

## 2. Selected Architectural Strategy: Neuro-Symbolic Program Synthesis & Cellular Automata Search
A hybrid neuro-symbolic engine combining:
1. **Core Domain Specific Language (DSL):** Geometric transformations, topological flood-fills, gravity, object segmentation, and symmetry primitives.
2. **LLM Program Proposal Engine:** Using fine-tuned reasoning models (DeepSeek-R1 / Qwen-2.5-Coder) to propose candidate Python transformation functions given ASCII grid encodings.
3. **Beam Search & Cellular Automata Evaluator:** Fast C++/Python execution engine that executes proposed transformation programs and ranks them via minimum description length (MDL) and verification against training pairs.

---

## 3. Directory Structure
```
kaggle-arc-prize-2026/
├── README.md               # Benchmark definition, rules, links (this file)
├── SPECIFICATION.md        # DSL specification, program synthesis search architecture
├── ROADMAP.md              # Research and submission milestones
├── dsl/                    # Primitive geometric, topological & color transformations
├── solver/                 # Program synthesizer, beam search & cellular automata
├── models/                 # LLM prompting harnesses & fine-tuning scripts
└── notebooks/              # Kaggle submission notebook pipeline
```
