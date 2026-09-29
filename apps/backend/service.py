"""
Service layer encapsulating ProteinSolver model singleton and operations.
"""

import sys
import platform
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
import torch

from apps.backend.config import settings
from apps.backend.schemas import (
    HealthResponse,
    ModelResponse,
    ChainInfo,
    ValidateStructureResponse,
    ExampleStructure,
    DesignResponse,
    DiagnosticResponse,
)

from compat import (
    load_proteinsolver_model,
    parse_structure_to_protein_data,
    get_available_chains,
    design_protein_sequence,
    compute_diagnostic_recovery,
    EXPECTED_PARAMS,
    EXPECTED_SHA256,
)


class ProteinSolverService:
    """Singleton service managing the ProteinSolver model and inference operations."""
    
    _instance: Optional["ProteinSolverService"] = None

    def __init__(self):
        self.device = "cpu"  # CPU recommended for PyTorch 2.6 cross-device indexing compatibility
        self.model = None
        self.checkpoint_sha256 = None
        self._load_model()

    @classmethod
    def get_instance(cls) -> "ProteinSolverService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_model(self) -> None:
        try:
            ckpt_path = Path(settings.checkpoint_path)
            if not ckpt_path.exists():
                raise FileNotFoundError(f"Checkpoint not found at: {ckpt_path}")
            self.checkpoint_sha256 = hashlib.sha256(ckpt_path.read_bytes()).hexdigest().upper()
            self.model = load_proteinsolver_model(str(ckpt_path), device=self.device)
            param_count = sum(p.numel() for p in self.model.parameters())
            print(f"[Service] ProteinSolver model loaded on {self.device} (params: {param_count:,})")
        except Exception as e:
            print(f"[Service] WARNING: Failed to load model: {e}")
            self.model = None

    def get_health(self) -> HealthResponse:
        param_count = sum(p.numel() for p in self.model.parameters()) if self.model else 0
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            python_version=platform.python_version(),
            torch_version=torch.__version__,
            cuda_available=torch.cuda.is_available(),
            device=self.device,
            model_loaded=self.model is not None,
            parameter_count=param_count,
        )

    def get_model_info(self) -> ModelResponse:
        model_loaded = self.model is not None
        param_count = sum(p.numel() for p in self.model.parameters()) if model_loaded else 0
        model_cls = self.model.__class__.__name__ if model_loaded else "ProteinNet"
        hidden_sz = getattr(self.model, "hidden_size", 128) if model_loaded else 128
        return ModelResponse(
            model_name="ProteinSolver",
            model_class=model_cls,
            architecture="4-block EdgeConv Residual GNN",
            parameter_count=param_count if model_loaded else EXPECTED_PARAMS,
            input_node_features=21,
            input_edge_features=2,
            hidden_size=hidden_sz,
            output_size=20,
            checkpoint_sha256=self.checkpoint_sha256 or EXPECTED_SHA256,
            checkpoint_loaded=model_loaded,
        )

    def validate_structure(self, pdb_content: str) -> ValidateStructureResponse:
        try:
            chains_data = get_available_chains(pdb_content)
            if not chains_data:
                return ValidateStructureResponse(valid=False, chains=[], error="No valid protein chains found in structure")
            
            chains = [
                ChainInfo(
                    chain_id=c["chain_id"],
                    residue_count=c["residue_count"],
                    first_res_id=c["first_res_id"],
                    last_res_id=c["last_res_id"],
                )
                for c in chains_data
            ]
            return ValidateStructureResponse(valid=True, chains=chains, error=None)
        except Exception as e:
            return ValidateStructureResponse(valid=False, chains=[], error=str(e))

    def get_examples(self) -> List[ExampleStructure]:
        examples = [
            ExampleStructure(
                id="1n5uA03",
                name="1n5uA03 (CATH domain)",
                filename="1n5uA03.pdb",
                chain_id="A",
                residue_count=92,
                description="Classic 92-residue alpha-helical CATH domain from historical publication. Integration sanity check target."
            ),
            ExampleStructure(
                id="3fndA02",
                name="3fndA02 (CATH domain)",
                filename="3fndA02.pdb",
                chain_id="A",
                residue_count=45,
                description="Small 45-residue domain included with upstream inputs."
            ),
            ExampleStructure(
                id="4unuA00",
                name="4unuA00 (CATH domain)",
                filename="4unuA00.pdb",
                chain_id="A",
                residue_count=107,
                description="107-residue globular protein domain from upstream inputs."
            ),
        ]
        return examples

    def get_example_pdb(self, example_id: str) -> str:
        base_dir = Path(settings.inputs_dir).resolve()
        clean_id = Path(example_id).name
        if clean_id != example_id or not clean_id.replace("_", "").replace("-", "").isalnum():
            raise ValueError(f"Invalid example identifier: {example_id}")
        pdb_path = (base_dir / f"{clean_id}.pdb").resolve()
        if not pdb_path.is_relative_to(base_dir):
            raise ValueError(f"Invalid example path traversal: {example_id}")
        if not pdb_path.exists() or not pdb_path.is_file():
            raise FileNotFoundError(f"Example file not found: {clean_id}.pdb")
        return pdb_path.read_text(encoding="utf-8")

    def run_design(
        self,
        pdb_content: str,
        chain_id: str = "A",
        strategy: str = "map",
        temperature: Optional[float] = None,
        seed: Optional[int] = None,
    ) -> DesignResponse:
        if self.model is None:
            raise RuntimeError("ProteinSolver model is not loaded")

        pdata, _ = parse_structure_to_protein_data(pdb_content, chain_id=chain_id)
        result = design_protein_sequence(
            self.model,
            pdata,
            strategy=strategy,
            temperature=temperature,
            seed=seed,
            device=self.device
        )
        return DesignResponse(**result.to_dict())

    def run_diagnostic(
        self,
        pdb_content: str,
        chain_id: str = "A",
        strategy: str = "map",
        temperature: Optional[float] = None,
        seed: Optional[int] = None,
    ) -> DiagnosticResponse:
        if self.model is None:
            raise RuntimeError("ProteinSolver model is not loaded")

        pdata, native_seq = parse_structure_to_protein_data(pdb_content, chain_id=chain_id)
        result = design_protein_sequence(
            self.model,
            pdata,
            strategy=strategy,
            temperature=temperature,
            seed=seed,
            device=self.device
        )
        diag = compute_diagnostic_recovery(result.sequence, native_seq)
        return DiagnosticResponse(
            design=DesignResponse(**result.to_dict()),
            native_sequence=native_seq,
            matches=diag["matches"],
            total_residues=diag["total_residues"],
            recovery_percentage=diag["recovery_percentage"],
            disclaimer=diag["disclaimer"]
        )