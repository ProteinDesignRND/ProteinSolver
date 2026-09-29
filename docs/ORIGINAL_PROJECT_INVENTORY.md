# Original Repository Forensic Inventory

**Document:** `docs/ORIGINAL_PROJECT_INVENTORY.md`  
**Repository:** `ProteinDesignRND/ProteinSolver`  
**Upstream Commit:** `69ef0965a3fc3bf191804035b539720a06e58ba6`  
**Audit Date:** 2026-09-29  

---

## 1. Classification Taxonomy

Every component in the upstream project is classified into one of the following operational categories:

1. **PRESERVED_UNCHANGED:** Kept exactly as authored in upstream commit `69ef0965`.
2. **COMPATIBILITY_ADAPTED:** Upstream source file preserved intact; modern runtime execution adapted via `compat/` without modifying upstream files.
3. **APPLICATION_WRAPPED:** Upstream capability exposed through modern FastAPI backend REST endpoints and React Web UI.
4. **CLI/NOTEBOOK_RETAINED:** Research notebook or script preserved in `notebooks/` or `scripts/` for CLI execution and reference.
5. **EXTERNAL_DEPENDENCY:** Upstream code preserved intact; execution depends on external tools/licenses (e.g., Rosetta, Modeller) or external multi-gigabyte datasets.
6. **LEGACY_RETAINED_BUT_NOT_EXECUTABLE:** Upstream legacy configuration preserved for provenance; operational workflows are superseded by modern equivalents (e.g. GitLab CI superseded by GitHub Actions, 2019 conda Dockerfiles superseded by native Python 3.11 / uv).
7. **FUNCTIONALLY_VERIFIED:** Executed and verified against expected outputs, parameter counts, or hash invariants in our automated test suite or runtime.

---

## 2. Upstream Module Inventory

| Module / Component | Upstream Path | Classification | Modern Status & Adaptation |
| :--- | :--- | :---: | :--- |
| **ProteinNet GNN** | `proteinsolver/models/proteinnet.py` | `PRESERVED_UNCHANGED` | 4-block EdgeConv GNN (567,060 params). Executes forward passes on both CPU and CUDA. |
| **EdgeConv Module** | `proteinsolver/nn/edge_conv_mod.py` | `PRESERVED_UNCHANGED` | Custom PyG message-passing layer for edge-conditioned graph convolutions. |
| **Activation Functions** | `proteinsolver/nn/activation.py` | `PRESERVED_UNCHANGED` | Custom ELU / activation functions. |
| **Functional NN Ops** | `proteinsolver/nn/functional.py` | `PRESERVED_UNCHANGED` | GNN tensor operations and loss functions. |
| **Protein Design (CSP)** | `proteinsolver/utils/protein_design.py`| `COMPATIBILITY_ADAPTED` | Core iterative constraint satisfaction design algorithm (`design_sequence`) source preserved intact; modern application execution is compatibility-adapted via `compat/inference.py` on CPU. |
| **Protein Structure Utils**| `proteinsolver/utils/protein_structure.py`| `COMPATIBILITY_ADAPTED` | Defines `ProteinData` namedtuple; source preserved intact, `kmbio` dependencies adapted via BioPython in `compat/structure.py`. |
| **Scatter Shim** | `proteinsolver/utils/scatter.py` | `COMPATIBILITY_ADAPTED` | Source preserved intact; PyG 2.x removed `scatter_`, shimmed via `torch_scatter.scatter` in `compat/shims.py`. |
| **Sudoku Utils** | `proteinsolver/utils/sudoku.py` | `PRESERVED_UNCHANGED` | 9x9 Sudoku CSP solver and graph representation using the same GNN engine. |
| **Common Utils** | `proteinsolver/utils/common.py` | `PRESERVED_UNCHANGED` | Utility functions, seeds, tensor helpers. |
| **Compression Utils** | `proteinsolver/utils/compression.py` | `PRESERVED_UNCHANGED` | Gzip / serialization helpers. |
| **Model Scoring** | `proteinsolver/utils/model_scoring/` | `EXTERNAL_DEPENDENCY` | Upstream scoring wrappers preserved intact in `proteinsolver/utils/model_scoring/`; require external standalone Rosetta binaries and/or Modeller. |
| **Protein Datasets** | `proteinsolver/datasets/protein.py` | `PRESERVED_UNCHANGED` | PyG Dataset classes for protein contact graphs (`row_to_data`, `transform_edge_attr`). |
| **Sudoku Datasets** | `proteinsolver/datasets/sudoku.py` | `PRESERVED_UNCHANGED` | PyG Dataset classes for Sudoku boards. |
| **N-Queens Datasets** | `proteinsolver/datasets/nqueens.py` | `PRESERVED_UNCHANGED` | PyG Dataset classes for N-Queens constraint problems. |
| **Graph Labeling** | `proteinsolver/datasets/graph_labeling.py`| `PRESERVED_UNCHANGED` | Generic graph coloring/labeling problem dataset. |
| **Legacy Voila Dashboard**| `proteinsolver/dashboard/` | `LEGACY_RETAINED_BUT_NOT_EXECUTABLE` | 2019 ipywidgets / Voila interactive dashboard preserved for provenance; modernized by `apps/frontend/` (React 19 + TypeScript + Vite). |
| **Example PDB Inputs** | `proteinsolver/data/inputs/` | `PRESERVED_UNCHANGED` | 6 real structure fixtures (`1n5uA03.pdb`, `3fndA02.pdb`, `4beuA02.pdb`, etc.). |
| **Published Checkpoint** | `data/e53-s1952148-d93703104.state` | `FUNCTIONALLY_VERIFIED` | Checkpoint bytes preserved; SHA-256 verified (`1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727`); deterministic key translation applied during loading by `compat/checkpoint.py` with 0 missing keys, 0 unexpected keys, and 567,060 parameters. |
| **Upstream Tests** | `tests/` | `PRESERVED_UNCHANGED` | Original test suite (tests `ProteinNet`, `sudoku`, `functional`). |
| **Notebooks (Training)** | `notebooks/04_protein_train*.ipynb` | `CLI/NOTEBOOK_RETAINED` | Full training workflows are retained as reference notebooks; full execution depends on the externally hosted multi-gigabyte training shards. |
| **Notebooks (Sudoku)** | `notebooks/04_sudoku_train*.ipynb` | `CLI/NOTEBOOK_RETAINED` | Sudoku training and demonstration notebooks preserved in `notebooks/`. |
| **Notebooks (Design Demo)**| `notebooks/06_design_proteins.ipynb` | `APPLICATION_WRAPPED` | Notebook design workflow directly realized in `apps/backend/` and `apps/frontend/`. |
| **CI Configuration** | `.gitlab-ci.yml`, `.ci/` | `LEGACY_RETAINED_BUT_NOT_EXECUTABLE` | Upstream author used GitLab CI; preserved for provenance; modern operational CI is handled by GitHub Actions (`.github/workflows/ci.yml`). |
| **Binder Configuration**| `binder/` | `LEGACY_RETAINED_BUT_NOT_EXECUTABLE` | Original 2019 cloud Binder environment preserved for provenance; superseded by local virtual environment and full-stack application. |
| **C Extension Source** | `scripts/sugen.c` | `PRESERVED_UNCHANGED` | Original C source for generating Sudoku puzzles. |

---

## 3. Summary of Upstream Retention
- **Total Upstream Files Preserved:** 100% of upstream files remain in the repository.
- **Upstream Code Modifications:** 0 lines modified in `proteinsolver/`.
- **Modernization Strategy:** All compatibility bridges are isolated in `compat/`, and all user-facing features are isolated in `apps/`.
