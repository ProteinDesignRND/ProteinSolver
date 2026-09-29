# Application Architecture & Technical Design

**Document:** `docs/ARCHITECTURE.md`  
**Repository:** `ProteinDesignRND/ProteinSolver`  

---

## 1. System Overview

ProteinSolver Milestone 1 provides a clean, modular, production-grade application architecture around the original ProteinSolver GNN core:

```
┌─────────────────────────────────────────────────────────────┐
│                    REACT FRONTEND (Vite)                    │
│   - Structure Upload (.pdb / .cif)                          │
│   - 1-Click Example Loader (1n5uA03, 3fndA02, etc.)         │
│   - Parameter Config (Strategy, Temperature, Seed)          │
│   - Sequence Viewer with Per-Residue Confidence Tiles       │
│   - FASTA & JSON Export                                     │
└──────────────────────────────┬──────────────────────────────┘
                               │ REST HTTP (JSON / multipart)
┌──────────────────────────────▼──────────────────────────────┐
│                    FASTAPI BACKEND                          │
│   - GET  /api/health       (status, hardware, versions)     │
│   - GET  /api/model        (params, checkpoint metadata)    │
│   - GET  /api/examples     (built-in structure fixtures)    │
│   - POST /api/validate     (PDB validation, chain parsing)  │
│   - POST /api/design       (real all-masked CSP design)     │
│   - POST /api/diagnostic   (native sequence recovery check) │
└──────────────────────────────┬──────────────────────────────┘
                               │ Python API
┌──────────────────────────────▼──────────────────────────────┐
│                  COMPATIBILITY LAYER (compat/)              │
│   - Shims: fcntl, kmtools, torch_geometric.utils.scatter_   │
│   - Structure: BioPython PDB parser -> ProteinData graph    │
│   - Checkpoint: State-dict key translation & validation     │
│   - Inference Engine: Mode enforcement, seed reproducibility│
└──────────────────────────────┬──────────────────────────────┘
                               │ Unmodified calls
┌──────────────────────────────▼──────────────────────────────┐
│                ORIGINAL UPSTREAM PROTEINSOLVER              │
│   - ProteinNet (4-block EdgeConv GNN, 567,060 parameters)   │
│   - row_to_data -> transform_edge_attr                      │
│   - design_sequence (iterative CSP sequence generator)      │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Component Specifications

### 2.1 Backend (`apps/backend/`)
- **Framework:** FastAPI with Uvicorn server and Pydantic schemas.
- **Design Mode Security:** Strictly enforces all-masked inverse folding (`data.x = 20`, `data.y = None`). The backend API refuses to accept native sequence labels into the design path, guaranteeing 0 information leakage.
- **Error Handling:** Structured HTTP exceptions with clean error messages; no raw stack traces exposed to client.

### 2.2 Frontend (`apps/frontend/`)
- **Framework:** React 19 + TypeScript + Vite.
- **Styling:** Curated modern CSS with responsive glassmorphism aesthetic, dark mode styling, and accessible contrast.
- **Visuals:** Sequence display with color-coded confidence indicators:
  - High confidence ($\ge 0.70$): Emerald
  - Moderate confidence ($0.40 - 0.69$): Amber
  - Low confidence ($< 0.40$): Rose

### 2.3 Compatibility Layer (`compat/`)
- Modular package providing pure caller-side adapters.
- Zero monkeypatches inside application endpoints.
