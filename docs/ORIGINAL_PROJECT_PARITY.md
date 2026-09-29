# Original Project Parity Audit Matrix

This document provides a forensic classification of every major component, script, workflow, and dataset from Alexey Strokach's original ProteinSolver repository (*Cell Systems* 2020) relative to our modern Milestone 1 implementation under `ProteinDesignRND/ProteinSolver`.

---

## 1. Classification Taxonomy

- **`PRESERVED_UNCHANGED`**: Original upstream source file is intact with 0 line modifications.
- **`FUNCTIONALLY_VERIFIED`**: Executed and verified against published or expected outputs in our automated test suite or runtime.
- **`COMPATIBILITY_ADAPTED`**: Obsolete 2018–2020 dependency or API bridged cleanly via the isolated `compat/` layer without editing upstream code.
- **`APPLICATION_WRAPPED`**: Original capability exposed through modern FastAPI backend REST endpoints and React Web UI.
- **`CLI/NOTEBOOK_RETAINED`**: Research notebook or script preserved in `notebooks/` or `scripts/` for CLI execution.
- **`EXTERNAL_DEPENDENCY`**: Requires external proprietary licenses (e.g., PyRosetta, Quark) or external multi-gigabyte training repositories.
- **`LEGACY_RETAINED_BUT_NOT_EXECUTABLE`**: Legacy packaging (e.g. 2019 conda Dockerfiles, GitLab CI) preserved for provenance but superseded by modern standards.
- **`NOT_IMPLEMENTED`**: Explicitly unaddressed capability.

---

## 2. Complete Forensic Component Disposition

