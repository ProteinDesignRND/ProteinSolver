"""
FastAPI application entrypoint for ProteinSolver backend.
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from apps.backend.config import settings
from apps.backend.schemas import (
    HealthResponse,
    ModelResponse,
    ValidateStructureRequest,
    ValidateStructureResponse,
    ExampleStructure,
    DesignRequest,
    DesignResponse,
    DiagnosticRequest,
    DiagnosticResponse,
)
from apps.backend.service import ProteinSolverService

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize service and preload model
    service = ProteinSolverService.get_instance()
    yield

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    lifespan=lifespan,
)

# Enable CORS for local Vite development origins (port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse, tags=["System"])
def get_health():
    """Return health status, device information, and model state."""
    service = ProteinSolverService.get_instance()
    return service.get_health()


@app.get("/api/model", response_model=ModelResponse, tags=["Model"])
def get_model_info():
    """Return ProteinSolver architecture details, parameter counts, and checkpoint metadata."""
    service = ProteinSolverService.get_instance()
    return service.get_model_info()


@app.get("/api/examples", response_model=List[ExampleStructure], tags=["Examples"])
def list_examples():
    """List built-in example structure fixtures suitable for 1-click mentor demonstration."""
    service = ProteinSolverService.get_instance()
    return service.get_examples()


@app.get("/api/examples/{example_id}", tags=["Examples"])
def get_example_pdb(example_id: str):
    """Retrieve raw PDB text for a built-in example structure."""
    service = ProteinSolverService.get_instance()
    try:
        content = service.get_example_pdb(example_id)
        return {"id": example_id, "pdb_content": content}
    except (ValueError, FileNotFoundError) as e:
        status_code = status.HTTP_400_BAD_REQUEST if isinstance(e, ValueError) else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status_code, detail=str(e))


@app.post("/api/validate", response_model=ValidateStructureResponse, tags=["Design"])
def validate_structure(req: ValidateStructureRequest):
    """Validate a PDB structure text and return available chains and residue counts."""
    service = ProteinSolverService.get_instance()
    return service.validate_structure(req.pdb_content)


@app.post("/api/design", response_model=DesignResponse, tags=["Design"])
def design_sequence(req: DesignRequest):
    """
    Execute real ProteinSolver inverse protein design.
    
    Design-path input invariant enforced by the compatibility/application layer
    and protected by regression tests.
    """
    service = ProteinSolverService.get_instance()
    try:
        return service.run_design(
            pdb_content=req.pdb_content,
            chain_id=req.chain_id,
            strategy=req.strategy,
            temperature=req.temperature,
            seed=req.seed,
        )
    except (ValueError, FileNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected error in /api/design: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error executing ProteinSolver design."
        )


@app.post("/api/diagnostic", response_model=DiagnosticResponse, tags=["Diagnostic"])
def evaluate_diagnostic(req: DiagnosticRequest):
    """
    Execute design and compute diagnostic recovery against the native sequence.
    
    DISCLAIMER: This is strictly a single-target integration check, not a benchmark claim.
    """
    service = ProteinSolverService.get_instance()
    try:
        return service.run_diagnostic(
            pdb_content=req.pdb_content,
            chain_id=req.chain_id,
            strategy=req.strategy,
            temperature=req.temperature,
            seed=req.seed,
        )
    except (ValueError, FileNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected error in /api/diagnostic: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error executing ProteinSolver diagnostic."
        )


if __name__ == "__main__":
    import uvicorn
    # Default reload to False for mentor/demo execution; allow PROTEINSOLVER_RELOAD=1 for dev
    use_reload = os.environ.get("PROTEINSOLVER_RELOAD", "false").lower() in ("true", "1")
    uvicorn.run("apps.backend.main:app", host=settings.host, port=settings.port, reload=use_reload)