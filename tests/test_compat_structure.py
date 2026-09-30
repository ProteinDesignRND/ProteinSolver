import pytest
from compat.structure import get_available_chains, parse_structure_to_protein_data

def test_get_available_chains(example_1n5u_pdb):
    chains = get_available_chains(example_1n5u_pdb)
    assert len(chains) == 1
    c = chains[0]
    assert c["chain_id"] == "A"
    assert c["residue_count"] == 92
    assert c["first_res_id"] == 205
    assert c["last_res_id"] == 296

def test_parse_structure_to_protein_data(example_1n5u_pdb):
    pdata, native_seq = parse_structure_to_protein_data(example_1n5u_pdb, chain_id="A")
    assert len(native_seq) == 92
    assert pdata.sequence == native_seq
    assert pdata.row_index.dim() == 1
    assert pdata.col_index.dim() == 1
    assert pdata.distances.dim() == 1
    assert len(pdata.row_index) == len(pdata.col_index) == len(pdata.distances)
    # Check that all distances are within cutoff 12.0 A
    assert (pdata.distances <= 12.0).all().item() is True
