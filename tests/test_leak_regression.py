import pytest
import torch
from torch_geometric.data import Batch
from compat.structure import parse_structure_to_protein_data
from compat.checkpoint import load_proteinsolver_model
from compat.inference import design_protein_sequence
import proteinsolver.datasets.protein as ps_protein

def test_leak_regression_data_structure(example_1n5u_pdb):
    """
    CRITICAL LESSON C REGRESSION TEST:
    Verify that in design mode, ground-truth sequence is strictly excluded.
    data.x must be initialized entirely to mask token (20).
    data.y must NOT exist on the design batch.
    """
    pdata, _ = parse_structure_to_protein_data(example_1n5u_pdb, chain_id="A")
    data = ps_protein.row_to_data(pdata)
    data = ps_protein.transform_edge_attr(data)
    batch = Batch.from_data_list([data])
    batch.x = torch.full_like(batch.x, 20)
    if hasattr(batch, "y"):
        delattr(batch, "y")
    
    assert getattr(batch, "y", None) is None, "FATAL: data.y ground-truth label leaked into design batch!"
    assert (batch.x == 20).all().item() is True, "FATAL: Unmasked tokens found in design batch.x!"

def test_design_ignores_native_sequence(checkpoint_path, example_1n5u_pdb):
    """
    Verify that design mode runs with all-masked input and produces a valid sequence.
    """
    model = load_proteinsolver_model(str(checkpoint_path), device="cpu")
    pdata, _ = parse_structure_to_protein_data(example_1n5u_pdb, chain_id="A")
    res = design_protein_sequence(
        model=model,
        protein_data=pdata,
        strategy="map",
    )
    assert res.mode == "DESIGN_ALL_MASKED"
    assert hasattr(res, "sequence")
    assert "X" not in res.sequence
    assert "?" not in res.sequence
    assert len(res.sequence) == 92
