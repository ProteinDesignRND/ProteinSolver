# Compatibility Analysis & Runtime Adaptations

**Document:** `docs/COMPATIBILITY.md`  
**Repository:** `ProteinDesignRND/ProteinSolver`  
**Runtime:** Python 3.11.9, PyTorch 2.6.0+cu124, PyG 2.8.0.post1, BioPython 1.88  

---

## 1. Executive Summary

The upstream ProteinSolver project was developed in 2019–2020 targeting Python 3.6/3.7, PyTorch 1.3, and PyTorch Geometric 1.3 on POSIX environments (Linux). Running this codebase in modern development environments (Python 3.11+, Windows 11, PyTorch 2.6+) encounters 6 specific compatibility barriers.

Rather than casually modifying upstream code, all 6 barriers are solved through **Tier 2 Compatibility Adapters (`compat/`)**. The historical core (`proteinsolver/`) remains 100% untouched.

---

## 2. Detailed Issue Forensics & Solutions

### ISSUE-COMPAT-01: Windows Lack of POSIX `fcntl`
- **Original Failure:** `ModuleNotFoundError: No module named 'fcntl'` upon importing `proteinsolver`.
- **Root Cause:** `proteinsolver/__init__.py` imports legacy submodules that attempt to import `fcntl`, a POSIX-only C extension used for file locking on Unix filesystems. Python on Windows does not include `fcntl`.
- **Solution:** In `compat/shims.py`, inject a dummy module into `sys.modules["fcntl"]`. The core GNN model, dataset structures, and CSP design algorithm do not actually invoke `fcntl` calls at runtime.
- **Verification:** Unit tests confirm `proteinsolver` imports cleanly on Windows.

### ISSUE-COMPAT-02: Obsolete `kmbio` / `kmtools` Monolith
- **Original Failure:** `ModuleNotFoundError: No module named 'kmtools'` upon importing `proteinsolver`.
- **Root Cause:** Upstream imported `kmtools.structure_tools`, an obsolete monolithic utility library with uncompiled Cython dependencies (`kmbio`) that only had binaries for Python 3.5/3.6.
- **Solution:** 
  1. In `compat/shims.py`, stub `kmtools` and `kmtools.structure_tools` in `sys.modules`.
  2. In `compat/structure.py`, implement a cleanroom, modern structure parser using standard BioPython (`Bio.PDB`). It extracts heavy atoms ($< 12.0$ Å minimum distance) and produces the exact `ProteinData` namedtuple expected by `proteinsolver.datasets.protein.row_to_data`.
- **Verification:** On target structure 1n5uA03, the cleanroom extractor produces node features and edge attributes that are numerically identical (`max diff: 0.0`) to upstream.

### ISSUE-COMPAT-03: Removal of `torch_geometric.utils.scatter_`
- **Original Failure:** `AttributeError: module 'torch_geometric.utils' has no attribute 'scatter_'`.
- **Root Cause:** PyG 2.x removed the legacy in-place `scatter_` utility in favor of external `torch_scatter.scatter`.
- **Solution:** In `compat/shims.py`, attach a backward-compatibility wrapper to `torch_geometric.utils.scatter_`:
  ```python
  def scatter_(name, src, index, out=None, dim=0, dim_size=None):
      return torch_scatter.scatter(src, index, out=None, dim=dim, dim_size=dim_size, reduce=name)
  torch_geometric.utils.scatter_ = scatter_
  ```
- **Verification:** Message-passing in `ProteinNet` forward passes executes without attribute errors.

### ISSUE-COMPAT-04: PyG 2.x Data / Batch Behavioral Shifts
- **Original Failure:** `AttributeError: 'NoneType' object has no attribute 'max'` inside `design_sequence`.
- **Root Cause:** In modern PyG, `data.batch` defaults to `None` for single graph instances unless explicitly wrapped with `Batch.from_data_list([data])`. `design_sequence` inspects `batch.max()`.
- **Solution:** `compat/inference.py` ensures that all input graphs passed to `design_sequence` are explicitly wrapped via `Batch.from_data_list([data])`, ensuring `batch` indices are fully populated.
- **Verification:** `design_sequence` executes smoothly to sequence completion.

### ISSUE-COMPAT-05: Checkpoint State-Dict Layer Naming Divergence
- **Original Failure:** `RuntimeError: Error(s) in loading state_dict for ProteinNet: Missing key(s)... Unexpected key(s)...`.
- **Root Cause:** The published checkpoint (`e53-s1952148-d93703104.state`) was serialized from training script `protein_train/191f05de/model.py`, which used `nn.ModuleList` producing keys `graph_conv_0` and `graph_conv.0..2`. When packaged into `ProteinNet`, the author flattened these to `graph_conv_1..4`. All tensor shapes and weights are 100% identical.
- **Solution:** In `compat/checkpoint.py`, apply an explicit prefix translation dictionary:
  ```python
  KEY_MAPPING = {
      "graph_conv_0.": "graph_conv_1.",
      "graph_conv.0.": "graph_conv_2.",
      "graph_conv.1.": "graph_conv_3.",
      "graph_conv.2.": "graph_conv_4.",
  }
  ```
- **Verification:** Checkpoint loads under `strict=True` with 0 missing keys and 0 unexpected keys (45/45 tensor shapes matching, 567,060 parameters).

### ISSUE-COMPAT-06: Modern PyTorch Cross-Device Indexing in `design_sequence()`
- **Original Failure:** `RuntimeError: indices should be either on cpu or on the same device as the indexed tensor` under PyTorch 2.6 on CUDA.
- **Root Cause:** In `proteinsolver/utils/protein_design.py:224`, iterative tensor updates perform cross-device boolean indexing that PyTorch 2.6 strictly forbids on CUDA.
- **Solution:** Run iterative CSP design on CPU. Because ProteinSolver is a compact 567k parameter network, CPU inference on a 92 AA target takes only ~1.77 seconds.
- **Verification:** Clean, deterministic sequence generation with zero CUDA runtime exceptions.
