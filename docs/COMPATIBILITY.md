# Compatibility Analysis & Modern Runtime Adapters

This document details the forensic root cause, resolution, test coverage, and limitations for all **seven (7)** historical compatibility adaptations in `compat/`.

---

## Compatibility Issue Index

| Issue ID | Subsystem | Upstream Incompatibility | Modern Resolution | Test Verification |
| :--- | :--- | :--- | :--- | :--- |
| **COMPAT-01** | OS Portability | Unix-only `fcntl` module fails on Windows | `compat/shims.py`: registers `fcntl` stub. Calls to `flock`/`lockf` raise `NotImplementedError` rather than silently simulating locks. | `tests/test_compat_shims.py::test_fcntl_stub` |
| **COMPAT-02** | Structure Parsing | Dead `kmbio`/`kmtools` fail on Python 3.11 | `compat/shims.py` stubs modules; `compat/structure.py` provides cleanroom BioPython coordinate & contact extraction ($r < 12.0$ Å). | `tests/test_compat_structure.py` |
| **COMPAT-03** | PyG Operators | `torch_geometric.utils.scatter_` removed in PyG 2.x | `compat/shims.py`: routes `scatter_` to `torch_scatter.scatter(..., out=out)` with in-place tensor modification. | `tests/test_compat_shims.py::test_pyg_scatter_shim` |
| **COMPAT-04** | PyG Batching | PyG 2.8 batching semantics changed from PyG 1.x | Explicit `Batch.from_data_list([data])` construction with tensor device assignment. | `tests/test_all_masked_design.py` |
| **COMPAT-05** | State Dict Keys | Checkpoint uses training names (`graph_conv_0.`) vs packaged (`graph_conv_1.`) | `compat/checkpoint.py`: deterministic prefix translation mapping. Validates 567,060 parameters against SHA-256. | `tests/test_model_checkpoint.py` |
| **COMPAT-06** | Tensor Indexing | CUDA boolean indexing assertions in PyTorch 2.6 `design_sequence` | Standardized CSP inference execution to CPU (`device="cpu"`), completing a 92-residue domain in ~1.5s with zero crash risk. | `tests/test_integration_1n5u.py` |
| **COMPAT-07** | YAML Parsing | Modern `ruamel.yaml` deprecated `yaml.safe_load(...)` | `compat/shims.py`: routes `safe_load` to `YAML(typ='safe', pure=True).load`. | `tests/utils/test_sudoku.py` |

---

## Architectural Principle
All compatibility adapters are isolated strictly inside `compat/`. Zero lines of code within the original upstream package (`proteinsolver/`) were modified.
