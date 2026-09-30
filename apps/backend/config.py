"""
Backend configuration and settings.
"""

from pathlib import Path
from pydantic import BaseModel

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CHECKPOINT = REPO_ROOT / "data" / "e53-s1952148-d93703104.state"
INPUTS_DIR = REPO_ROOT / "proteinsolver" / "data" / "inputs"

class Settings(BaseModel):
    title: str = "ProteinSolver API"
    version: str = "1.0.0"
    description: str = "FastAPI service for ProteinSolver Graph Neural Network Inverse Protein Design"
    checkpoint_path: str = str(DEFAULT_CHECKPOINT)
    inputs_dir: str = str(INPUTS_DIR)
    host: str = "127.0.0.1"
    port: int = 8000

settings = Settings()
