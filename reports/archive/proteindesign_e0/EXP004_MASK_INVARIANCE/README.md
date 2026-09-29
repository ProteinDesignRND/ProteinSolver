# Historical Experiment EXP004: ProteinSolver Mask-Invariance & Information Leakage Audit

> [!NOTE]
> **STATUS:** HISTORICAL ARCHIVE — NON-AUTHORITATIVE FOR CURRENT MILESTONE 1 IMPLEMENTATION
> **SOURCE:** ProteinDesign research repository (`experiments/EXP004_MASK_INVARIANCE/`)
> **ORIGINAL SOURCE PATH:** `experiments/EXP004_MASK_INVARIANCE/`
> **DESTINATION:** ProteinSolver historical archive (`reports/archive/proteindesign_e0/EXP004_MASK_INVARIANCE/`)
> **PURPOSE:** Historical E0 / ProteinSolver reproduction evidence (mask invariance proof and data.y native leak mechanism demonstration)
> **CURRENT AUTHORITATIVE TESTS:** `tests/test_leak_regression.py` and `tests/test_all_masked_design.py`
> **ARCHIVAL NOTE:** Historical artifact from ProteinDesign E0 work. Later ProteinSolver forensic closure superseded terminology where necessary. Refer to current ProteinSolver reports for authoritative Milestone 1 claims.

## Overview
This experiment proved two critical scientific facts about ProteinSolver:
1. **Mask-Invariance Under All-Masked Setup:** When all node features are set to the mask token (`data.x = 20`) and `data.y = None`, the model's logits and designed sequences are 100% invariant to any extraneous residue label metadata (max absolute logit difference: `0.00000000e+00`).
2. **Native Sequence Leak Mechanism via `data.y`:** Demonstrated how attaching reference sequences in `data.y` causes `proteinsolver/utils/protein_design.py` (lines 148-176) to treat residues as pre-assigned and copy them directly using `strategy="ref"`. This explained why earlier runs erroneously appeared to report "100% recovery".

## Key Metrics
- Max Absolute Logit Difference on identical backbones with different hidden labels: `0.00000000e+00`
- Logits 100% Identical: `True`
- Sequence Output Equality: `True`
- Valid All-Masked Recovery on `1n5uA03`: `41.30%` (38/92 matches)

## Fixture Deduplication Note
The input fixture `1n5uA03.pdb` was verified byte-identical to ProteinSolver's canonical fixture:
- Canonical Path: `data/1n5uA03.pdb`
- SHA-256: `19D1FCAA81C209B96C0B0559BC1C775EF393744094CCF2FB928FFEC528B65416`
Per deduplication principles, the redundant copy was omitted from this archive.

## Archive Contents
- `config.json`: Experiment test parameters and dummy label definitions
- `metrics.json`: Verification results and logit difference statistics
- `run_log.txt`: Execution log demonstrating the leak proof
- `run_mask_invariance.py`: Verification script executing the invariance audit
