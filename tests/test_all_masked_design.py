import pytest
from compat.checkpoint import load_proteinsolver_model
from compat.structure import parse_structure_to_protein_data
from compat.inference import design_protein_sequence

VALID_AA = set("ACDEFGHIKLMNPQRSTVWY")

def test_greedy_map_design(checkpoint_path, example_1n5u_pdb):
    model = load_proteinsolver_model(str(checkpoint_path), device="cpu")
    pdata, _ = parse_structure_to_protein_data(example_1n5u_pdb, chain_id="A")
    res = design_protein_sequence(
        model=model,
        protein_data=pdata,
        strategy="map",
        temperature=1.0,
    )
    assert len(res.sequence) == 92
    assert set(res.sequence).issubset(VALID_AA)
    assert res.length == 92
    assert len(res.confidences) == 92
    assert 0.0 <= res.mean_confidence <= 1.0
    assert res.strategy == "map"
    assert res.mode == "DESIGN_ALL_MASKED"

def test_multinomial_seed_determinism(checkpoint_path, example_1n5u_pdb):
    model = load_proteinsolver_model(str(checkpoint_path), device="cpu")
    pdata, _ = parse_structure_to_protein_data(example_1n5u_pdb, chain_id="A")
    res1 = design_protein_sequence(
        model=model,
        protein_data=pdata,
        strategy="multinomial",
        temperature=0.1,
        seed=42,
    )
    res2 = design_protein_sequence(
        model=model,
        protein_data=pdata,
        strategy="multinomial",
        temperature=0.1,
        seed=42,
    )
    assert res1.sequence == res2.sequence
    assert res1.confidences == res2.confidences
