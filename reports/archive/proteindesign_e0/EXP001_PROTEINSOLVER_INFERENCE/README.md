# Historical Experiment EXP001: ProteinSolver Real Inference & Determinism Reproducibility Test

> [!NOTE]
> **STATUS:** HISTORICAL ARCHIVE — NON-AUTHORITATIVE FOR CURRENT MILESTONE 1 IMPLEMENTATION
> **SOURCE:** ProteinDesign research repository (`experiments/EXP001_PROTEINSOLVER_INFERENCE/`)
> **ORIGINAL SOURCE PATH:** `experiments/EXP001_PROTEINSOLVER_INFERENCE/`
> **DESTINATION:** ProteinSolver historical archive (`reports/archive/proteindesign_e0/EXP001_PROTEINSOLVER_INFERENCE/`)
> **PURPOSE:** Historical E0 / ProteinSolver reproduction evidence (inference determinism and multi-target testing)
> **CURRENT AUTHORITATIVE TESTS:** `tests/test_integration_1n5u.py` and `apps/backend/service.py`
> **ARCHIVAL NOTE:** Historical artifact from ProteinDesign E0 work. Later ProteinSolver forensic closure superseded terminology where necessary. Refer to current ProteinSolver reports for authoritative Milestone 1 claims.

## Overview
This experiment assessed the deterministic reproducibility of the CSP iterative unmasking algorithm across different sampling temperatures (MAP/greedy, T=0.1, T=0.5, T=1.0) on two targets:
1. `1n5uA03` (92 AA, paper demo CATH domain)
2. `1UBQ` (76 AA, human ubiquitin)

## Key Results
- Fixed random seeds yield bitwise identical designed sequences across runs.
- On `1n5uA03`, MAP greedy design achieved 41.30% recovery (38/92 matches) under all-masked design (`data.x = 20`, `data.y = None`).
- Formally classified as a single-target all-masked integration result, not a cross-fold benchmark.

## Fixture Deduplication & Data Policy Note
- The input fixture `1n5uA03.pdb` was verified byte-identical to ProteinSolver's canonical fixture:
  - Canonical Path: `data/1n5uA03.pdb`
  - SHA-256: `19D1FCAA81C209B96C0B0559BC1C775EF393744094CCF2FB928FFEC528B65416`
  Per deduplication principles, redundant copy was omitted from this archive.
- The external test fixture `1UBQ.pdb` (SHA-256: `D4A6812D8951CF6594E6A0763F089E35F5A80B62ACB3C117B2C5565228A7B161`) is documented in `TRANSFER_MANIFEST.md`; its full design results are archived below in `output/` and `metrics.json`.

## Archive Contents
- `config.json`: Sampling configurations and target declarations
- `metrics.json`: Per-target, per-temperature recovery metrics and runtime
- `run_inference.py`: Python script executing the multi-target CSP design
- `run_log.txt`: Console execution log (sanitized of machine-specific absolute paths)
- `output/designed_sequences.csv`: Generated sequence records
- `output/inference_summary.csv`: Summary metrics table
- `output/reproducibility_check.json`: Multi-run bitwise identity validation records
