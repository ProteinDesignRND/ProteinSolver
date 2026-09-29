# Setup & Installation Guide

**Document:** `docs/SETUP.md`  
**Repository:** `ProteinDesignRND/ProteinSolver`  

---

## 1. Prerequisites

- **Operating System:** Windows 10/11, Ubuntu 20.04+, or macOS
- **Python:** 3.10 or 3.11 (tested on Python 3.11.9)
- **Node.js:** v18+ (tested on Node.js v24.18.0)
- **Hardware:** CPU or NVIDIA GPU with CUDA support

---

## 2. Installation Steps

### Step 2.1: Clone the Repository
```bash
git clone https://github.com/ProteinDesignRND/ProteinSolver.git
cd ProteinSolver
```

### Step 2.2: Setup Python Virtual Environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
pip install torch_geometric torch_scatter biopython fastapi uvicorn pydantic pytest
```

### Step 2.3: Verify Checkpoint
The verified published checkpoint is included at:
`data/e53-s1952148-d93703104.state` (SHA-256: `1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727`).

### Step 2.4: Setup Frontend
```bash
cd apps/frontend
npm install
cd ../..
```

---

## 3. Running Tests
```bash
pytest tests/ -v
```

---

## 4. Running the Application
### Terminal 1: Backend (from repository root)
```bash
python -m apps.backend.main
```
*(Or alternatively: `python -m uvicorn apps.backend.main:app --host 127.0.0.1 --port 8000`)*

### Terminal 2: Frontend (from repository root)
```bash
npm --prefix apps/frontend run dev
```
*(Or alternatively: `cd apps/frontend && npm run dev`)*

Open your browser at `http://localhost:5173`.
