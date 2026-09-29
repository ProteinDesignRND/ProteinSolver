# ProteinSolver — Modern Runnable Reproduction & Full-Stack Application
**Upstream Reproduction, Isolated Compatibility Engine, FastAPI Backend, & React Frontend**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.11.x](https://img.shields.io/badge/Python-3.11.9-brightgreen.svg)](https://python.org)
[![PyTorch: 2.6](https://img.shields.io/badge/PyTorch-2.6.0%2Bcu124-orange.svg)](https://pytorch.org)
[![PyG: 2.8](https://img.shields.io/badge/PyG-2.8.0.post1-purple.svg)](https://pyg.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com)
[![React: 19](https://img.shields.io/badge/React-19.2-61dafb.svg)](https://react.dev)
[![TypeScript: 6.0](https://img.shields.io/badge/TypeScript-6.0.2-3178c6.svg)](https://www.typescriptlang.org)
[![Node.js: >=20.19](https://img.shields.io/badge/Node.js-%3E%3D20.19.0-green.svg)](https://nodejs.org)

---

## Table of Contents
1. [Overview & Project Context](#overview--project-context)
2. [Architectural Stratification (Upstream vs. Modern)](#architectural-stratification-upstream-vs-modern)
3. [Original Upstream Project Heritage](#original-upstream-project-heritage)
4. [Resolved Compatibility Innovations (7 Issues)](#resolved-compatibility-innovations-7-issues)
5. [Prerequisites & Verified Installation](#prerequisites--verified-installation)
6. [Running the Full-Stack Application](#running-the-full-stack-application)
7. [Mentor Demonstration Walkthrough](#mentor-demonstration-walkthrough)
8. [Automated Test Suite](#automated-test-suite)
9. [Pre-trained Checkpoints & Datasets](#pre-trained-checkpoints--datasets)
10. [Known Limitations & Scientific Boundaries](#known-limitations--scientific-boundaries)
11. [Governance & Team Contribution Model](#governance--team-contribution-model)
12. [License & Citation](#license--citation)

---

## Overview & Project Context

**ProteinSolver** is a Graph Neural Network (GNN) for inverse protein design, originally created by Alexey Strokach, David Becerra, Carles Corbi-Verge, Albert Perez-Riba, and Philip M. Kim (*Cell Systems* 2020). It formulates inverse protein folding as a **Constraint Satisfaction Problem (CSP)** over residue spatial adjacency graphs ($r < 12.0$ Å), iteratively assigning amino acids that stabilize a target protein backbone.

This implementation repository (`ProteinDesignRND/ProteinSolver`) fulfills **Milestone 1** of the ProteinDesign project:
- A **GitHub fork of ostrokach/proteinsolver**, preserving 100% of upstream git commit history.
- An **isolated cleanroom compatibility layer** (`compat/`) enabling execution on Python 3.11, PyTorch 2.6, and PyG 2.8 without altering the frozen upstream package.
- A **local mentor-ready FastAPI backend** (`apps/backend/`) exposing structured REST endpoints with strict JSON input validation.
- A **modern React 19 + TypeScript + Vite frontend** (`apps/frontend/`) featuring interactive residue confidence heatmaps and FASTA export.
- **Design-path input invariant enforced by the compatibility/application layer and protected by regression tests**, ensuring that inverse folding design operates on purely all-masked inputs ($data.x = 20$, $data.y = None$).

---

## Architectural Stratification (Upstream vs. Modern)

To maintain absolute provenance and scientific traceability, the codebase is partitioned into three strict tiers:

```
┌────────────────────────────────────────────────────────────────────────┐
│  Tier 1: Upstream Original Package (proteinsolver/)                   │
│  - 100% frozen upstream source (baseline commit 69ef0965a3fc3bf1918)   │
│  - 4-block EdgeConv Residual GNN (hidden_size=128, 567,060 parameters) │
│  - CSP iterative sequence design algorithm (design_sequence)           │
│  - Sudoku graph representations and verification utilities             │
└──────────────────────────────────▲─────────────────────────────────────┘
                                   │ (imported & wrapped, NEVER modified)
┌──────────────────────────────────┴─────────────────────────────────────┐
│  Tier 2: Cleanroom Compatibility Layer (compat/)                       │
│  - compat/shims.py: Windows POSIX fcntl stub, kmtools stubs,           │
│    PyG 2.x scatter_ in-place shim, ruamel.yaml safe_load shim          │
│  - compat/structure.py: BioPython cleanroom structure parser (<12.0 A) │
│  - compat/checkpoint.py: Layer key mapping (graph_conv_0 -> 1)         │
│  - compat/inference.py: All-masked design engine (data.x=20, data.y=None)│
└──────────────────────────────────▲─────────────────────────────────────┘
                                   │
┌──────────────────────────────────┴─────────────────────────────────────┐
│  Tier 3: Modern Application Layer (apps/)                              │
│  - apps/backend/: Local mentor-ready FastAPI REST service (port 8000)   │
│  - apps/frontend/: React 19 + TypeScript + Vite web UI (port 5173)     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Original Upstream Project Heritage

The following original documentation sections from Alexey Strokach's repository are preserved for historical provenance:

### Upstream Pre-trained Models
Original models can be downloaded using `wget` from the historical model registry:
*(HISTORICAL UPSTREAM COMMAND — may no longer be operational; modern application uses bundled local checkpoint `data/e53-s1952148-d93703104.state`)*
```bash
wget -r -nH --cut-dirs 1 --reject "index.html*" "http://models.proteinsolver.org/v0.1/"
```
For examples of using pretrained ProteinSolver models in downstream applications (such as mutation ΔΔG prediction), see the historical [`elaspic/elaspic2`](https://gitlab.com/elaspic/elaspic2) repository.

### Upstream Training and Validation Datasets
Data used to train the original networks on Sudoku puzzles and protein sequence reconstruction is hosted at:
*(HISTORICAL UPSTREAM COMMAND — may no longer be operational; documented for reference)*
```bash
wget -r -nH --reject "index.html*" "http://deep-protein-gen.data.proteinsolver.org/"
```
Dataset generation was carried out in predecessor project [`ostrokach/protein-adjacency-net`](https://gitlab.com/ostrokach/protein-adjacency-net).

### Upstream Environment Variables
- `DATAPKG_DATA_DIR` - Location of historical training and validation data shards.

---

## Resolved Compatibility Innovations (7 Issues)

Seven concrete historical incompatibilities between the 2020 codebase and modern runtime environments were resolved inside `compat/`:

1. **Windows POSIX `fcntl` Incompatibility:** Windows lacks the Unix `fcntl` module. `compat/shims.py` registers an in-memory module. To ensure file locking semantics are not falsely simulated, calling `flock` or `lockf` raises `NotImplementedError` rather than silently pretending locks succeed.
2. **Obsolete `kmbio` / `kmtools` Dependencies:** Unmaintained 2018–2019 dependencies fail to build on Python 3.11. `compat/shims.py` stubs their imports, while `compat/structure.py` provides a cleanroom BioPython-based parser for coordinate extraction and heavy-atom distance matrices ($r < 12.0$ Å).
3. **PyG 2.x `scatter_` In-Place Removal:** Modern PyG removed `torch_geometric.utils.scatter_`. `compat/shims.py` defines a backward-compatible wrapper that routes in-place operations to `torch_scatter.scatter(..., out=out)`.
4. **PyG Batch Construction Changes:** Modern PyG handles batching semantics differently than PyG 1.x. Handled via explicit `Batch.from_data_list([data])` encapsulation.
5. **Checkpoint State-Dict Key Mapping:** Published checkpoint keys use training-run names (`graph_conv_0.`) whereas packaged `ProteinNet` defines `graph_conv_1.`. `compat/checkpoint.py` maps these deterministically, validating all 567,060 parameters with zero missing/unexpected keys.
6. **PyTorch 2.6 Cross-Device Indexing:** Under the verified PyTorch 2.6 environment, boolean tensor masking in `proteinsolver.utils.protein_design.design_sequence` triggered cross-device indexing assertions on CUDA. CSP iterative design is standardized to CPU (`device="cpu"`), completing a 92-residue domain typically around 1.5–2.1 seconds on the verified CPU environment (exact runtime is run-dependent).
7. **`ruamel.yaml` 0.18+ Deprecation:** Modern `ruamel.yaml` deprecated `yaml.safe_load(...)`. `compat/shims.py` routes `safe_load` to `YAML(typ='safe', pure=True).load`, enabling upstream Sudoku test validation.

---

## Prerequisites & Verified Installation

### System Requirements
- **Python**: 3.11.x (tested on 3.11.9)
- **Node.js**: `>=20.19.0` (tested on Node v24.18.0, npm 11.16.0)
- **OS**: Windows 10/11 (verified environment: Windows 11); Linux/macOS setup paths provided as unverified references
- **Hardware**: CPU is sufficient for the verified application path; NVIDIA GPU/CUDA is optional for supported model forward operations (iterative CSP sequence design is standardized to CPU).

### Step 1: Clone Repository
```bash
git clone https://github.com/ProteinDesignRND/ProteinSolver.git
cd ProteinSolver
git checkout feature/milestone-1-full-implementation
```

### Step 2: Set Up Python Virtual Environment
Using `uv` (recommended) or standard Python `venv`:
```bash
uv venv .venv --python 3.11.9
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies from pinned requirements:
uv pip install -r requirements.txt
uv pip install -e . --no-deps
```

### Step 3: Verify Checkpoint Integrity
Verify the cryptographic SHA-256 checksum of the bundled checkpoint:
```powershell
# Windows PowerShell:
Get-FileHash .\data\e53-s1952148-d93703104.state -Algorithm SHA256
```
```bash
# Cross-Platform Python:
python -c "import hashlib; print(hashlib.sha256(open('data/e53-s1952148-d93703104.state','rb').read()).hexdigest().upper())"
```
Expected SHA-256: `1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727`

### Step 4: Install Frontend Dependencies
```bash
cd apps/frontend
npm ci
cd ../..
```

---

## Running the Full-Stack Application

### Terminal 1: Launch Backend API
```bash
python -m apps.backend.main
# Server active at: http://127.0.0.1:8000
# Interactive OpenAPI documentation: http://127.0.0.1:8000/docs
```

### Terminal 2: Launch Frontend Application
```bash
cd apps/frontend
npm run dev
# Vite dev server active at: http://localhost:5173
```
Open `http://localhost:5173` in your browser. The Vite development server automatically proxies API requests to `http://127.0.0.1:8000`.

---

## Mentor Demonstration Walkthrough

Follow this deterministic sequence during an academic demonstration:

1. **Launch Stack:** Confirm backend is active on `:8000` and frontend on `:5173`.
2. **Open Browser:** Navigate to `http://localhost:5173`.
3. **Inspect Connection Badge:** Header shows `Model Ready (567,060 params) | CPU`.
4. **Load Reference Target:** Click the **`1n5uA03`** 1-Click Fixture button. Chain A (92 residues, IDs 205..296) loads with spatial adjacency extracted.
5. **Run Inverse Protein Design:**
   - Ensure mode is set to **✨ Inverse Folding Design**.
   - Select **Argmax (Greedy MAP)**.
   - Click **🚀 Run ProteinSolver Design**.
   - Typically within 1.5–2.1 seconds on CPU (exact runtime is run-dependent), the model designs a 92-residue sequence with an interactive residue confidence heatmap.
   - Click **📋 Copy FASTA** or **💾 Download**.
6. **Demonstrate Methodological Integrity (Zero Native Leakage):**
   - Switch mode to **📊 Diagnostic Evaluation**.
   - Click **🚀 Run ProteinSolver Diagnostic**.
   - The UI reveals **41.30% native sequence identity** (38/92 residues), reproducing the project's previously validated single-target integration result.
   - Point out the prominent disclaimer stating that native sequence comparison is segregated and was never exposed to the design network.
7. **Inspect Upstream Lineage:** Click **📖 Upstream Provenance** to review author attribution, MIT license, and compatibility boundaries.

---

## Automated Test Suite

Run the full automated test suite covering neural network operations, compatibility shims, structure parsing, checkpoint loading, API contracts, zero-leak regression, and Sudoku puzzle verification:

```bash
pytest tests/ -v
```

### Suite Composition (32 Tests Total)
- `tests/nn/test_functional.py`: Sparse multi-head attention forward operations.
- `tests/test_all_masked_design.py`: MAP greedy design and multinomial seed determinism.
- `tests/test_attributes.py`: Upstream package version and namespace attributes.
- `tests/test_backend_api.py`: 7 distinct REST endpoints verified across 8 backend API tests (`/api/health`, `/api/model`, `/api/examples`, `/api/examples/{id}`, `/api/validate`, `/api/design`, `/api/diagnostic`).
- `tests/test_compat_shims.py`: Fail-loud `fcntl` stub, `kmtools` stubs, PyG `scatter_` in-place shim.
- `tests/test_compat_structure.py`: BioPython chain metadata and heavy-atom contact matrix extraction.
- `tests/test_integration_1n5u.py`: End-to-end integration reproducing 41.30% native sequence identity.
- `tests/test_leak_regression.py`: Critical verification that `batch.y` is stripped and `batch.x = 20`.
- `tests/test_model_checkpoint.py`: SHA-256 checksum, exact 567,060 parameter count, forward pass.
- `tests/utils/test_sudoku.py`: 8 Sudoku tensor parsing and solution verification tests.

---

## Pre-trained Checkpoints & Datasets

- **Pre-trained Model Checkpoint:** `data/e53-s1952148-d93703104.state` (tracked in repository)
  - **Architecture:** `ProteinNet` (4 EdgeConv blocks, `hidden_size=128`)
  - **Parameter Count:** Exactly 567,060 parameters
  - **SHA-256 Checksum:** `1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727`
- **Integration Structure Fixture:** `data/1n5uA03.pdb` (92-residue crystal structure, Chain A)

---

## Known Limitations & Scientific Boundaries

1. **Single-Target Fixture Boundary:** Target `1n5uA03` is a single-target integration fixture. Its 41.30% recovery (38/92 residues) reproduces the project's previously validated single-target all-masked integration result, NOT a general benchmark. Training set membership of `1n5uA03` has not been independently verified against the external multi-gigabyte training shards. Comprehensive scientific benchmarking belongs strictly to the separate research repository (`ProteinDesignRND/ProteinDesign`).
2. **Display-Only Confidence Bands:** In the Web UI, residue tiles are color-coded based on model selection probability ($\ge 70\%$ green, $40-69\%$ amber, $< 40\%$ rose). These are visualization aids, not calibrated biological probabilities.
3. **CPU Execution Default:** CSP iterative sequence design is executed on CPU (`device="cpu"`). Under the verified PyTorch 2.6 environment, the legacy CUDA design path triggered cross-device indexing assertions; the compatibility layer therefore standardizes iterative CSP execution to CPU. CPU execution is typically around 1.5–2.1 seconds on the verified CPU environment (exact runtime is run-dependent) and stable without editing upstream code.
4. **External Scoring Dependencies:** Upstream evaluation notebooks (`notebooks/16_david_analysis.ipynb`, `notebooks/16_david_analysis_quark.ipynb`) and wrappers in `proteinsolver/utils/model_scoring/` depend on external installations of standalone Rosetta binaries and Modeller, and analyze external QUARK ab initio structural models. These scoring workflows are external research dependencies and are NOT required for the verified Milestone 1 mentor demo or application path.
5. **External Multi-GB Training Datasets:** Full training datasets (multi-gigabyte shards) are hosted externally and documented for reference; full training workflows are retained as reference notebooks; full execution depends on the externally hosted multi-gigabyte training shards.
6. **Browser E2E Testing Not Automated:** Automated test suites cover unit, model, compat, and backend API suites (32 tests across 10 modules) plus frontend TypeScript/Vite production build; browser-based end-to-end UI interaction is not automated in CI.
7. **CI Forward-Maintenance Notes:** GitHub Actions runners emit advisory deprecation notices for Node.js 20 actions (automatically executed under Node 24 by the runner) and scheduled Ubuntu 26 runner image migrations. These warnings are advisory and non-blocking for Milestone 1; active workflows succeed 100% in CI.

---

## Governance & Team Contribution Model

- **Repository Owner:** Organization `ProteinDesignRND`
- **Branch Protection:** GitHub Ruleset `main-protection` active on `main`:
  - Enforce linear history: YES
  - Require pull request: YES (1 approval)
  - Require signed commits: YES
  - Block force pushes: YES
  - Direct pushes to `main` blocked for all non-admin teammates.
- **Workflow:** Teammates clone, create a feature branch (`feature/topic`), verify tests (`pytest tests/`), and open a Pull Request targeting `main`.

---

## License & Citation

ProteinSolver is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

```bibtex
@article{strokach2020fast,
  title={Fast and Flexible Protein Design Using Deep Graph Neural Networks},
  author={Strokach, Alexey and Becerra, David and Corbi-Verge, Carles and Perez-Riba, Albert and Kim, Philip M},
  journal={Cell Systems},
  volume={11},
  number={4},
  pages={402--411},
  year={2020},
  publisher={Elsevier},
  doi={10.1016/j.cels.2020.08.016}
}
```
