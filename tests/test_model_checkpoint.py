import pytest
import hashlib
import torch
from compat.checkpoint import load_proteinsolver_model, EXPECTED_PARAMS, EXPECTED_SHA256
from compat.structure import parse_structure_to_protein_data
import proteinsolver.datasets.protein as ps_protein

def test_checkpoint_hash(checkpoint_path):
    h = hashlib.sha256()
    with open(checkpoint_path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    assert h.hexdigest().upper() == EXPECTED_SHA256

def test_load_model_parameters(checkpoint_path):
    model = load_proteinsolver_model(str(checkpoint_path), device="cpu")
    param_count = sum(p.numel() for p in model.parameters())
    assert param_count == EXPECTED_PARAMS
    assert param_count == 567060
    assert not model.training

def test_forward_pass(checkpoint_path, example_1n5u_pdb):
    model = load_proteinsolver_model(str(checkpoint_path), device="cpu")
    pdata, _ = parse_structure_to_protein_data(example_1n5u_pdb, chain_id="A")
    data = ps_protein.row_to_data(pdata)
    data = ps_protein.transform_edge_attr(data)
    
    # Initialize all nodes to mask token (20)
    data.x = torch.full_like(data.x, 20)
    
    with torch.no_grad():
        out = model(data.x, data.edge_index, data.edge_attr)
    
    # Output logits shape: [num_nodes, 20]
    assert out.shape == (92, 20)
    assert not torch.isnan(out).any()
