"""
Runtime shims for modern compatibility.
Enables execution on Windows and with modern PyTorch Geometric.
"""

import sys
import types
import torch
import torch_geometric
import torch_scatter

def _scatter_(name, src, index, out=None, dim=0, dim_size=None):
    """Shim for torch_geometric.utils.scatter_ using torch_scatter.scatter."""
    return torch_scatter.scatter(src, index, out=out, dim=dim, dim_size=dim_size, reduce=name)

def apply_shims() -> None:
    """Apply transparent compatibility shims if not already present."""
    # 1. fcntl dummy module for Windows
    # Fails loudly on locking operations rather than silently pretending locks exist
    if "fcntl" not in sys.modules:
        sys.modules["fcntl"] = types.ModuleType("fcntl")
    fcntl_mod = sys.modules["fcntl"]
    def _unsupported_locking(*args, **kwargs):
        raise NotImplementedError("POSIX file locking (fcntl) is not supported on Windows. Avoid concurrent file mutation.")
    for fn in ["flock", "lockf", "fcntl"]:
        setattr(fcntl_mod, fn, _unsupported_locking)
    fcntl_mod.LOCK_EX = getattr(fcntl_mod, "LOCK_EX", 2)
    fcntl_mod.LOCK_SH = getattr(fcntl_mod, "LOCK_SH", 1)
    fcntl_mod.LOCK_NB = getattr(fcntl_mod, "LOCK_NB", 4)
    fcntl_mod.LOCK_UN = getattr(fcntl_mod, "LOCK_UN", 8)

    # 2. kmtools and kmbio dummy stubs to isolate neural network / design pipelines
    sys.modules.setdefault("kmtools", types.ModuleType("kmtools"))
    if "kmtools.structure_tools" not in sys.modules:
        sys.modules["kmtools.structure_tools"] = types.ModuleType("kmtools.structure_tools")
    st_mod = sys.modules["kmtools.structure_tools"]
    if not hasattr(st_mod, "parse_pdb"):
        st_mod.parse_pdb = lambda *args, **kwargs: None
    if not hasattr(st_mod, "extract_seq_and_adj"):
        st_mod.extract_seq_and_adj = lambda *args, **kwargs: None

    sys.modules.setdefault("kmbio", types.ModuleType("kmbio"))
    sys.modules.setdefault("kmbio.PDB", types.ModuleType("kmbio.PDB"))

    # 3. torch_geometric.utils.scatter_ backward-compatibility shim
    if not hasattr(torch_geometric.utils, "scatter_"):
        torch_geometric.utils.scatter_ = _scatter_

    # 4. ruamel.yaml safe_load compatibility shim for modern ruamel.yaml 0.18+
    try:
        import ruamel.yaml
        def _yaml_safe_load(stream):
            y = ruamel.yaml.YAML(typ="safe", pure=True)
            return y.load(stream)
        ruamel.yaml.safe_load = _yaml_safe_load
    except ImportError:
        pass

apply_shims()
