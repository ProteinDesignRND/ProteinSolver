# Original Repository Forensic Inventory

**Document:** `docs/ORIGINAL_PROJECT_INVENTORY.md`  
**Repository:** `ProteinDesignRND/ProteinSolver`  
**Upstream Commit:** `69ef0965a3fc3bf191804035b539720a06e58ba6`  
**Audit Date:** 2026-09-29  

---

## 1. Classification Taxonomy

The forensic classification separates two orthogonal dimensions: **Disposition Category** (software engineering & packaging disposition) and **Verification Status** (execution & test verification in Milestone 1).

### Disposition Categories:
1. **`PRESERVED_UNCHANGED`:** Kept exactly as authored in upstream commit `69ef0965` (0 lines modified).
2. **`COMPATIBILITY_ADAPTED`:** Upstream source file preserved intact; modern runtime execution adapted via `compat/` without modifying upstream files.
3. **`APPLICATION_WRAPPED`:** Upstream capability exposed through modern FastAPI backend REST endpoints and React Web UI.
4. **`CLI/NOTEBOOK_RETAINED`:** Research notebook or script preserved in `notebooks/` or `scripts/` for CLI execution and reference.
5. **`EXTERNAL_DEPENDENCY`:** Upstream code preserved intact; execution depends on external tools/licenses (e.g., Rosetta, Modeller) or externally hosted training shards.
6. **`LEGACY_RETAINED_BUT_NOT_EXECUTABLE`:** Upstream legacy configuration preserved for provenance; operational workflows are superseded by modern equivalents (e.g. GitLab CI superseded by GitHub Actions, 2019 conda Dockerfiles superseded by native Python 3.11 / uv).

### Verification Statuses:
- **`FUNCTIONALLY_VERIFIED`:** Executed and verified against expected outputs, parameter counts, or hash invariants in our automated test suite or runtime.
- **`NOT_FUNCTIONALLY_VERIFIED`:** Retained for provenance, reference, or external execution; not directly executed in the automated test suite.
- **`NOT_VERIFIABLE_FROM_REPOSITORY`:** Execution depends on external resources (such as externally hosted training shards) not bundled in the repository.

---

## 2. Upstream Module Inventory (File / Subsystem Level — 24 Items)

