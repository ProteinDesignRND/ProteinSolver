# Durable Memory: Agent Rules, Scientific Lessons, & Architecture Decisions

This document records the non-negotiable principles, lessons, and boundaries governing the `ProteinDesignRND/ProteinSolver` implementation repository.

---

## 1. Core Methodological Lessons

### Lesson 1 — Runtime Verification != Milestone 1 Completion
Verifying that a model forward pass executes is an E0 milestone. Full Milestone 1 requires complete upstream preservation, compatibility adaptations, production backend, usable frontend, automated test suites, clean-clone reproducibility, and team git governance.

### Lesson 2 — Explicit Upstream Provenance
Baseline commit `69ef0965a3fc3bf191804035b539720a06e58ba6` is preserved through a GitHub fork of ostrokach/proteinsolver. Downstream code is strictly segregated from upstream files.

### Lesson 3 — Single-Target Fixture != Benchmark
Recovery of 41.30% (38/92 residues) on `1n5uA03` is a single-target integration check. It must never be described as a general benchmark or benchmark recovery across folds.

### Lesson 4 — Zero Native Sequence Leakage Invariant
In Design Mode:
- `data.x` is initialized strictly to mask token `20` for all residues.
- `data.y` is deleted/stripped from the PyG batch.
- Native sequence comparison is quarantined strictly to diagnostic mode (`/api/diagnostic`).
- Wording: "Design-path input invariant enforced by the compatibility/application layer and protected by regression tests."

### Lesson 5 — Never Weaken Tests to Force Passes
When implementation and test contract disagree, determine the canonical contract and fix the implementation or test specification honestly. For example, `model_name` is canonically `ProteinSolver` and `model_class` is `ProteinNet`.

### Lesson 6 — Clean Clone Independence
A clean-clone verification must use a brand-new virtual environment with its own dependencies, never piggybacking on another repository's environment or global packages.

### Lesson 7 — No Unsupported "Production-Grade" Claims
Use accurate descriptors: "local mentor-ready application backend," "functionally verified," "compatibility adapted."

### Lesson 8 — No "Mathematically Guaranteed" Without Formal Proofs
Describe leak protection as an enforced design-path invariant protected by regression tests.

### Lesson 9 — Anti-Infinite Debug Loop Policy
Maximum 3 coherent repair attempts per underlying issue. If unresolved after 3 attempts, classify as `BLOCKED`, record evidence, preserve working state, and proceed with independent work.

### Lesson 10 — Architecture Stability
Do not continuously rewrite architecture once requirements are verified.
