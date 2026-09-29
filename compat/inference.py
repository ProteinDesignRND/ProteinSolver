"""
ProteinSolver sequence design engine.
Enforces pure all-masked inverse folding (preventing reference sequence leakage)
and provides structured execution metadata.
"""

import time
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
import torch
from torch_geometric.data import Batch

from compat.shims import apply_shims
apply_shims()

import proteinsolver.datasets.protein as ps_protein
import proteinsolver.utils.protein_design as ps_design
from proteinsolver.utils.protein_structure import ProteinData

AMINO_ACIDS = [
    "G", "V", "A", "L", "I", "C", "M", "F", "W", "P",
    "D", "E", "S", "T", "Y", "Q", "N", "K", "R", "H"
]

@dataclass
class DesignResult:
    """Result of ProteinSolver sequence design."""
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

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def design_protein_sequence(
    model: torch.nn.Module,
    protein_data: ProteinData,
    strategy: str = "map",
    temperature: Optional[float] = None,
    seed: Optional[int] = None,
    device: str = "cpu"
) -> DesignResult:
    """
    Design an amino acid sequence from contact graph using ProteinSolver CSP.
    
    CRITICAL SECURITY & METHODOLOGICAL INVARIANT:
    All residues are initialized strictly to mask token (20).
    data.y is explicitly stripped. Zero native sequence labels can leak into the design.
    """
    if temperature is None:
        temperature = 1.0 if strategy == "map" else 0.1

    if seed is not None:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

    # 1. Pipeline: ProteinData -> PyG Data -> edge attributes -> PyG Batch
    data = ps_protein.row_to_data(protein_data)
    data = ps_protein.transform_edge_attr(data)
    batch = Batch.from_data_list([data])

    # 2. Strict all-masked initialization (no leakage)
    batch.x = torch.full_like(batch.x, 20)
    if hasattr(batch, "y"):
        delattr(batch, "y")

    # 3. Execution on target device (CPU recommended for PyTorch 2.6 cross-device indexing)
    batch = batch.to(device)
    model = model.to(device)
    model.eval()

    t0 = time.perf_counter()
    with torch.no_grad():
        designed_seq_tensor, designed_proba = ps_design.design_sequence(
            model,
            batch,
            value_selection_strategy=strategy,
            temperature=temperature,
            num_categories=20
        )
    runtime = time.perf_counter() - t0

    # 4. Map indices to standard amino acid letters
    designed_sequence = "".join(AMINO_ACIDS[idx.item()] for idx in designed_seq_tensor)
    confidences = [round(float(p.item()), 4) for p in designed_proba]
    mean_conf = float(sum(confidences) / len(confidences)) if confidences else 0.0

    return DesignResult(
        sequence=designed_sequence,
        length=len(designed_sequence),
        confidences=confidences,
        mean_confidence=round(mean_conf, 4),
        runtime_seconds=round(runtime, 4),
        strategy=strategy,
        temperature=temperature,
        seed=seed,
        device=str(device),
        mode="DESIGN_ALL_MASKED"
    )


def compute_diagnostic_recovery(designed_sequence: str, native_sequence: str) -> Dict[str, Any]:
    """
    Explicit diagnostic comparison against native sequence.
    Exposed ONLY in diagnostic mode, clearly disclaimed as an integration check.
    """
    if len(designed_sequence) != len(native_sequence):
        raise ValueError("Sequence length mismatch for recovery calculation")

    matches = sum(1 for a, b in zip(designed_sequence, native_sequence) if a == b)
    recovery_pct = (matches / len(native_sequence)) * 100.0 if native_sequence else 0.0

    return {
        "native_sequence": native_sequence,
        "designed_sequence": designed_sequence,
        "matches": matches,
        "total_residues": len(native_sequence),
        "recovery_percentage": round(recovery_pct, 2),
        "disclaimer": "Single-target integration check only. NOT a general benchmark."
    }