| # | Upstream Component / Artifact | Original Path | Status Classification | Forensic Analysis & Modern Disposition |
| :- | :--- | :--- | :--- | :--- |
| **1** | **ProteinNet Core Model** | `proteinsolver/models/proteinnet.py` | `PRESERVED_UNCHANGED` & `FUNCTIONALLY_VERIFIED` | 4-block EdgeConv Residual Graph Neural Network with 128-dim hidden embeddings and exactly 567,060 parameters. Verified in `tests/test_model_checkpoint.py`. |
| **2** | **EdgeConv Modules** | `proteinsolver/nn/edge_conv_mod.py` | `PRESERVED_UNCHANGED` & `FUNCTIONALLY_VERIFIED` | Edge-conditioned message passing neural network blocks. Tested in forward pass. |
| **3** | **Functional & Attention Utilities** | `proteinsolver/nn/functional.py` | `PRESERVED_UNCHANGED` & `FUNCTIONALLY_VERIFIED` | Sparse multi-head attention and activation modules. Verified via upstream unit test `tests/nn/test_functional.py`. |
| **4** | **Protein Datasets** | `proteinsolver/datasets/protein*.py` | `PRESERVED_UNCHANGED` & `FUNCTIONALLY_VERIFIED` | `protein.py`, `protein_v2.py`, and `protein_interaction.py`. Data-to-graph transformations and distance discretization. Verified in design pipeline. |
| **5** | **Sudoku Datasets & Utilities** | `proteinsolver/datasets/sudoku*.py` | `PRESERVED_UNCHANGED` & `FUNCTIONALLY_VERIFIED` | Sudoku string-to-tensor parsing and puzzle validity checking. 8/8 parameterizations pass in `tests/utils/test_sudoku.py`. |
| **6** | **N-Queens Dataset Stub** | `proteinsolver/datasets/nqueens.py` | `PRESERVED_UNCHANGED` | Upstream placeholder abstract `Dataset` class (`class NQueensDataset(Dataset): ...`). Preserved intact. |
| **7** | **Graph Labeling Dataset Stub** | `proteinsolver/datasets/graph_labeling.py` | `PRESERVED_UNCHANGED` | Upstream placeholder abstract `Dataset` class. Preserved intact. |
| **8** | **Protein Design Algorithm (CSP)** | `proteinsolver/utils/protein_design.py` | `COMPATIBILITY_ADAPTED` | Core iterative constraint satisfaction inverse folding engine (`design_sequence`) source preserved intact; wrapped by `compat/inference.py` on CPU to prevent PyTorch 2.6 cross-device indexing assertions. |
| **9** | **Protein Demo Workflow** | `notebooks/20_protein_demo.ipynb` | `APPLICATION_WRAPPED` | Original Jupyter demonstration adapted into modern interactive React web application (`apps/frontend/`) backed by FastAPI REST API (`apps/backend/`). |
| **10** | **Protein Analysis Workflow** | `notebooks/06_protein_analysis.ipynb` | `CLI/NOTEBOOK_RETAINED` | Jupyter analysis evaluating log-probabilities and mutations. Preserved in `notebooks/`. |
| **11** | **Sudoku Demo Workflow** | `notebooks/20_sudoku_demo.ipynb` | `CLI/NOTEBOOK_RETAINED` | Requires external trained Sudoku neural network checkpoint (`sudoku_train/c8de7e56/*.state`). Data generation and verification utilities are executable locally; model checkpoint is an external dependency. |
| **12** | **Sudoku Analysis Workflow** | `notebooks/06_sudoku_analysis.ipynb` | `CLI/NOTEBOOK_RETAINED` | Research analysis of Sudoku difficulty vs. graph connectivity. Preserved in `notebooks/`. |
| **13** | **Training Workflows** | `notebooks/04_protein_train.ipynb`, `04_sudoku_train*.ipynb` | `CLI/NOTEBOOK_RETAINED` | Full training workflows are retained as reference notebooks; full execution depends on the externally hosted multi-gigabyte training shards. |
| **14** | **Model Selection Workflows** | `notebooks/05_select_best_model.ipynb` | `CLI/NOTEBOOK_RETAINED` | Checkpoint validation loss tracking. Preserved in `notebooks/`. |
| **15** | **Model Scoring Utilities** | `proteinsolver/utils/model_scoring/` | `EXTERNAL_DEPENDENCY` | Scoring utilities in `proteinsolver/utils/model_scoring/` preserved intact; require external installations of standalone Rosetta binaries and/or Modeller. |
| **16** | **Pretrained Protein Checkpoint** | `data/e53-s1952148-d93703104.state` | `FUNCTIONALLY_VERIFIED` | Checkpoint bytes preserved; SHA-256 verified (`1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727`); deterministic key translation applied during loading by `compat/checkpoint.py` with 0 missing keys, 0 unexpected keys, and 567,060 parameters. |
| **17** | **External Training Datasets** | `http://deep-protein-gen.data.proteinsolver.org/` | `EXTERNAL_DEPENDENCY` | Multi-gigabyte pre-generated training datasets and graph shards. Retained as documented external download workflows. |
| **18** | **Docker Support** | `binder/Dockerfile`, `.ci/docker/Dockerfile` | `LEGACY_RETAINED_BUT_NOT_EXECUTABLE` | 2019 Conda/GitLab CI Dockerfiles targeting Python 3.7. Preserved for provenance; modern execution handled via native Python 3.11 / uv. |
| **19** | **Binder Support** | `binder/` | `LEGACY_RETAINED_BUT_NOT_EXECUTABLE` | Interactive Binder environment for legacy 2020 paper demonstration. |
| **20** | **Original Tests** | `tests/nn/test_functional.py`, `tests/utils/test_sudoku.py` | `FUNCTIONALLY_VERIFIED` | Upstream tests execute and pass cleanly under modern PyG/ruamel compatibility shims. |
| **21** | **C & Shell Utilities** | `scripts/sugen.c`, `scripts/run_notebook_*.sh` | `PRESERVED_UNCHANGED` | Standalone C Sudoku generator (`sugen.c`) and shell helpers. |
| **22** | **Legacy CI & Config** | `.gitlab-ci.yml`, `.ci/` | `LEGACY_RETAINED_BUT_NOT_EXECUTABLE` | Upstream GitLab CI configuration preserved for provenance; modern operational CI is handled by GitHub Actions (`.github/workflows/ci.yml`). |

---

## 3. Summary of Upstream Preservation
- **Package source code (`proteinsolver/`):** 100% frozen and unmodified.
- **Original notebooks and scripts:** 100% preserved in place.
- **Original checkpoint weights:** 100% preserved and verified against SHA-256 hash.
- **Runtime Modernization:** Completely encapsulated within `compat/`, `apps/backend/`, and `apps/frontend/`.
