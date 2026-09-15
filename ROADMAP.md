# Roadmap & Milestones: Neuro-Symbolic ARC Solver
**Hackathon:** ARC Prize 2026 (ARC-AGI-2 & ARC-AGI-3)  
**Target:** Kaggle Code Competition  

---

## Phase 1: DSL Engine & Primitive Library (Milestone 1)
- [ ] Implement Python/NumPy library of ~40 core ARC transformation primitives.
- [ ] Build object segmentation module (connected components, color clusters, bounding boxes).
- [ ] Create automated unit test suite verifying primitives on canonical ARC training pairs.

## Phase 2: Beam Search & Genetic Program Synthesis (Milestone 2)
- [ ] Implement depth-bounded beam search combining primitive functions into composition pipelines.
- [ ] Implement pruning heuristics: reject programs that alter non-target background or violate dimension invariants.
- [ ] Benchmark DSL solver on the 400 ARC training tasks to establish baseline solve rate.

## Phase 3: LLM Reasoning & Code Generation Pipeline (Milestone 3)
- [ ] Build ASCII grid serializer and compact visual representation format for LLMs.
- [ ] Setup API harness for DeepSeek-R1 / Qwen2.5-Coder to generate candidate Python solutions.
- [ ] Implement secure sandboxed code execution runtime with sub-second timeouts.
- [ ] Create test-time verification loop that filters only 100% training-consistent programs.

## Phase 4: Ensembling, Kaggle Offline Packaging & Submission (Milestone 4)
- [ ] Combine Symbolic DSL + LLM code generation into a unified two-attempt prediction pipeline.
- [ ] Package all dependencies and models for Kaggle's offline-inference competition environment (< 9 hour limit).
- [ ] Validate generated `submission.json` against Kaggle evaluation harness and submit.
