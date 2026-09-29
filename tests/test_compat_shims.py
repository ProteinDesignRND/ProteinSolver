import pytest
import sys
import torch

def test_fcntl_stub():
    import fcntl
    assert hasattr(fcntl, "flock")
    assert hasattr(fcntl, "lockf")
    assert hasattr(fcntl, "fcntl")
    assert hasattr(fcntl, "LOCK_EX")
    assert hasattr(fcntl, "LOCK_SH")
    assert hasattr(fcntl, "LOCK_UN")
    assert hasattr(fcntl, "LOCK_NB")
    # Calling flock/lockf on Windows fails loudly rather than pretending locking works
    with pytest.raises(NotImplementedError):
        fcntl.flock(0, fcntl.LOCK_EX)
    with pytest.raises(NotImplementedError):
        fcntl.lockf(0, fcntl.LOCK_EX)

def test_kmtools_stub():
    from kmtools import structure_tools
    assert hasattr(structure_tools, "parse_pdb")
    assert hasattr(structure_tools, "extract_seq_and_adj")

def test_pyg_scatter_shim():
    from torch_geometric.utils import scatter_
    src = torch.tensor([1.0, 2.0, 3.0, 4.0])
    index = torch.tensor([0, 0, 1, 1])
    out = torch.zeros(2)
    scatter_("add", src, index, out=out)
    assert torch.allclose(out, torch.tensor([3.0, 7.0]))
