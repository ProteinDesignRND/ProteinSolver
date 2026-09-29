"""
ProteinSolver Compatibility & Modern Execution Package.
"""

from compat.shims import apply_shims
from compat.structure import parse_structure_to_protein_data, get_available_chains
from compat.checkpoint import load_proteinsolver_model, KEY_MAPPING, EXPECTED_SHA256, EXPECTED_PARAMS
from compat.inference import design_protein_sequence, compute_diagnostic_recovery, DesignResult, AMINO_ACIDS

__all__ = [
    "apply_shims",
    "parse_structure_to_protein_data",
    "get_available_chains",
    "load_proteinsolver_model",
    "design_protein_sequence",
    "compute_diagnostic_recovery",
    "DesignResult",
    "AMINO_ACIDS",
    "KEY_MAPPING",
    "EXPECTED_SHA256",
    "EXPECTED_PARAMS",
]
