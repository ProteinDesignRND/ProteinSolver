"""
Pydantic schemas for request and response validation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
    python_version: str
    torch_version: str
    cuda_available: bool
    device: str
    model_loaded: bool
    parameter_count: int


class ModelResponse(BaseModel):
    model_name: str = "ProteinSolver"
    model_class: str = "ProteinNet"
    architecture: str = "4-block EdgeConv Residual GNN"
    parameter_count: int = 567060
    input_node_features: int = 21  # 20 amino acids + 1 mask token
    input_edge_features: int = 2   # distance + sequence separation
    hidden_size: int = 128
    output_size: int = 20          # 20 amino acid logits
    checkpoint_sha256: str = "1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727"
    checkpoint_loaded: bool


class ChainInfo(BaseModel):
    chain_id: str
    residue_count: int
    first_res_id: int
    last_res_id: int


class ValidateStructureRequest(BaseModel):
    pdb_content: str = Field(..., description="PDB structure as text")


class ValidateStructureResponse(BaseModel):
    valid: bool
    chains: List[ChainInfo] = []
    error: Optional[str] = None


class ExampleStructure(BaseModel):
    id: str
    name: str
    filename: str
    chain_id: str
    residue_count: int
    description: str


class DesignRequest(BaseModel):
    pdb_content: str = Field(..., description="PDB file content as text")
    chain_id: str = Field(default="A", description="Chain ID to design")
    strategy: str = Field(default="map", description="Selection strategy: 'map' (greedy argmax) or 'multinomial'")
    temperature: Optional[float] = Field(default=None, description="Sampling temperature (default 1.0 for map, 0.1 for multinomial)")
    seed: Optional[int] = Field(default=None, description="Random seed for reproducibility")


class DesignResponse(BaseModel):
    sequence: str
    length: int
    confidences: List[float]
    mean_confidence: float
    runtime_seconds: float
    strategy: str
    temperature: float
    seed: Optional[int]
    device: str
    mode: str = "DESIGN_ALL_MASKED"


class DiagnosticRequest(BaseModel):
    pdb_content: str = Field(..., description="PDB file content as text")
    chain_id: str = Field(default="A", description="Chain ID to evaluate")
    strategy: str = Field(default="map", description="Selection strategy")
    temperature: Optional[float] = Field(default=None, description="Sampling temperature")
    seed: Optional[int] = Field(default=None, description="Random seed")


class DiagnosticResponse(BaseModel):
    design: DesignResponse
    native_sequence: str
    matches: int
    total_residues: int
    recovery_percentage: float
    disclaimer: str = "Single-target integration check only. NOT a general benchmark."
