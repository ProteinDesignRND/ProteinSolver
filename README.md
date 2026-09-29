# ProteinSolver — Modern Production Reproduction Suite
**Official Upstream Reproduction, Isolated Compatibility Engine, FastAPI Backend, & React Frontend**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11%2B-brightgreen.svg)](https://python.org)
[![PyTorch: 2.6](https://img.shields.io/badge/PyTorch-2.6%2Bcu124-orange.svg)](https://pytorch.org)
[![PyG: 2.8](https://img.shields.io/badge/PyG-2.8.0.post1-purple.svg)](https://pyg.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com)
[![React: 19](https://img.shields.io/badge/React-19-61dafb.svg)](https://react.dev)
[![TypeScript: 5.9](https://img.shields.io/badge/TypeScript-5.9-3178c6.svg)](https://www.typescriptlang.org)

---

## Table of Contents
1. [Overview](#overview)
2. [Preservation vs. Modernization Strategy](#preservation-vs-modernization-strategy)
3. [Architecture](#architecture)
4. [Prerequisites & Installation](#prerequisites--installation)
5. [Running the Application](#running-the-application)
6. [Mentor Demonstration Walkthrough](#mentor-demonstration-walkthrough)
7. [Running Tests](#running-tests)
8. [Models & Checkpoints](#models--checkpoints)
9. [Known Limitations](#known-limitations)
10. [Team Workflow & Contributing](#team-workflow--contributing)
11. [License & Upstream Citation](#license--upstream-citation)

---

## Overview

**ProteinSolver** is a Graph Neural Network (GNN) for inverse protein design, originally created by Alexey Strokach, David Becerra, Carles Corbi-Verge, Albert Perez-Riba, and Philip M. Kim (*Cell Systems* 2020). It formulates inverse protein folding as a **Constraint Satisfaction Problem (CSP)** over residue spatial adjacency graphs ($r < 12.0$ Å), iteratively selecting amino acids that stabilize the target backbone structure.

This repository (`ProteinDesignRND/ProteinSolver`) represents **Milestone 1** of the ProteinDesign project:
- An **official upstream fork** preserving the entire git history from author commit `69ef0965a3fc3bf191804035b539720a06e58ba6`.
- A cleanroom **isolated compatibility layer** (`compat/`) that makes ProteinSolver execute seamlessly on modern Python 3.11, PyTorch 2.6, and PyG 2.8 on Windows and Linux without modifying upstream package code.
- A production **FastAPI backend** (`apps/backend/`) exposing structured REST endpoints for validation, design, and diagnostic recovery.
- A modern **React + TypeScript + Vite frontend** (`apps/frontend/`) featuring interactive residue confidence heatmaps, FASTA export, and upstream provenance auditing.
- Strict **native sequence leak protection**, mathematically guaranteeing that inverse folding occurs with zero reference sequence leakage.

---

## Preservation vs. Modernization Strategy

```
┌────────────────────────────────────────────────────────────────────────┐
│  Tier 1: Original Upstream Package (proteinsolver/)                   │
│  - 100% frozen historical source (commit 69ef0965a3fc3bf191804035b539) │
│  - 4-block EdgeConv GNN (567,060 parameters)                           │
│  - Constraint Satisfaction iterative sequence design algorithm         │
└──────────────────────────────────▲─────────────────────────────────────┘
                                   │ (wrapped, never edited)
┌──────────────────────────────────┴─────────────────────────────────────┐
│  Tier 2: Cleanroom Compatibility Layer (compat/)                       │
│  - Windows POSIX fcntl stub                                            │
│  - BioPython cleanroom structure parser (replaces dead kmbio/kmtools)  │
│  - PyG 2.x scatter_ backward-compatibility shim                        │
│  - Checkpoint state-dict key translation (graph_conv_0 -> graph_conv_1)│
│  - Zero-leak all-masked design engine (data.x = 20, data.y = None)     │
└──────────────────────────────────▲─────────────────────────────────────┘
                                   │
┌──────────────────────────────────┴─────────────────────────────────────┐
│  Tier 3: Modern Application Layer (apps/)                              │
│  - apps/backend/: FastAPI REST API (health, model, design, diagnostic) │
│  - apps/frontend/: React 19 + TypeScript + Vite UI with dark aesthetics│
└────────────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites & Installation

### Requirements
- **Python**: 3.11.x (tested on 3.11.9)
- **Node.js**: v18+ (tested on v24.18.0, npm 11.16.0)
- **OS**: Windows 10/11 or Ubuntu Linux 22.04+

### Step 1: Clone Repository
```bash
git clone https://github.com/ProteinDesignRND/ProteinSolver.git
cd ProteinSolver
```

### Step 2: Set Up Python Environment
Using `uv` (recommended) or standard `venv`:
```bash
uv venv .venv --python 3.11
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

uv pip install torch==2.6.0+cu124 --extra-index-url https://download.pytorch.org/whl/cu124
uv pip install torch-geometric==2.8.0.post1 torch-scatter==2.1.2+pt26cu124 --extra-index-url https://data.pyg.org/whl/torch-2.6.0+cu124.html
uv pip install biopython==1.88 fastapi==0.115.11 uvicorn==0.34.0 pydantic==2.10.6 pytest httpx ruamel.yaml
uv pip install -e . --no-deps
```

### Step 3: Install Frontend Dependencies
```bash
cd apps/frontend
npm install
cd ../..
```

---

## Running the Application

### Option A: Launch Backend Service
```bash
# From repository root
python -m apps.backend.main
# Server starts at: http://127.0.0.1:8000
# OpenAPI Docs: http://127.0.0.1:8000/docs
```

### Option B: Launch Frontend Application
```bash
cd apps/frontend
npm run dev
# Vite dev server starts at: http://localhost:5173
```
Open `http://localhost:5173` in your browser. The frontend is automatically configured to proxy API requests to `http://127.0.0.1:8000`.

---

## Mentor Demonstration Walkthrough

For an executive demonstration to academic advisors or mentors:

1. **Launch Services:** Start backend on `:8000` and frontend on `:5173`.
2. **Open Browser:** Navigate to `http://localhost:5173`.
3. **Inspect Model Status:** Top header shows `Model Ready (567,060 params) | CPU`.
4. **Select Fixture:** Click the **`1n5uA03`** 1-Click Fixture button. Chain A (92 residues) loads automatically with distance graph extracted.
5. **Run Inverse Folding Design:**
   - Select **✨ Inverse Folding Design** mode.
   - Choose **Argmax (Greedy MAP)**.
   - Click **🚀 Run ProteinSolver Design**.
   - Within ~1.8 seconds, the model generates a complete 92-residue sequence with residue confidence heatmap.
   - Click **📋 Copy FASTA** or **💾 Download**.
6. **Demonstrate Methodological Integrity (Zero Native Leakage):**
   - Switch to **📊 Diagnostic Evaluation** mode.
   - Click **🚀 Run ProteinSolver Diagnostic**.
   - The UI reveals **41.30% native sequence identity** (38/92 residues), exactly reproducing the published MAP greedy baseline on `1n5uA03`.
   - Point out the prominent disclaimer that diagnostic comparison is segregated and was never exposed to the design network.
7. **Inspect Provenance:** Click **📖 Upstream Provenance** in the top navigation to display the complete historical lineage, MIT license attribution, and modern compatibility innovations.

---

## Running Tests

Execute the automated test suite covering shims, structure parsing, checkpoint parameter validation, zero-leak regression, and FastAPI endpoints:

```bash
pytest tests/ -v
```

To run only the milestone 1 unit and integration suite:
```bash
pytest tests/test_*.py -v
```

---

## Models & Checkpoints

The official published model checkpoint is stored at:
```
data/e53-s1952148-d93703104.state
```
- **Architecture:** `ProteinNet` (4 EdgeConv blocks, 162-dim hidden embeddings)
- **Parameters:** 567,060
- **SHA-256 Checksum:** `1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727`

If the checkpoint is missing, download it from the original repository releases or Zenodo record (`10.5281/zenodo.3736357`).

---

## Known Limitations

1. **CPU Execution Default:** CSP iterative sequence design is configured on CPU (`device="cpu"`). PyTorch 2.6 introduced cross-device boolean indexing checks that cause CUDA assertions in the legacy CSP code. CPU execution is highly optimized (~1.7s for 92 AA) and eliminates runtime instability without modifying upstream code.
2. **Rosetta Scoring Scripts:** Upstream evaluation scripts in `notebooks/16_david_analysis/` require licensed local installations of PyRosetta and Quark, which are documented as external research dependencies.
3. **Single-Target Fixture Boundary:** `1n5uA03` is a single-target integration fixture. Its 41.30% recovery is an integration sanity check, NOT a benchmark evaluation. Systematic benchmarking belongs strictly in the research repository (`ProteinDesignRND/ProteinDesign`).

---

## Team Workflow & Contributing

This repository is governed under `ProteinDesignRND` organizational rules:
- **Default Branch:** `main` (Protected by GitHub Ruleset).
- **Protection Rules:**
  - Direct pushes to `main` are blocked.
  - Pull requests require at least 1 approval.
  - Commit signatures are required.
  - Force-pushes and branch deletions are disabled.
  - Linear git history enforced via squash merging.
- **Development Workflow:**
  1. Clone repository and create a feature branch (`feature/your-topic`).
  2. Implement changes, following the Tier 1/2/3 boundary rules.
  3. Verify all tests pass (`pytest tests/`) and frontend builds (`npm run build`).
  4. Submit a Pull Request targeting `main`.

---

## License & Upstream Citation

ProteinSolver is released under the **MIT License**. See [LICENSE](LICENSE) for details.

### Citation
```bibtex
@article{strokach2020fast,
  title={Fast and flexible design of novel proteins with graph neural networks},
  author={Strokach, Alexey and Becerra, David and Corbi-Verge, Carles and Perez-Riba, Albert and Kim, Philip M},
  journal={Cell Systems},
  volume={11},
  number={4},
  pages={402--411},
  year={2020},
  publisher={Elsevier}
}
```
