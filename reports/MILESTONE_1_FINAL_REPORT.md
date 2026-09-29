# ProteinSolver Milestone 1 — Forensic Audit, Correction & Final Verification Report

**Status Classification:** `MILESTONE_1_FUNCTIONALLY_COMPLETE_WITH_LIMITATIONS`
**Governance State:** `PENDING_HUMAN_MERGE`
**Date:** September 29, 2026
**Environment:** Windows 11, Python 3.11.9, PyTorch 2.6.0+cu124, PyG 2.8.0.post1, Node v24.18.0, npm 11.16.0
**Implementation Repository:** `https://github.com/ProteinDesignRND/ProteinSolver` (`ProteinDesignRND/ProteinSolver`)
**Research Repository (Firewalled):** `https://github.com/ProteinDesignRND/ProteinDesign` (`ProteinDesignRND/ProteinDesign`)
**Feature Branch:** `feature/milestone-1-full-implementation`
**Current Pushed Branch HEAD:** `4b0e86f90e5dbfeb58ad7bf38c5f9e0fd117bf12`
**Target Branch main HEAD:** `69ef0965a3fc3bf191804035b539720a06e58ba6`
**Pull Request:** [PR #1 (Open)](https://github.com/ProteinDesignRND/ProteinSolver/pull/1)


---

## 1. Executive Summary

Milestone 1 has delivered a complete, runnable, and independently verified reproduction of Alexey Strokach's *Cell Systems* 2020 ProteinSolver graph neural network system under the `ProteinDesignRND` organization.

Following a thorough forensic audit, all prior factual, architectural, terminology, and reproducibility inconsistencies have been permanently resolved:
- **Upstream Source Frozen:** 100% of the upstream `proteinsolver/` package from scientific baseline commit `69ef0965` is preserved unchanged (0 files modified).
- **Exact Model Architecture:** Confirmed `ProteinNet` has a hidden dimensionality of **128** (not 162) and contains exactly **567,060** parameters matching the published checkpoint.
- **Compatibility Issues:** Exactly **7** compatibility issues were identified, resolved in `compat/`, and regression-tested, including a fail-loud Windows `fcntl` locking stub and a modern BioPython structure extraction engine.
- **Native-Sequence Leak Invariant:** Enforced design-path input invariant (`data.x = 20`, `data.y = None`, native sequence rejected by design endpoint) protected by automated regression tests.
- **Calibrated Result Language:** Single-target recovery on `1n5uA03` is strictly characterized as a *"previously validated single-target all-masked integration result (41.30% native sequence identity, 38/92 residues)"*, avoiding generalized benchmark or published MAP claims.
- **Genuine Clean-Clone Reproducibility:** Verified in a brand-new, isolated temporary directory with a clean Python 3.11 virtual environment completely free of cross-repository dependencies (32/32 tests passed, npm ci + build passed, real integration inference passed).
- **Scientific Firewall:** The `ProteinDesignRND/ProteinDesign` research repository remains 100% untouched. Zero benchmark candidates, zero folding evaluations, and zero test-set evaluations were performed.
- **Human Merge Gate:** Pull Request #1 is OPEN targeting `main` pending human review and approval.

---

## 2. Upstream Lineage & Provenance Audit

| Parameter | Value | Verification Evidence |
| :--- | :--- | :--- |
| **Upstream Repository** | `https://github.com/ostrokach/proteinsolver` | Upstream baseline |
| **Upstream Acquisition HEAD** | `69ef0965a3fc3bf191804035b539720a06e58ba6` | Verified via `git ls-remote upstream refs/heads/master` |
| **Scientific Reference Commit** | `69ef0965a3fc3bf191804035b539720a06e58ba6` | Identical to acquisition HEAD; full upstream history preserved |
| **Fork Creation Method** | GitHub Fork (`gh repo fork ostrokach/proteinsolver --org ProteinDesignRND`) | Complete Git commit history retained |
| **Upstream Push Safety** | `git remote set-url --push upstream no_push` | Push URL configured to `no_push` |
| **License** | MIT License | Preserved; upstream copyright notices intact |

---

## 3. Strict Upstream File Integrity Audit

A full Git diff was executed against scientific baseline commit `69ef0965a3fc3bf191804035b539720a06e58ba6`:

```
git diff 69ef0965..HEAD --name-status
```

### File Classification Results:
- `proteinsolver/**`: **0 files modified**. The upstream package source code is 100% frozen.
- `tests/nn/**` and `tests/utils/**`: **0 files modified**. Upstream unit tests preserved.
- Root repository baseline files:
  1. `.gitignore`: **Class B (Legitimate downstream repository metadata)**. Added `!apps/frontend/index.html` and modern IDE ignores.
  2. `README.md`: **Class B (Legitimate downstream repository metadata)**. Updated to provide comprehensive modern setup, architecture, and provenance instructions.
  3. `setup.py`: **Class C (Legitimate compatibility change)**. Updated file reader with `encoding="utf-8", errors="replace"` to prevent Windows cp1252 charmap decoding crashes on README UTF-8 characters.

---

## 4. Original Upstream Project Parity Matrix

The upstream project inventory was audited across all 22 meaningful capabilities and documented in `docs/ORIGINAL_PROJECT_PARITY.md`:

| # | Upstream Component | Classification | Current Disposition |
| :--- | :--- | :--- | :--- |
| 1 | `ProteinNet` Core GNN Model | `PRESERVED_UNCHANGED` | Packaged in `proteinsolver/models/proteinnet.py`, wrapped by `compat/checkpoint.py` (567,060 params, hidden dim 128) |
| 2 | EdgeConv GNN Modules | `PRESERVED_UNCHANGED` | `proteinsolver/nn/` EdgeConv modules executed natively |
| 3 | Functional/Activation Utilities | `PRESERVED_UNCHANGED` | Tested in `tests/nn/test_functional.py` |
| 4 | Protein Datasets & Transforms | `PRESERVED_UNCHANGED` | `proteinsolver/datasets/protein.py` preserved and active |
| 5 | Sudoku Datasets & Utilities | `PRESERVED_UNCHANGED` | Tested in `tests/utils/test_sudoku.py` (8 parameterized tests pass) |
| 6 | N-Queens Dataset Stub | `PRESERVED_UNCHANGED` | Upstream placeholder abstract `Dataset` class preserved intact in `proteinsolver/datasets/nqueens.py` |
| 7 | Graph-Labeling Dataset Stub | `PRESERVED_UNCHANGED` | Upstream placeholder abstract `Dataset` class preserved intact in `proteinsolver/datasets/graph_labeling.py` |
| 8 | Protein Design Iterative CSP | `PRESERVED_UNCHANGED` | `proteinsolver.utils.protein_design.design_sequence` wrapped by `compat/inference.py` |
| 9 | Protein Demo Workflow | `APPLICATION_WRAPPED` | Modernized into interactive FastAPI + React application (`apps/backend/` + `apps/frontend/`) |
| 10 | Protein Analysis Notebook | `CLI/NOTEBOOK_RETAINED` | Research notebook preserved in `notebooks/06_protein_analysis.ipynb` |
| 11 | Sudoku Demo Workflow | `CLI/NOTEBOOK_RETAINED` | Retained and executable via `proteinsolver.utils.sudoku` |
| 12 | Sudoku Analysis Workflow | `CLI/NOTEBOOK_RETAINED` | Research notebook preserved in `notebooks/06_sudoku_analysis.ipynb` |
| 13 | Training Workflows | `CLI/NOTEBOOK_RETAINED` | Full GNN training pipelines preserved in `notebooks/04_protein_train*.ipynb`; documented in `docs/KNOWN_LIMITATIONS.md` |
| 14 | Model Selection Workflows | `CLI/NOTEBOOK_RETAINED` | Checkpoint validation loss tracking in `notebooks/05_select_best_model.ipynb`; single-target diagnostic wrapped in API |
| 15 | Model Scoring Utilities | `CLI/NOTEBOOK_RETAINED` | Legacy scoring wrappers in `proteinsolver/utils/` (requires external PyRosetta / Modeller) |
| 16 | Pretrained Protein Checkpoint | `FUNCTIONALLY_VERIFIED` | 2.28 MB state-dict (`data/e53-s1952148-d93703104.state`), SHA-256 verified, key mapping in `compat/checkpoint.py` |
| 17 | External Training Datasets | `EXTERNAL_DEPENDENCY` | Multi-gigabyte external datasets documented at `http://deep-protein-gen.data.proteinsolver.org/` |
| 18 | Docker Support | `LEGACY_RETAINED_BUT_NOT_EXECUTABLE` | 2019 Conda/GitLab CI Dockerfiles retained for provenance; modern local venv standardized |
| 19 | Binder Support | `LEGACY_RETAINED_BUT_NOT_EXECUTABLE` | Legacy Binder environment retained for provenance |
| 20 | Original Unit Tests | `FUNCTIONALLY_VERIFIED` | All compatible upstream unit tests pass cleanly in test suite |
| 21 | C & Shell Utilities | `PRESERVED_UNCHANGED` | Standalone C Sudoku generator (`scripts/sugen.c`) and shell helpers preserved |
| 22 | Legacy CI Configuration | `PRESERVED_UNCHANGED` | Upstream `.gitlab-ci.yml` preserved; modern CI active via GitHub Actions (`.github/workflows/ci.yml`) |

---

## 5. Compatibility Layer Forensics (7 Issues Resolved)

The compatibility layer (`compat/`) resolves exactly **7** distinct historical incompatibilities without modifying the upstream scientific package:

1. **Windows POSIX `fcntl` stub (`compat/shims.py`):**
   POSIX file locking is absent on Windows. Shims create a dummy `fcntl` module with standard constants (`LOCK_EX`, `LOCK_SH`, `LOCK_UN`, `LOCK_NB`). To prevent silent race conditions, `fcntl.flock` and `fcntl.lockf` explicitly raise `NotImplementedError` rather than pretending locking succeeded.
2. **Cleanroom BioPython Structure Parser (`compat/structure.py`):**
   The legacy `kmbio` / `kmtools` dependencies are abandoned. A modern BioPython-based parser computes heavy-atom inter-residue distance matrices ($r < 12.0$ Å), extracts coordinates, builds PyG edge indices, and determines edge attributes.
3. **PyTorch Geometric 2.x `scatter_` In-Place Shim (`compat/shims.py`):**
   The in-place `torch_geometric.utils.scatter_` operator was removed in PyG 2.x. A shim intercepts calls and delegates to `torch_scatter.scatter(src, index, dim=dim, out=out, reduce=reduce)`.
4. **PyG Data & Batch Collation Adaptation (`compat/inference.py`):**
   Modern PyG 2.8 `Batch.from_data_list` requires uniform tensor keys and handles slicing differently from PyG 1.x. The adapter ensures homogeneous tensor dictionaries prior to collation.
5. **Checkpoint State-Dict Layer Key Mapping (`compat/checkpoint.py`):**
   The published checkpoint (`e53-s1952148-d93703104.state`) uses training-time keys (`graph_conv_0.`) whereas packaged `ProteinNet` defines `graph_conv_1.`. The loader deterministically maps keys and validates that all 567,060 parameters load with 0 missing and 0 unexpected keys.
6. **PyTorch 2.6 Cross-Device Indexing Standardization (`compat/inference.py`):**
   Iterative CSP sequence design performs sequential scalar index assignments (`data.x[best_idx] = best_val`). Under PyTorch 2.6 on CUDA, scalar cross-device indexing triggers asynchronous device-side assert errors. The compatibility inference engine standardizes design execution to CPU.
7. **`ruamel.yaml` 0.18+ API Migration (`compat/shims.py`):**
   Replaced deprecated `ruamel.yaml.safe_load(...)` with `YAML(typ='safe', pure=True).load`.

---

## 6. Model Architecture & Checkpoint Facts

Empirical verification from the checkpoint tensors and model code confirms:

- **Model Class Name:** `ProteinNet`
- **Application Product Name:** `ProteinSolver`
- **Architecture:** 4-block EdgeConv Residual Graph Neural Network
- **Embedding Dimensions:**
  - `embed_x`: `(21, 128)` — 20 standard amino acids + 1 mask token (token 20) mapped to **128-dimensional** node embeddings.
  - `embed_adj`: `(128, 2)` — Edge distance and direction attributes mapped to **128-dimensional** edge embeddings.
  - `graph_conv` blocks: 4 sequential residual blocks with EdgeConv message-passing and batch normalization.
  - `linear_out`: `(20, 128)` — Final linear projection from **128-dimensional** hidden representations to 20 amino acid logits.
- **Exact Parameter Count:** **567,060** parameters (empirical count: 567,060; state-dict tensors: 567,060).
- **Checkpoint File:** `data/e53-s1952148-d93703104.state` (2,278,071 bytes)
- **Checkpoint SHA-256:** `1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727`

---

## 7. Native-Sequence Leak Protection

- **Invariant:** During design mode, `data.x` is initialized with mask token 20 for all residues, `data.y` is explicitly set to `None`, and the design endpoint strictly rejects any reference sequence input.
- **Verification:** Tested in `tests/test_leak_regression.py`.
- **Diagnostic Separation:** The native sequence is only accepted by the separate `/api/diagnostic` endpoint for retrospective sequence identity computation.

---

## 8. Single-Target Integration Result

- **Target Structure:** `1n5uA03` (CATH domain from PDB 1N5U, Chain A, 92 amino acids).
- **Execution Mode:** All-masked MAP greedy inverse folding on CPU.
- **Result:** **38 / 92 residues** match the native sequence (**41.30% native sequence identity**).
- **Runtime:** Typical CPU runtime ~1.5–2.1 seconds (e.g. 1.52s in initial benchmark, 1.77s in parity log, 2.09s in local verification run). Runtime is run-dependent and varies with CPU platform and system load.
- **Characterization:** This is a *previously validated single-target all-masked integration result* (38/92 = 41.30% native sequence identity). It is NOT claimed to be a generalized benchmark, published baseline, or proof of fold-wide recovery. Training set membership of `1n5uA03` is not verifiable from accessible metadata without downloading the external multi-gigabyte training shards.

---

## 9. Genuine Isolated Clean-Clone Verification

To satisfy clean-clone independence and commit-bound verification standards (Lesson 6 and Proposed Lesson 20), an audit of post-`0b5cbb9` commits was conducted. Because modifications to `apps/backend/service.py`, `apps/backend/main.py`, `apps/backend/schemas.py`, `compat/inference.py`, `tests/test_backend_api.py`, `apps/frontend/src/App.tsx`, and `.github/workflows/ci.yml` occurred after commit `0b5cbb9`, the prior clean-clone evidence was determined to be insufficient.

Consequently, a fresh, true remote clean-clone verification was executed from scratch directly on branch commit `4b0e86f90e5dbfeb58ad7bf38c5f9e0fd117bf12`:

1. **Remote Clone:** Cloned `feature/milestone-1-full-implementation` from GitHub into a fresh, isolated temporary scratch directory (`scratch/clean_clone_verify`) outside both project repositories.
2. **Working Tree Verification:** Verified clean working tree at commit `4b0e86f90e5dbfeb58ad7bf38c5f9e0fd117bf12`.
3. **Isolated Python Environment:** Created an isolated Python 3.11 virtual environment (`.venv`) using `uv venv`.
4. **Environment Isolation Gate:** Verified that `sys.path` contained 0 references to `Protein Design` or any other project directory.
5. **Authoritative Dependency Installation:** Installed dependencies strictly via `uv pip install -r requirements.txt` and `uv pip install -e . --no-deps`.
6. **Frontend Dependency & Production Build:** In `apps/frontend/`, executed `npm ci` and `npm run build` (23 modules bundled, 0 TypeScript or bundling errors).
7. **Automated Pytest Suite:** Executed `pytest tests/ -v`: **32 passed**, 0 failed, in 11.23 seconds.
8. **Real Single-Target Integration Inference:** Executed real MAP greedy design on `1n5uA03.pdb` using the loaded checkpoint:
   `INFERENCE_SUCCESS: Length=92, Matches=38/92, Recovery=41.30%, Runtime=1.75s`.
9. **Scratch Teardown:** Completely removed the temporary clone and its virtual environment.

**Commit-Bound Applicability Statement:** Current-head clean-clone reproducibility is empirically verified on commit `4b0e86f90e5dbfeb58ad7bf38c5f9e0fd117bf12`. Subsequent release-closure changes are strictly documentation and setup calibrations (`docs/SETUP.md` `npm install` -> `npm ci`, `AGENT_RULES_AND_LESSONS.md` terminology, and report synchronization) with zero changes to executable, runtime, package, model, or CI files.

---

## 10. Automated Test Suite Summary

The automated test suite contains **32 tests** across 10 test modules:

| Test Module | Tests | Focus Area | Status |
| :--- | :--- | :--- | :--- |
| `tests/nn/test_functional.py` | 1 | Upstream Sparse Multi-Head Attention forward pass | **PASSED** |
| `tests/test_attributes.py` | 2 | Upstream package attributes (`__version__`, `__main__`) | **PASSED** |
| `tests/utils/test_sudoku.py` | 8 | Upstream Sudoku puzzle validation (solved & invalid) | **PASSED** |
| `tests/test_compat_shims.py` | 3 | Windows `fcntl` fail-loud stub, `kmtools` stub, PyG `scatter_` shim | **PASSED** |
| `tests/test_compat_structure.py` | 2 | BioPython structure parsing, chain selection, contact graph | **PASSED** |
| `tests/test_model_checkpoint.py` | 3 | Checkpoint SHA-256, 567,060 parameter count, forward pass | **PASSED** |
| `tests/test_all_masked_design.py` | 2 | Deterministic greedy MAP design, stochastic seed determinism | **PASSED** |
| `tests/test_leak_regression.py` | 2 | Design-path zero-leakage invariant, reference sequence immunity | **PASSED** |
| `tests/test_backend_api.py` | 8 | Health, exact model metadata, examples, validation, design, diagnostic | **PASSED** |
| `tests/test_integration_1n5u.py` | 1 | Single-target all-masked integration reproduction (41.30% recovery) | **PASSED** |
| **Total** | **32** | **Full automated coverage** | **32 PASSED (0 failed)** |

---

## 11. Application Architecture & Verification

- **Backend:** FastAPI service in `apps/backend/`. Unweakened API contract verified: `model_name="ProteinSolver"`, `model_class="ProteinNet"`, `architecture="4-block EdgeConv Residual GNN"`.
- **Frontend:** React 19 + TypeScript + Vite interactive dark-mode interface in `apps/frontend/`. Built with `tsc -b && vite build`.
- **Confidence Visualization:** Confidence bands in the UI (High $\ge$ 70%, Moderate 40–69%, Low < 40%) are documented strictly as **display-only visualization bands** representing uncalibrated model selection probabilities.
- **Browser Automation Classification:**
  - `FRONTEND_BUILD_VERIFIED`: Built via Vite with 0 TypeScript/bundling errors.
  - `BACKEND_INTEGRATION_VERIFIED`: All 8 REST endpoints verified via FastAPI TestClient.
  - `BROWSER_E2E_NOT_AUTOMATED`: Automated headless browser binaries are not installed in the local environment; interactive browser execution is performed via manual mentor demo workflow.

---

## 12. Scientific Firewall Confirmation

The scientific research repository `ProteinDesignRND/ProteinDesign` remains **100% untouched**:
- 0 candidate sequences generated for scientific experiments.
- 0 benchmark runs (no E1, no TS50, no ProteinMPNN evaluations).
- 0 ESMFold or AlphaFold2 folding evaluations.
- Historical reference clone at `external/proteinsolver-original` remains frozen at commit `69ef0965`.

---

## 13. Known Limitations

As documented in `docs/KNOWN_LIMITATIONS.md`:
1. **Single-Target Integration Check vs. Benchmark:** Target `1n5uA03` (92 AA) is an integration sanity fixture. Its 41.30% recovery (38/92 residues) reproduces the project's previously validated single-target all-masked integration result. It is NOT a generalized benchmark, published baseline, or proof of multi-target recovery across protein folds. Furthermore, training set membership of `1n5uA03` has not been independently verified against the external multi-gigabyte training shards. Systematic benchmarking is reserved exclusively for the research repository (`ProteinDesignRND/ProteinDesign`).
2. **CPU Inference Default:** Iterative CSP sequence generation is standardized to CPU in the compatibility layer to prevent PyTorch 2.6 CUDA scalar indexing asserts.
3. **Unsupported Windows POSIX File Locking:** POSIX `fcntl` file locking is unsupported on Windows; calls raise `NotImplementedError` rather than silently pretending locks exist.
4. **Retired Legacy RCSB/PDB Fetching Path:** Upstream network fetching methods relying on defunct URLs are retired; user uploads or local files are used.
5. **Display-Only Confidence Bands:** Residue confidence bands are uncalibrated model selection probabilities and should not be used as biological thresholds.
6. **External Licensed Scoring Dependencies:** Upstream scoring scripts in `notebooks/16_david_analysis/` require external licensed installations of PyRosetta and Quark.
7. **External Multi-GB Training Dataset Dependency:** Full training datasets (multi-gigabyte shards) are hosted externally and documented for reference; full training workflows are retained as legacy.
8. **Browser E2E Testing Not Automated:** Automated test suites cover unit, model, compat, and backend API suites (32 tests across 10 modules) plus frontend TypeScript/Vite production build; browser-based end-to-end UI interaction is not automated in CI.

---

## 14. Governance & Human Merge Requirement

- **Pull Request:** [ProteinDesignRND/ProteinSolver PR #1](https://github.com/ProteinDesignRND/ProteinSolver/pull/1)
- **Branch Protection:** Active ruleset requires 1 approving review, squash merge, linear history, and signed commits.
- **Human Merge Gate:** In accordance with team governance rules and the strict human-merge gate, PR #1 has NOT been autonomously merged. Human review and approval remain required.
- **Post-Merge Transition:** Once PR #1 is approved and merged into `main` by a human reviewer, the repository will be classified as `MILESTONE_1_READY_FOR_MENTOR_DEMO`.

---

## 15. Conclusion & Verification Summary

| Gate / Requirement | Requirement Standard | Verified Status |
| :--- | :--- | :--- |
| **Upstream Lineage** | Fork acquisition HEAD & scientific reference commit explicit | **VERIFIED** (`69ef0965`) |
| **File Integrity** | Upstream package source frozen; only legitimate changes | **VERIFIED** (0 files in `proteinsolver/` modified) |
| **Parity Matrix** | 22 upstream capabilities accounted for honestly | **VERIFIED** (`docs/ORIGINAL_PROJECT_PARITY.md`) |
| **Compatibility Layer** | Exactly 7 issues addressed without silent failures | **VERIFIED** (7 issues resolved & tested) |
| **Model Facts** | Hidden dim = 128, parameters = 567,060 | **VERIFIED** (Empirical & checkpoint match) |
| **Native Leak Invariant** | Mask token 20, y=None, design rejects native sequence | **VERIFIED** (Regression tested) |
| **Result Language** | Single-target 41.30% integration result (not benchmark) | **VERIFIED** (Calibrated everywhere) |
| **Test Suite** | Full suite passes without weakened assertions | **VERIFIED** (32/32 passed) |
| **Frontend Build** | TypeScript compilation and Vite build pass | **VERIFIED** (0 errors) |
| **Clean Clone** | Brand-new isolated environment with 0 cross-repo deps | **VERIFIED** (100% passed in isolated clean clone) |
| **Research Firewall** | `ProteinDesign` research repository untouched | **VERIFIED** (100% clean) |
| **Governance** | PR #1 open, human review required | **VERIFIED** (`PENDING_HUMAN_MERGE`) |
