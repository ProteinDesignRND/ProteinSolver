# Original Repository Forensic Inventory

**Document:** `docs/ORIGINAL_PROJECT_INVENTORY.md`  
**Repository:** `ProteinDesignRND/ProteinSolver`  
**Upstream Commit:** `69ef0965a3fc3bf191804035b539720a06e58ba6`  
**Audit Date:** 2026-09-29  

---

## 1. Classification Taxonomy

Every component in the upstream project is classified into one of the following operational categories:

1. **PRESERVED_UNCHANGED:** Kept exactly as authored in upstream commit `69ef0965`.
2. **COMPATIBILITY_ADAPTED:** Wrapped or adapted via Tier 2 `compat/` to execute on modern PyTorch 2.6+ / PyG 2.8+ / Python 3.11+.
3. **WRAPPED_BY_APPLICATION:** Exposed through Tier 3 FastAPI backend and React frontend.
4. **REPLACED_WHERE_UNAVOIDABLE:** Replaced by modern cleanroom implementation outside upstream code (e.g. `kmbio` replaced by Biopython).
5. **EXTERNAL_DATA_DEPENDENT:** Valid upstream research code whose full execution requires external multi-gigabyte datasets (e.g. 72M CATH Parquet corpus).
6. **LEGACY_OBSOLETE:** Obsolete CI/cloud configurations (e.g. 2019 GitLab CI, obsolete ipywidgets Voila dashboard).

---

## 2. Upstream Module Inventory

| Module / Component | Upstream Path | Classification | Modern Status & Adaptation |
| :--- | :--- | :---: | :--- |
| **ProteinNet GNN** | `proteinsolver/models/proteinnet.py` | `PRESERVED_UNCHANGED` | 4-block EdgeConv GNN (567,060 params). Executes forward passes on both CPU and CUDA. |
| **EdgeConv Module** | `proteinsolver/nn/edge_conv_mod.py` | `PRESERVED_UNCHANGED` | Custom PyG message-passing layer for edge-conditioned graph convolutions. |
| **Activation Functions** | `proteinsolver/nn/activation.py` | `PRESERVED_UNCHANGED` | Custom ELU / activation functions. |
| **Functional NN Ops** | `proteinsolver/nn/functional.py` | `PRESERVED_UNCHANGED` | GNN tensor operations and loss functions. |
| **Protein Design (CSP)** | `proteinsolver/utils/protein_design.py`| `COMPATIBILITY_ADAPTED` | Core iterative constraint satisfaction design algorithm (`design_sequence`). Modern PyTorch 2.6 cross-device indexing requires CPU execution. |
| **Protein Structure Utils**| `proteinsolver/utils/protein_structure.py`| `COMPATIBILITY_ADAPTED` | Defines `ProteinData` namedtuple. `kmbio` dependencies adapted via Biopython in `compat/structure.py`. |
| **Scatter Shim** | `proteinsolver/utils/scatter.py` | `COMPATIBILITY_ADAPTED` | PyG 2.x removed `scatter_`; shimmed via `torch_scatter.scatter` in `compat/shims.py`. |
| **Sudoku Utils** | `proteinsolver/utils/sudoku.py` | `PRESERVED_UNCHANGED` | 9x9 Sudoku CSP solver and graph representation using the same GNN engine. |
| **Common Utils** | `proteinsolver/utils/common.py` | `PRESERVED_UNCHANGED` | Utility functions, seeds, tensor helpers. |
| **Compression Utils** | `proteinsolver/utils/compression.py` | `PRESERVED_UNCHANGED` | Gzip / serialization helpers. |
| **Model Scoring** | `proteinsolver/utils/model_scoring/` | `EXTERNAL_DATA_DEPENDENT` | Legacy Rosetta / Modeller scoring wrappers (requires external proprietary software). |
| **Protein Datasets** | `proteinsolver/datasets/protein.py` | `PRESERVED_UNCHANGED` | PyG Dataset classes for protein contact graphs (`row_to_data`, `transform_edge_attr`). |
| **Sudoku Datasets** | `proteinsolver/datasets/sudoku.py` | `PRESERVED_UNCHANGED` | PyG Dataset classes for Sudoku boards. |
| **N-Queens Datasets** | `proteinsolver/datasets/nqueens.py` | `PRESERVED_UNCHANGED` | PyG Dataset classes for N-Queens constraint problems. |
| **Graph Labeling** | `proteinsolver/datasets/graph_labeling.py`| `PRESERVED_UNCHANGED` | Generic graph coloring/labeling problem dataset. |
| **Legacy Voila Dashboard**| `proteinsolver/dashboard/` | `LEGACY_OBSOLETE` | 2019 ipywidgets / Voila interactive dashboard. Modernized by `apps/frontend/` (React + Vite). |
| **Example PDB Inputs** | `proteinsolver/data/inputs/` | `PRESERVED_UNCHANGED` | 6 real structure fixtures (`1n5uA03.pdb`, `3fndA02.pdb`, `4beuA02.pdb`, etc.). |
| **Published Checkpoint** | `data/e53-s1952148-d93703104.state` | `COMPATIBILITY_ADAPTED` | 2.2 MB trained weights. State-dict keys mapped (`graph_conv_0` $	o$ `graph_conv_1`). |
| **Upstream Tests** | `tests/` | `PRESERVED_UNCHANGED` | Original test suite (tests `ProteinNet`, `sudoku`, `functional`). |
| **Notebooks (Training)** | `notebooks/04_protein_train*.ipynb` | `EXTERNAL_DATA_DEPENDENT` | Training notebooks requiring 72M CATH Parquet corpus on HPC cluster. |
| **Notebooks (Sudoku)** | `notebooks/04_sudoku_train*.ipynb` | `PRESERVED_UNCHANGED` | Sudoku training and demonstration notebooks. |
| **Notebooks (Design Demo)**| `notebooks/06_design_proteins.ipynb` | `WRAPPED_BY_APPLICATION` | Notebook design workflow directly realized in `apps/backend/` and `apps/frontend/`. |
| **CI Configuration** | `.gitlab-ci.yml`, `.ci/` | `LEGACY_OBSOLETE` | Upstream author used GitLab CI; downstream utilizes GitHub Actions. |
| **Binder Configuration**| `binder/` | `PRESERVED_UNCHANGED` | Original environment specifications for cloud Binder. |
| **C Extension Source** | `scripts/sugen.c` | `PRESERVED_UNCHANGED` | Original C source for generating Sudoku puzzles. |

---

## 3. Summary of Upstream Retention
- **Total Upstream Files Preserved:** 100% of upstream files remain in the repository.
- **Upstream Code Modifications:** 0 lines modified in `proteinsolver/`.
- **Modernization Strategy:** All compatibility bridges are isolated in `compat/`, and all user-facing features are isolated in `apps/`.
