# Durable Memory: Agent Rules, Scientific Lessons, & Architecture Decisions

This document encodes mandatory lessons learned across audits, historical reproductions, and production modernizations for the **ProteinSolver Milestone 1** implementation repository under `ProteinDesignRND/ProteinSolver`. Future agents and contributors must consult and adhere strictly to these principles.

---

## 1. Core Methodological Lessons

### Lesson A — Never Confuse E0 Runtime Verification with Milestone 1 Completion
- **Context:** Previous engineering passes verified checkpoint loading and single-target inference in a notebook/script environment.
- **Rule:** Milestone 1 requires full application delivery: official upstream repository provenance, runnable modernization on modern Python/PyTorch/PyG, isolated compatibility layer (`compat/`), production FastAPI backend (`apps/backend/`), interactive React+TypeScript frontend (`apps/frontend/`), end-to-end integration tests, clean-clone verification, and teammate workflow protection. Inference execution alone is insufficient.

### Lesson B — Strict Upstream Source Provenance & Immutability
- **Context:** Historical upstream commit `69ef0965a3fc3bf191804035b539720a06e58ba6` by Alexey Strokach represents the published *Cell Systems* 2020 foundation.
- **Rule:** The original `proteinsolver/` package must remain untouched. All modernizations, monkeypatches, and bridges must reside strictly in `compat/` or `apps/`. Upstream git history is preserved completely via GitHub Fork.

### Lesson C — Zero Native Sequence Leakage Invariant
- **Context:** An earlier audit discovered that supplying native sequence labels in `data.y` or unmasked `data.x` tokens creates an illusion of 100% sequence recovery, masquerading reference scoring as inverse folding.
- **Rule:** In **Design Mode**:
  1. `data.x` is initialized strictly to the mask token (`20` for all residues).
  2. `data.y` is explicitly deleted/stripped from the PyG batch.
  3. No ground-truth sequence is accepted or consumed by the design pipeline.
  4. Diagnostic native sequence comparison is segregated into an explicitly separate evaluation endpoint (`/api/diagnostic`) with prominent disclaimers that it is an integration check, not a generalized benchmark.

### Lesson D — Preserve Original Scientific Architecture
- **Context:** Alexey Strokach's 4-block EdgeConv GNN architecture with 567,060 parameters is the published scientific artifact.
- **Rule:** Do not casually substitute or rewrite the neural network. Preserve the exact parameter count, layer definitions, distance cutoffs ($r < 12.0$ Å), and CSP formulation.

---

## 2. Modern Runtime & Compatibility Solutions (`compat/`)

| Compatibility Issue | Root Cause | Modern Resolution | Validation Evidence |
| :--- | :--- | :--- | :--- |
| **Windows POSIX `fcntl`** | Upstream code unconditionally imports Unix `fcntl` for flock operations | In `compat/shims.py`, register a dummy `fcntl` module with `flock`, `lockf`, and `LOCK_*` constants | Clean import on Windows 11 without native compilation errors |
| **Obsolete `kmbio` / `kmtools`** | Abandoned 2018–2019 dependencies fail to build on Python 3.11 | Stubs registered in `compat/shims.py`; cleanroom BioPython PDB parser implemented in `compat/structure.py` | Accurate coordinate extraction, heavy-atom distance matrices, and residue metadata |
| **PyG 2.x `scatter_` removal** | `torch_geometric.utils.scatter_` in-place operator was removed in PyG 2.x | Shim registered in `compat/shims.py` redirecting to `torch_scatter.scatter` | `tests/nn/test_functional.py` passes completely |
| **Checkpoint State-Dict Keys** | Published checkpoint uses training prefixes (`graph_conv_0.`) whereas packaged `ProteinNet` expects `graph_conv_1.` | Layer key translator in `compat/checkpoint.py` maps legacy prefixes deterministically | Exact parameter match (567,060 params) and zero missing/unexpected keys |
| **PyG Batch Behavioral Changes** | PyG 2.8 handles batch attributes differently than PyG 1.x | Explicit `Batch.from_data_list([data])` with device assignment | Clean execution of forward pass and CSP design sequence |
| **PyTorch 2.6 Cross-Device Indexing** | Upstream `design_sequence` boolean tensor indexing triggers a CUDA assertion in PyTorch 2.6 | Standardize CSP execution on CPU (`device="cpu"`) | Flawless, stable design execution in ~1.7s per 92-residue domain |
| **`ruamel.yaml` 0.18+ Deprecation** | Modern `ruamel.yaml` deprecated `yaml.safe_load(...)` | Shim registered in `compat/shims.py` routing `safe_load` to `YAML(typ='safe', pure=True).load` | Upstream Sudoku tests collect and execute cleanly |

---

## 3. Engineering & Workflow Governance

### Anti-Infinite Debug Loop Policy
- Limit: Maximum 3 coherent attempts for any single underlying issue.
- If unresolved after 3 attempts: classify as `BLOCKED`, document root cause, record evidence, preserve working state, and proceed with independent deliverables.

### Objective Status Classifications
- `IMPLEMENTED`: Code is written and present.
- `VERIFIED`: Automated unit/integration tests validate correctness.
- `FUNCTIONALLY REPRODUCED`: Execution matches published scientific outputs within documented tolerances.
- `COMPATIBILITY ADAPTED`: Legacy incompatibilities bridged without touching upstream core.
- `NOT VERIFIED`: Capability present but unvalidated locally.
- `BLOCKED`: Dependency or upstream limitation prevents local execution.
