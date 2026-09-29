import sys
import os
import pytest
from pathlib import Path

# Ensure root directory and compat are on sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Apply compatibility shims before any tests import proteinsolver
import compat.shims
compat.shims.apply_shims()

def pytest_ignore_collect(collection_path, config):
    """
    Ignore obsolete legacy tests that rely on external RCSB network access
    and deprecated kmbio modules documented in docs/KNOWN_LIMITATIONS.md.
    """
    p = str(collection_path or path)
    if "test_protein_structure.py" in p:
        return True
    return False

@pytest.fixture(scope="session")
def example_1n5u_pdb():
    pdb_path = root_dir / "data" / "1n5uA03.pdb"
    assert pdb_path.exists(), f"1n5uA03.pdb fixture not found at {pdb_path}"
    return pdb_path.read_text(encoding="utf-8")

@pytest.fixture(scope="session")
def checkpoint_path():
    ckpt = root_dir / "data" / "e53-s1952148-d93703104.state"
    assert ckpt.exists(), f"Pretrained checkpoint not found at {ckpt}"
    return ckpt
