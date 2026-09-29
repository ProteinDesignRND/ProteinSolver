# Durable Memory: Agent Rules, Scientific Lessons, & Architecture Decisions

This document records the non-negotiable principles, lessons, and boundaries governing the `ProteinDesignRND/ProteinSolver` implementation repository.

---

## 1. Core Methodological Lessons

### Lesson 1 — Runtime Verification != Milestone 1 Completion
Verifying that a model forward pass executes is an E0 milestone. Full Milestone 1 requires complete upstream preservation, compatibility adaptations, production backend, usable frontend, automated test suites, clean-clone reproducibility, and team git governance.

### Lesson 2 — Explicit Upstream Provenance & Push Safety
Baseline commit `69ef0965a3fc3bf191804035b539720a06e58ba6` is preserved through a GitHub fork of `ostrokach/proteinsolver`. Downstream code is strictly segregated from upstream files. The upstream remote push URL must always be set to `no_push` (`git remote set-url --push upstream no_push`) to prevent accidental upstream pushes.

### Lesson 3 — Single-Target Fixture != Benchmark
Recovery of 41.30% (38/92 residues) on `1n5uA03` is a single-target integration check. It must never be described as a general benchmark or benchmark recovery across folds. Training set membership of `1n5uA03` is not independently verified against the external training shards.

### Lesson 4 — Zero Native Sequence Leakage Invariant
In Design Mode:
- `data.x` is initialized strictly to mask token `20` for all residues.
- `data.y` is deleted/stripped from the PyG batch.
- Native sequence comparison is quarantined strictly to diagnostic mode (`/api/diagnostic`).
- Wording: "Design-path input invariant enforced by the compatibility/application layer and protected by regression tests."

### Lesson 5 — Never Weaken Tests to Force Passes
When implementation and test contract disagree, determine the canonical contract and fix the implementation or test specification honestly. For example, `model_name` is canonically `ProteinSolver` and `model_class` is `ProteinNet`.

### Lesson 6 — Clean Clone Independence & Wrong Environment Prevention
A clean-clone verification must use a brand-new virtual environment with its own dependencies, never piggybacking on another repository's environment (e.g. `Protein Design`) or global packages. Verify `sys.path` to ensure zero cross-repo contamination.

### Lesson 7 — No Unsupported "Production-Grade" Claims
Use accurate descriptors: "local mentor-ready application backend," "functionally verified," "compatibility adapted."

### Lesson 8 — No "Mathematically Guaranteed" Without Formal Proofs
Describe leak protection as an enforced design-path invariant protected by regression tests. Avoid phrases like "mathematically guaranteed" or "algorithmic correctness proof."

### Lesson 9 — Anti-Infinite Debug Loop Policy
Maximum 3 coherent repair attempts per underlying issue. If unresolved after 3 attempts, classify as `BLOCKED`, record evidence, preserve working state, and proceed with independent work.

### Lesson 10 — Architecture Stability
Do not continuously rewrite architecture once requirements are verified.

### Lesson 11 — Hard Working-Directory Safety Rule
Every agent execution must begin by verifying the exact expected repository directory. If it does not match, execution stops. Agents must not cd into other repositories during the run. Cross-repository read-only checks must use explicit paths such as `git -C` without changing the current working directory.

### Lesson 12 — Acquisition HEAD vs. Scientific Reference Commit
Distinguish between the commit at which the fork was acquired (`69ef0965a3fc3bf191804035b539720a06e58ba6`) and any downstream reference commits. Upstream commit lineage must remain 100% intact.

### Lesson 13 — Architecture Terminology: 128 Hidden Dimension vs. 162 Attention Test
`ProteinNet` has a hidden dimensionality of 128 (4 EdgeConv blocks, 567,060 parameters). 162 is strictly the embedding dimension in an upstream functional test for sparse multi-head attention (`tests/nn/test_functional.py`), not the model's hidden dimension.

### Lesson 14 — Compatibility Scope: Exactly 7 Issues
The compatibility layer (`compat/`) resolves exactly 7 distinct issues:
1. Windows POSIX `fcntl` locking stub (fails loudly on Windows)
2. BioPython structure parser & heavy-atom distance matrix ($r < 12.0$ Å)
3. PyG 2.x `scatter_` backward-compatibility shim
4. PyG 2.8 Batch and collate handling
5. Checkpoint key translation (`graph_conv_0.` -> `graph_conv_1.`)
6. PyTorch 2.6 CPU CSP standardization
7. `ruamel.yaml` 0.18+ safe_load compatibility

### Lesson 15 — Build vs. Browser E2E Distinction
Passing `npm run build` and backend API integration tests proves build and API functionality, but does NOT constitute automated browser end-to-end (E2E) testing. Always classify honestly as `BROWSER_E2E_NOT_AUTOMATED`.

### Lesson 16 — Bounded AI Artifact & Context Scope
Avoid unbounded context growth. Rely on the repository itself as the source of truth, verify against active files, and avoid dumping scratch paths or machine-specific logs into persistent documentation.

### Lesson 17 (Proposed) — Cross-Repository Evidence Transfer
Historical evidence may be copied into another project only after explicit source/destination classification. Source research records are not deleted during transfer. Existing destination authoritative documents must not be overwritten. Transfers must record source paths, hashes where practical, transformations, and destination paths. Cross-repository reads must strictly respect the Hard Working-Directory Safety Rule (explicit paths / `git -C`, zero working directory changes).

### Lesson 18 (Proposed) — Current-State Documentation Must Be Bound to Actual Repository State
Current-state documents must derive branch, HEAD, PR, CI, test and deployment claims from the repository/GitHub state at the time of writing. Historical reports must remain explicitly historical and must not be presented as current.

### Lesson 19 (Proposed) — Copy-Type Terminology Must Match Cryptographic Evidence
A file altered by line-ending, whitespace, metadata, path or content transformation must not be labelled an exact byte-for-byte copy. Preserve source/destination hashes and record transformations accurately (e.g. "Content copy with line-ending normalization"). Reserve "Exact byte-for-byte copy" strictly for files with matching cryptographic hashes.

### Lesson 20 (Proposed) — Verification Evidence Is Commit-Bound
Tests, clean-clone runs, CI results and runtime measurements must be tied to the exact repository commit/HEAD on which they were observed. Later documentation must not silently present earlier evidence as evidence for a newer commit; when code has not changed between commits, the preservation of executable state must be explicitly proven rather than assumed.