> **Note on Abstraction Level:** This inventory catalogs 24 concrete file, module, and directory-level paths in the upstream repository. By contrast, [docs/ORIGINAL_PROJECT_PARITY.md](file:///D:/Projects/ProteinSolver/docs/ORIGINAL_PROJECT_PARITY.md) evaluates 22 functional capabilities and workflows at a capability level (e.g. grouping individual neural network operator modules).

| Module / Component | Upstream Path | Disposition | Verification Status | Modern Status & Adaptation |
| :--- | :--- | :---: | :---: | :--- |
| **ProteinNet GNN** | `proteinsolver/models/proteinnet.py` | `PRESERVED_UNCHANGED` | `FUNCTIONALLY_VERIFIED` | 4-block EdgeConv GNN (567,060 params). Executes forward passes on both CPU and CUDA. |
| **EdgeConv Module** | `proteinsolver/nn/edge_conv_mod.py` | `PRESERVED_UNCHANGED` | `FUNCTIONALLY_VERIFIED` | Custom PyG message-passing layer for edge-conditioned graph convolutions. |
| **Activation Functions** | `proteinsolver/nn/activation.py` | `PRESERVED_UNCHANGED` | `FUNCTIONALLY_VERIFIED` | Custom ELU / activation functions. |
| **Functional NN Ops** | `proteinsolver/nn/functional.py` | `PRESERVED_UNCHANGED` | `FUNCTIONALLY_VERIFIED` | GNN tensor operations and loss functions. |
| **Protein Design (CSP)** | `proteinsolver/utils/protein_design.py`| `COMPATIBILITY_ADAPTED` | `FUNCTIONALLY_VERIFIED` | Core iterative constraint satisfaction design algorithm (`design_sequence`) source preserved intact; modern application execution is compatibility-adapted via `compat/inference.py` on CPU. |
| **Protein Structure Utils**| `proteinsolver/utils/protein_structure.py`| `COMPATIBILITY_ADAPTED` | `FUNCTIONALLY_VERIFIED` | Defines `ProteinData` namedtuple; source preserved intact, `kmbio` dependencies adapted via BioPython in `compat/structure.py`. |
| **Scatter Shim** | `proteinsolver/utils/scatter.py` | `COMPATIBILITY_ADAPTED` | `FUNCTIONALLY_VERIFIED` | Source preserved intact; PyG 2.x removed `scatter_`, shimmed via `torch_scatter.scatter` in `compat/shims.py`. |
| **Sudoku Utils** | `proteinsolver/utils/sudoku.py` | `PRESERVED_UNCHANGED` | `FUNCTIONALLY_VERIFIED` | 9x9 Sudoku CSP solver and graph representation using the same GNN engine. |
| **Common Utils** | `proteinsolver/utils/common.py` | `PRESERVED_UNCHANGED` | `FUNCTIONALLY_VERIFIED` | Utility functions, seeds, tensor helpers. |
| **Compression Utils** | `proteinsolver/utils/compression.py` | `PRESERVED_UNCHANGED` | `FUNCTIONALLY_VERIFIED` | Gzip / serialization helpers. |
| **Model Scoring** | `proteinsolver/utils/model_scoring/` | `EXTERNAL_DEPENDENCY` | `NOT_FUNCTIONALLY_VERIFIED` | Upstream scoring wrappers preserved intact in `proteinsolver/utils/model_scoring/`; require external standalone Rosetta binaries and/or Modeller. |
| **Protein Datasets** | `proteinsolver/datasets/protein.py` | `PRESERVED_UNCHANGED` | `FUNCTIONALLY_VERIFIED` | PyG Dataset classes for protein contact graphs (`row_to_data`, `transform_edge_attr`). |
| **Sudoku Datasets** | `proteinsolver/datasets/sudoku.py` | `PRESERVED_UNCHANGED` | `FUNCTIONALLY_VERIFIED` | PyG Dataset classes for Sudoku boards. |
| **N-Queens Dataset Stub** | `proteinsolver/datasets/nqueens.py` | `PRESERVED_UNCHANGED` | `NOT_FUNCTIONALLY_VERIFIED` | Upstream placeholder abstract Dataset class (`class NQueensDataset(Dataset): ...`). Preserved intact. |
| **Graph-Labeling Dataset Stub** | `proteinsolver/datasets/graph_labeling.py`| `PRESERVED_UNCHANGED` | `NOT_FUNCTIONALLY_VERIFIED` | Upstream placeholder abstract Dataset class (`class GraphLabelingDataset(Dataset): ...`). Preserved intact. |
| **Legacy Voila Dashboard**| `proteinsolver/dashboard/` | `LEGACY_RETAINED_BUT_NOT_EXECUTABLE` | `NOT_FUNCTIONALLY_VERIFIED` | 2019 ipywidgets / Voila interactive dashboard preserved for provenance; modernized by `apps/frontend/` (React 19 + TypeScript + Vite). |
| **Example PDB Inputs** | `proteinsolver/data/inputs/` | `PRESERVED_UNCHANGED` | `FUNCTIONALLY_VERIFIED` | 6 real structure fixtures (`1n5uA03.pdb`, `3fndA02.pdb`, `4beuA02.pdb`, etc.). |
| **Published Checkpoint** | `data/e53-s1952148-d93703104.state` | `PRESERVED_UNCHANGED` | `FUNCTIONALLY_VERIFIED` | Checkpoint bytes preserved; SHA-256 verified (`1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727`); deterministic key translation applied during loading by `compat/checkpoint.py` with 0 missing keys, 0 unexpected keys, and 567,060 parameters. |
| **Upstream Tests** | `tests/` | `PRESERVED_UNCHANGED` | `FUNCTIONALLY_VERIFIED` | Original test suite (tests `ProteinNet`, `sudoku`, `functional`). |
| **Notebooks (Training)** | `notebooks/04_protein_train*.ipynb` | `CLI/NOTEBOOK_RETAINED` | `NOT_VERIFIABLE_FROM_REPOSITORY` | Full training workflows are retained as reference notebooks; full execution depends on the externally hosted training shards. |
| **Notebooks (Sudoku)** | `notebooks/04_sudoku_train*.ipynb` | `CLI/NOTEBOOK_RETAINED` | `NOT_VERIFIABLE_FROM_REPOSITORY` | Sudoku training and demonstration notebooks preserved in `notebooks/`. |
| **Notebooks (Design Demo)**| `notebooks/06_design_proteins.ipynb` | `APPLICATION_WRAPPED` | `FUNCTIONALLY_VERIFIED` | Notebook design workflow directly realized in `apps/backend/` and `apps/frontend/`. |
| **CI Configuration** | `.gitlab-ci.yml`, `.ci/` | `LEGACY_RETAINED_BUT_NOT_EXECUTABLE` | `NOT_FUNCTIONALLY_VERIFIED` | Upstream author used GitLab CI; preserved for provenance; modern operational CI is handled by GitHub Actions (`.github/workflows/ci.yml`). |
| **Binder Configuration**| `binder/` | `LEGACY_RETAINED_BUT_NOT_EXECUTABLE` | `NOT_FUNCTIONALLY_VERIFIED` | Original 2019 cloud Binder environment preserved for provenance; superseded by local virtual environment and full-stack application. |
| **C Extension Source** | `scripts/sugen.c` | `PRESERVED_UNCHANGED` | `NOT_FUNCTIONALLY_VERIFIED` | Original C source for generating Sudoku puzzles. |

---

## 3. Summary of Upstream Retention
- **Total Upstream Files Preserved:** 100% of upstream files remain in the repository.
- **Upstream Code Modifications:** 0 lines modified in `proteinsolver/`.
- **Modernization Strategy:** All compatibility bridges are isolated in `compat/`, and all user-facing features are isolated in `apps/`.
