# Upstream Provenance & Historical Lineage

**Document:** `docs/UPSTREAM_PROVENANCE.md`  
**Repository:** `ProteinDesignRND/ProteinSolver`  
**Upstream Repository:** `ostrokach/proteinsolver`  
**License:** MIT License (preserved intact in `LICENSE`)  
**Date of Acquisition:** 2026-09-29  

---

## 1. Upstream Metadata & Lineage

| Attribute | Upstream Value | Downstream Organization Value |
| :--- | :--- | :--- |
| **Repository URL** | `https://github.com/ostrokach/proteinsolver` | `https://github.com/ProteinDesignRND/ProteinSolver` |
| **Owner** | Alexey Strokach (`ostrokach`) | `ProteinDesignRND` |
| **Repository Name** | `proteinsolver` | `ProteinSolver` |
| **Acquisition Mode** | Official GitHub Fork | Full upstream commit history preserved |
| **Upstream Baseline Commit** | `69ef0965a3fc3bf191804035b539720a06e58ba6` | Baseline parent commit of `main` |
| **Original Default Branch** | `master` | Preserved as upstream mirror tracking branch |
| **Organization Default Branch**| N/A | `main` (branch protection ruleset active) |
| **Upstream License** | MIT License | MIT License (preserved, zero deletions) |
| **Primary Scientific Citation** | Strokach et al., *Cell Systems* 11.4 (2020): 402-411 | Same (primary attribution preserved) |

---

## 2. Scientific Attribution & Publication

The upstream software and model were designed and published by:

> **Alexey Strokach, David Becerra, Carles Corbi-Verge, Alan Perez-Rathke, and Philip M. Kim**  
> *"Fast and flexible design of novel proteins with graph neural networks."*  
> **Cell Systems** 11.4 (2020): 402-411.  
> DOI: [10.1016/j.cels.2020.08.016](https://doi.org/10.1016/j.cels.2020.08.016)

The upstream project is distributed under the terms of the MIT License:
```
MIT License
Copyright (c) 2019 Alexey Strokach
Permission is hereby granted, free of charge, to any person obtaining a copy...
```
This license and all original copyright headers remain strictly preserved in the repository.

---

## 3. Scoped Architectural Hierarchy

To guarantee upstream provenance and eliminate monkeypatch sprawl, code in this repository is strictly segregated into three architectural tiers:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TIER 3: APPLICATION LAYER                       │
│    apps/backend/ (FastAPI)    │    apps/frontend/ (React + Vite)       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ consumes
┌───────────────────────────────────▼────────────────────────────────────┐
│                       TIER 2: COMPATIBILITY LAYER                      │
│     compat/shims.py           │     compat/structure.py                │
│     compat/checkpoint.py      │     compat/inference.py                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ adapts without modifying
┌───────────────────────────────────▼────────────────────────────────────┐
│                    TIER 1: UPSTREAM ORIGINAL CORE                      │
│     proteinsolver/ (models, datasets, utils, neural network modules)   │
│     data/ (published checkpoint e53-s1952148-d93703104.state)          │
│     scripts/, notebooks/, tests/                                       │
└────────────────────────────────────────────────────────────────────────┘
```

### Tier 1: Upstream Original Core (`proteinsolver/`, `data/`)
- Contains the unmodified historical Python source code from commit `69ef0965a3fc3bf191804035b539720a06e58ba6`.
- **Policy:** 0 modifications to `proteinsolver/`. No in-place edits, no deletions of copyright notices, no modifications to legacy algorithms.

### Tier 2: Downstream Compatibility Layer (`compat/`)
- Contains non-invasive, caller-side compatibility adapters to bridge the 2019/2020 Python 3.6/3.7 stack with modern execution (Python 3.11, PyTorch 2.6, PyG 2.8).
- **Modules:**
  - `compat/shims.py`: Runtime stubs for Windows `fcntl`, `kmtools`, and `torch_geometric.utils.scatter_`.
  - `compat/structure.py`: Cleanroom Biopython-based structure parser and heavy-atom distance graph generator (replacing legacy `kmbio`).
  - `compat/checkpoint.py`: Checkpoint loader mapping flattened state-dict keys (`graph_conv_0` $	o$ `graph_conv_1`, etc.) with strict tensor shape validation.
  - `compat/inference.py`: High-level inference engine exposing pure `all-masked` design (preventing native sequence leakage), greedy MAP, multinomial sampling with temperature, and seed control.

### Tier 3: Downstream Application Layer (`apps/`)
- **Backend (`apps/backend/`):** A lightweight FastAPI REST API service exposing health, model inspection, structure validation, 1-click example loading, and real ProteinSolver inference.
- **Frontend (`apps/frontend/`):** A modern React + TypeScript + Vite web user interface allowing mentors and teammates to upload protein structures, configure design parameters, trigger generation, inspect color-coded per-residue confidence scores, and export FASTA sequences.

---

## 4. Upstream Remote Configuration

To pull future upstream changes or inspect upstream branches, git remotes are configured as:
```bash
git remote -v
# origin    https://github.com/ProteinDesignRND/ProteinSolver.git (fetch)
# origin    https://github.com/ProteinDesignRND/ProteinSolver.git (push)
# upstream  https://github.com/ostrokach/proteinsolver.git (fetch)
# upstream  https://github.com/ostrokach/proteinsolver.git (push)
```
