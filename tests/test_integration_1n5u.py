import pytest
from compat.checkpoint import load_proteinsolver_model
from compat.structure import parse_structure_to_protein_data
from compat.inference import design_protein_sequence, compute_diagnostic_recovery

def test_reproduce_exact_1n5u_baseline(checkpoint_path, example_1n5u_pdb):
    """
    FUNCTIONAL REPRODUCTION VERIFICATION:
    Verifies that running MAP greedy search with ProteinSolver reproduced
    the verified baseline of 41.30% recovery (38/92 residues) on 1n5uA03.
    """
    model = load_proteinsolver_model(str(checkpoint_path), device="cpu")
    pdata, native_seq = parse_structure_to_protein_data(example_1n5u_pdb, chain_id="A")
    design_res = design_protein_sequence(
        model=model,
        protein_data=pdata,
        strategy="map",
        temperature=1.0,
    )
    diag = compute_diagnostic_recovery(design_res.sequence, native_seq)
    
    assert diag["total_residues"] == 92
    assert diag["matches"] == 38
    assert diag["recovery_percentage"] == 41.30
    assert len(design_res.sequence) == 92
    assert design_res.mode == "DESIGN_ALL_MASKED"
