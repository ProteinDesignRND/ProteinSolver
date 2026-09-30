# Historical Experiment EXP000: ProteinSolver Smoke Test

> [!NOTE]
> **STATUS:** HISTORICAL ARCHIVE — NON-AUTHORITATIVE FOR CURRENT MILESTONE 1 IMPLEMENTATION
> **SOURCE:** ProteinDesign research repository (`experiments/EXP000_PROTEINSOLVER_SMOKETEST/`)
> **ORIGINAL SOURCE PATH:** `experiments/EXP000_PROTEINSOLVER_SMOKETEST/`
> **DESTINATION:** ProteinSolver historical archive (`reports/archive/proteindesign_e0/EXP000_PROTEINSOLVER_SMOKETEST/`)
> **PURPOSE:** Historical E0 / ProteinSolver reproduction evidence (initial model instantiation & checkpoint forward pass)
> **CURRENT AUTHORITATIVE TESTS:** `tests/test_model_checkpoint.py` and `tests/test_compat_shims.py`
> **ARCHIVAL NOTE:** Historical artifact from ProteinDesign E0 work. Later ProteinSolver forensic closure superseded terminology where necessary. Refer to current ProteinSolver reports for authoritative Milestone 1 claims.

## Overview
This experiment verified the initial loading and forward pass of the official ProteinSolver checkpoint (`e53-s1952148-d93703104.state`) into the 4-block EdgeConv architecture (567,060 parameters, hidden dimension 128) under modern Python 3.11 / PyG 2.8.

## Fixture Deduplication Note
The input fixture `1n5uA03.pdb` was verified byte-identical to ProteinSolver's canonical fixture:
- Canonical Path: `data/1n5uA03.pdb`
- SHA-256: `19D1FCAA81C209B96C0B0559BC1C775EF393744094CCF2FB928FFEC528B65416`
Per deduplication principles, the redundant copy was omitted from this archive.

## Archive Contents
- `config.json`: Experiment configuration and target specifications
- `environment.txt`: Runtime environment audit snapshot
- `metrics.json`: Execution metrics (parameter count, runtime, validation checks)
- `run_log.txt`: Console output log from historical execution
- `run_smoketest.py`: Execution script for the smoketest
