# Setup & Installation Guide

**Document:** `docs/SETUP.md`  
**Repository:** `ProteinDesignRND/ProteinSolver`  

---

## 1. Prerequisites

- **Operating System:** Windows 10/11 (verified environment: Windows 11); Linux/macOS setup paths provided as unverified references
- **Python:** 3.11.x (tested on Python 3.11.9)
- **Node.js:** `>=20.19.0` (tested on Node.js v24.18.0, npm 11.16.0)
- **Hardware:** CPU or NVIDIA GPU with CUDA support

---

## 2. Installation Steps

### Step 2.1: Clone the Repository
```bash
git clone https://github.com/ProteinDesignRND/ProteinSolver.git
cd ProteinSolver
git checkout feature/milestone-1-full-implementation
```

### Step 2.2: Setup Python Virtual Environment
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
Or with standard `pip`:
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install -e . --no-deps
```

### Step 2.3: Verify Checkpoint
The verified published checkpoint is included at:
`data/e53-s1952148-d93703104.state` (SHA-256: `1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727`).

### Step 2.4: Setup Frontend
```bash
cd apps/frontend
npm ci
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
