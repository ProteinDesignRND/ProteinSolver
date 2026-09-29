# Historical E0 Evidence Transfer Manifest: ProteinDesign -> ProteinSolver

> [!NOTE]
> **STATUS:** HISTORICAL ARCHIVE PROVENANCE MANIFEST
> **PURPOSE:** Permanent provenance record documenting the transfer, classification, sanitization, and cryptographic verification of historical Milestone 1 / E0 evidence from the ProteinDesign research repository into the ProteinSolver implementation repository.
> **CURRENT IMPLEMENTATION AUTHORITY:** [MILESTONE_1_FINAL_REPORT.md](../../MILESTONE_1_FINAL_REPORT.md), [UPSTREAM_PROVENANCE.md](../../../docs/UPSTREAM_PROVENANCE.md), [COMPATIBILITY.md](../../../docs/COMPATIBILITY.md), and [ORIGINAL_PROJECT_PARITY.md](../../../docs/ORIGINAL_PROJECT_PARITY.md).

---

## 1. Transfer Metadata

| Metadata Field | Value |
| :--- | :--- |
| **Source Repository** | `D:\Projects\Protein Design` (`ProteinDesignRND/ProteinDesign`) |
| **Destination Repository** | `D:\Projects\ProteinSolver` (`ProteinDesignRND/ProteinSolver`) |
| **Transfer Date** | September 29, 2026 |
| **Source Commit SHA** | `3c0639ca96ba19494bb2e82ca1f72ab9a7834ade` |
| **Destination Commit BEFORE Transfer** | `e5c90ad5e31317f85d691e731d146556e278d03e` |
| **Destination Branch** | `feature/milestone-1-full-implementation` |
| **Transfer Classification Scheme** | A: TRANSFER_AS_HISTORICAL_EVIDENCE, B: TRANSFER_AS_SANITIZED_ARCHIVE, C: EXTRACT_INFORMATION_ONLY, D: DO_NOT_TRANSFER, E: DUPLICATE_OF_CURRENT_PROTEINSOLVER_SOURCE, F: RESEARCH_REPOSITORY_ONLY |

---

## 2. Inventory of Transferred Files

| Destination Path | Source Path | Classification | Copy Type | Source SHA-256 | Destination SHA-256 | Transformations Applied | Current Authoritative Replacement |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `reports/archive/proteindesign_e0/PHASE1_PROTEINSOLVER_REPRODUCTION.md` | `reports/PHASE1_PROTEINSOLVER_REPRODUCTION.md` | B | Sanitized Archive | `420D7A83FCFE50774F1D0B50EFCEFB9BC092F8149E5229E3320463371B293087` | `1D5505AC712D46FA6875B882A76DF3AD62161B32A072FBE7CF3D2A936BD1E016` | Prepended Phase 6 non-authoritative header + archival note; normalized manifest link to relative link | `reports/MILESTONE_1_FINAL_REPORT.md`, `docs/IMPLEMENTATION_STATUS.md` |
| `reports/archive/proteindesign_e0/PROTEINSOLVER_PROVENANCE_MANIFEST.md` | `reports/PROTEINSOLVER_PROVENANCE_MANIFEST.md` | B | Sanitized Archive | `FC225CDBF87DC81D9AD5C71F25EB2A4F4A9ECE79D59B823423754B9CCF0BA179` | `DDC1262AF20E355CE2A63EA8308F005F85C3381ED70C0B903153E350B997B9E6` | Prepended Phase 6 non-authoritative header + archival note | `docs/UPSTREAM_PROVENANCE.md`, `docs/COMPATIBILITY.md` |
| `reports/archive/proteindesign_e0/PAPER_VS_IMPLEMENTATION_AUDIT.md` | `reports/paper_vs_implementation.md` | B | Sanitized Archive | `E94BE01F9EA4D28D28CCA1005A6F0EB1BAF88527163116906F5CF9BE0DA12E58` | `8610AAF96E57450A8879532D61716846196E4E7F502766AE6E2053AA4D73C095` | Prepended Phase 6 non-authoritative header + archival note | `docs/ORIGINAL_PROJECT_PARITY.md`, `docs/KNOWN_LIMITATIONS.md` |
| `reports/archive/proteindesign_e0/test_original_execution.py` | `test_original_execution.py` | A | Historical Evidence | `B83524F94EDE4BC8AD6EE32419233941B6508F182CA452EDAA80A02C873B22D4` | `8CFC150527BDEFBD1F698452FDC91775A30543079A27B3497DAB4677AC6E05E3` | Prepended Phase 6 non-authoritative python docstring header + archival note | `tests/test_all_masked_design.py`, `tests/test_leak_regression.py`, `tests/test_model_checkpoint.py`, `tests/test_integration_1n5u.py` |
| `reports/archive/proteindesign_e0/EXP000_PROTEINSOLVER_SMOKETEST/config.json` | `experiments/EXP000_PROTEINSOLVER_SMOKETEST/config.json` | A | Exact Copy | `B39D3BE51DAA507BBD12C67A39BB3EF7A83C2A6B7E7597E916D9C66CC41A8505` | `AA82659F6FCD8C065F56991A464CDFE6867AF0F772D4C17AC41A27B194FFAB8C` | Cleaned trailing newline | `tests/test_model_checkpoint.py` |
| `reports/archive/proteindesign_e0/EXP000_PROTEINSOLVER_SMOKETEST/environment.txt` | `experiments/EXP000_PROTEINSOLVER_SMOKETEST/environment.txt` | A | Exact Copy | `A5C71DA0571508E90061B0043C95BF5D69E3FE3D5942504B5C13511B9211E2C9` | `5857E40043B7016EDA165BAFA9B7A9CE2EB9F34616C4D927FB161CD1D1612E6A` | Cleaned trailing newline | `docs/COMPATIBILITY.md` |
| `reports/archive/proteindesign_e0/EXP000_PROTEINSOLVER_SMOKETEST/metrics.json` | `experiments/EXP000_PROTEINSOLVER_SMOKETEST/metrics.json` | A | Exact Copy | `AFD9B1FDF9777DA346B6FC3157BFE99408AF8BEB96BD4ABEBC7C3A3ACDB44198` | `37348E4E03A187EDED1E196F6CF789BF890220373B7D55DC74DE48555311E66F` | Cleaned trailing newline | `tests/test_model_checkpoint.py` |
| `reports/archive/proteindesign_e0/EXP000_PROTEINSOLVER_SMOKETEST/run_log.txt` | `experiments/EXP000_PROTEINSOLVER_SMOKETEST/run_log.txt` | A | Exact Copy | `337DFC8FAF101009CB994EA8D3CEA2E07583153282FB6BDB4841E98BA9F3CD32` | `E6BD664517AB13B8AEF97445CB628B6F8CD3B6584D19546F0CACF0E66B7304D4` | Cleaned trailing newline | `tests/test_compat_shims.py` |
| `reports/archive/proteindesign_e0/EXP000_PROTEINSOLVER_SMOKETEST/run_smoketest.py` | `experiments/EXP000_PROTEINSOLVER_SMOKETEST/run_smoketest.py` | A | Exact Copy | `1A3BE5CDDDED2E56FBF2796BFDE9350E6D910C44FAF6682BB75F3DAFC03AEF13` | `E4A558BBAC9071AE087C09CD35E5AA96B1C515F4A8E6DC6899E53664E6BF2728` | Cleaned trailing newline | `tests/test_model_checkpoint.py` |
| `reports/archive/proteindesign_e0/EXP000_PROTEINSOLVER_SMOKETEST/README.md` | *(Generated)* | A | Created Record | N/A | `E593DC7E1B53C07E76A9AACC0055ECC0369A9C3B0A882BE46FF227B4C2F7B3F1` | Explanatory archive README documenting experiment scope, fixture deduplication, and non-authoritative status | `tests/test_model_checkpoint.py` |
| `reports/archive/proteindesign_e0/EXP001_PROTEINSOLVER_INFERENCE/config.json` | `experiments/EXP001_PROTEINSOLVER_INFERENCE/config.json` | A | Exact Copy | `642AC8D562CCA9807E459DE0CC65785A5528A33E86A278777D4D8E57691C9242` | `C5F8B2A7961459AF734CE9340078A4C511DC478855010A373E6F6AF1ECC80E53` | Cleaned trailing newline | `tests/test_integration_1n5u.py` |
| `reports/archive/proteindesign_e0/EXP001_PROTEINSOLVER_INFERENCE/metrics.json` | `experiments/EXP001_PROTEINSOLVER_INFERENCE/metrics.json` | A | Exact Copy | `C256ACB52714A9586D6D309F251B999570111249CDCDD1ACAD5FF18431C5EE18` | `2AC9EDD8D89C6C2DF5CD0597807384A72B64D2305D5861E9A13F259B09ABFF57` | Cleaned trailing newline | `tests/test_integration_1n5u.py` |
| `reports/archive/proteindesign_e0/EXP001_PROTEINSOLVER_INFERENCE/run_inference.py` | `experiments/EXP001_PROTEINSOLVER_INFERENCE/run_inference.py` | A | Exact Copy | `B497E11479B702E5383598B447B9972768C3117F98966BC4353A47CEAF5EC6AA` | `2E121E9AEB7B1249F8EDA77201FD4F610AEAE9C414C66C7B6CFBE49D3E890B65` | Cleaned trailing newline | `tests/test_integration_1n5u.py` |
| `reports/archive/proteindesign_e0/EXP001_PROTEINSOLVER_INFERENCE/run_log.txt` | `experiments/EXP001_PROTEINSOLVER_INFERENCE/run_log.txt` | B | Sanitized Archive | `D9C9DCD7C0EAACDEAC77D7D666CD6BA373A97BB2C3E296F4C36DC4E8242FF324` | `2F5A43D680FD3EFD9136D1BCD30D4E9056BA72A521361E2A5832D8BC512D5ADF` | Normalized 2 machine-specific absolute path lines to repo-relative paths | `tests/test_integration_1n5u.py` |
| `reports/archive/proteindesign_e0/EXP001_PROTEINSOLVER_INFERENCE/output/designed_sequences.csv` | `experiments/EXP001_PROTEINSOLVER_INFERENCE/output/designed_sequences.csv` | A | Exact Copy | `3B7BB676D7EAF69DF7F3065F7A9864670472D6734125B42E74C531A5333C5A6F` | `7E1D22E3B949B4EE47C5A454E297C980861565125B8AFD8585EB75319F85600D` | Cleaned trailing newline | `tests/test_integration_1n5u.py` |
| `reports/archive/proteindesign_e0/EXP001_PROTEINSOLVER_INFERENCE/output/inference_summary.csv` | `experiments/EXP001_PROTEINSOLVER_INFERENCE/output/inference_summary.csv` | A | Exact Copy | `E70173738CD294363700FC07AB1523203C862F5AF0371A5DCFB9AB89F4DEBB6C` | `52C721F4D97DA21B543B01EE05CC77FDF28675ABEB6CC9D5DFBE3265DBBB2274` | Cleaned trailing newline | `tests/test_integration_1n5u.py` |
| `reports/archive/proteindesign_e0/EXP001_PROTEINSOLVER_INFERENCE/output/reproducibility_check.json` | `experiments/EXP001_PROTEINSOLVER_INFERENCE/output/reproducibility_check.json` | A | Exact Copy | `8D9538FACEB0CB4C78BBE502949BB0A38828BBF2D937C01D987C5EC654D60A14` | `A20C445CFDEAB8F859D003E39178F5B11D7E3CB6FF805FC85DB7BD6649BCFAC0` | Cleaned trailing newline | `tests/test_integration_1n5u.py` |
| `reports/archive/proteindesign_e0/EXP001_PROTEINSOLVER_INFERENCE/README.md` | *(Generated)* | A | Created Record | N/A | `B0380BC5C2F095B2C1FF5E576FE03701461FF7BA3E70733981D12CAD4E6F8E2B` | Explanatory archive README documenting experiment scope, fixture deduplication, data policy, and non-authoritative status | `tests/test_integration_1n5u.py` |
| `reports/archive/proteindesign_e0/EXP004_MASK_INVARIANCE/config.json` | `experiments/EXP004_MASK_INVARIANCE/config.json` | A | Exact Copy | `B44947F613342F43EC9B8297F44D855B719D203A372B5F2873AC17EB72F4703B` | `52039DBE46E6B4356D8D90282C9E2DD621EFFBBD09895D90B9D280A50C59DC50` | Cleaned trailing newline | `tests/test_leak_regression.py` |
| `reports/archive/proteindesign_e0/EXP004_MASK_INVARIANCE/metrics.json` | `experiments/EXP004_MASK_INVARIANCE/metrics.json` | A | Exact Copy | `BE8EB0F11FFBF7EC9D1B4B9D445AD119B0742C5E8214C3F2237BF64D484AC567` | `B8A154931FA60D642F1D2D09896036F637057D21022B177B1F6AAF8ED788E1A2` | Cleaned trailing newline | `tests/test_leak_regression.py` |
| `reports/archive/proteindesign_e0/EXP004_MASK_INVARIANCE/README.md` | *(Generated)* | A | Created Record | N/A | `207AD83DF9039CC5A4A05C37FA3CF02811438E71C8AC96BD3600A67C7E78FD09` | Explanatory archive README documenting experiment scope, fixture deduplication, and non-authoritative status | `tests/test_leak_regression.py` |
| `reports/archive/proteindesign_e0/EXP004_MASK_INVARIANCE/run_log.txt` | `experiments/EXP004_MASK_INVARIANCE/run_log.txt` | A | Exact Copy | `8A3689B0F61F1D3C5727536283B0FB228476E3D414FB7514D0FA1174BB36ECF1` | `C54915FDD2D67B4DB898140AFF2783849A6137CB4B9B2AD76B839CF01BB2D9A8` | Cleaned trailing newline | `tests/test_leak_regression.py` |
| `reports/archive/proteindesign_e0/EXP004_MASK_INVARIANCE/run_mask_invariance.py` | `experiments/EXP004_MASK_INVARIANCE/run_mask_invariance.py` | A | Exact Copy | `CB5779EE6CC15A72509656E756E3A20C88DA061F5CA120DFA157A1CE866D5501` | `3CF3F81F82904390EEC38065B850CB06457F29664FA35221525F20360A5C7027` | Cleaned trailing newline | `tests/test_leak_regression.py` |

---

## 3. Files Explicitly NOT Transferred & Justification

| Source Path / Pattern | Classification | Justification |
| :--- | :--- | :--- |
| `external/proteinsolver-original/` | E | Duplicate of upstream source: ProteinSolver is a direct GitHub fork of `ostrokach/proteinsolver` preserving 100% upstream git history at acquisition commit `69ef0965a3fc3bf191804035b539720a06e58ba6`. Duplicating as a subfolder would violate repository boundaries. |
| `environment/proteinsolver-original/` | D | Virtual environment containing local binaries, machine paths, site-packages, and caches. ProteinSolver specifies its own dependencies via `pyproject.toml` and verified clean-clone virtual environments. |
| `src/proteinsolver_baseline/` | D | Superseded cleanroom prototype from early ProteinDesign research. Does not match ProteinSolver's production architecture (`proteinsolver/`, `compat/`, `apps/`). Current `compat/` is authoritative. |
| `research/paper_vs_implementation.md` | D | Superseded duplicate draft in ProteinDesign. The authoritative ProteinDesign report was `reports/paper_vs_implementation.md`, which is transferred as `PAPER_VS_IMPLEMENTATION_AUDIT.md`. |
| `experiments/EXP000_PROTEINSOLVER_SMOKETEST/input/1n5uA03.pdb` | E | Byte-identical duplicate of canonical fixture `data/1n5uA03.pdb` (SHA-256: `19D1FCAA81C209B96C0B0559BC1C775EF393744094CCF2FB928FFEC528B65416`). Omitted to prevent redundancy. |
| `experiments/EXP001_PROTEINSOLVER_INFERENCE/input/1n5uA03.pdb` | E | Byte-identical duplicate of canonical fixture `data/1n5uA03.pdb` (SHA-256: `19D1FCAA81C209B96C0B0559BC1C775EF393744094CCF2FB928FFEC528B65416`). Omitted to prevent redundancy. |
| `experiments/EXP001_PROTEINSOLVER_INFERENCE/input/1UBQ.pdb` | D | External structure fixture (SHA-256: `D4A6812D8951CF6594E6A0763F089E35F5A80B62ACB3C117B2C5565228A7B161`). All design sequences and reproducibility metrics generated from it are fully preserved in `output/` and `metrics.json`. Omitted from persistent repo archive to keep archive purely metadata/scripts/metrics. |
| `data/e53-s1952148-d93703104.state` | E | Model checkpoint already tracked at `data/e53-s1952148-d93703104.state` (SHA-256: `1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727`). |
| `CLAIMS_REGISTRY.md` | F | ProteinDesign research project governance and claims registry; belongs strictly to research repository. |
| `PROJECT_STATE.md` | F | ProteinDesign research project state tracking; belongs strictly to research repository. |
| `DECISION_LOG.md` | F | ProteinDesign research architecture decisions; ProteinSolver maintains its own `AGENT_RULES_AND_LESSONS.md`. |
| `RESEARCH_PROTOCOL.md` | F | Research laboratory protocol governing scientific investigation in ProteinDesign. |
| `reports/FOUNDATION_HANDOFF_REPORT.md` | F | Research foundation handoff report for ProteinDesign research team. |
| `science/*` | F | ProteinDesign downstream scientific workflows, evaluation suites, and design scripts. |
| `architecture/*` | F | ProteinDesign architecture specifications. |
| `docs/PROJECT_TRUTH.md` | F | ProteinDesign research governance documentation. |
| `docs/TEAM_WORKSTREAMS.md` | F | ProteinDesign team workstream tracking. |
| `docs/TEAM_ONBOARDING.md` | F | ProteinDesign onboarding documentation. |

---

## 4. Canonical Fixture & Checkpoint Verification

| Item | Expected SHA-256 | Actual Measured SHA-256 in ProteinSolver | Match Status |
| :--- | :--- | :--- | :---: |
| Canonical Fixture `data/1n5uA03.pdb` | `19D1FCAA81C209B96C0B0559BC1C775EF393744094CCF2FB928FFEC528B65416` | `19D1FCAA81C209B96C0B0559BC1C775EF393744094CCF2FB928FFEC528B65416` | **VERIFIED MATCH** |
| Pretrained Checkpoint `data/e53-s1952148-d93703104.state` | `1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727` | `1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727` | **VERIFIED MATCH** |

---

## 5. Scientific Facts Preserved in the Historical Archive

1. **Upstream Commit Provenance:** Upstream acquisition commit `69ef0965a3fc3bf191804035b539720a06e58ba6` from `https://github.com/ostrokach/proteinsolver.git`.
2. **Model Parameter Count & Architecture:** Total 567,060 trainable parameters across 4 EdgeConv residual blocks with hidden dimension 128 (reconciling obsolete mentions of 162, which belongs to attention tests).
3. **State Dict Key Adapter:** Checkpoint keys (`graph_conv_0.` $\to$ `graph_conv_1.`, `graph_conv.0..2.` $\to$ `graph_conv_2..4.`) load under `strict=True` with 0 missing and 0 unexpected keys.
4. **Valid All-Masked Design Protocol:** Input invariant requires `data.x = 20` (all-masked) and `data.y = None` (no reference sequence).
5. **Native Sequence Leak Mechanism:** Attaching reference sequences to `data.y` causes lines 148-176 of `protein_design.py` to copy `x_ref` site-by-site under `strategy="ref"`, producing false "100% recovery".
6. **Mask-Invariance Proof (EXP004):** Logit difference between different hidden sequences on all-masked input is exactly `0.00000000e+00`.
7. **Single-Target Result (EXP001):** Valid all-masked CSP design on `1n5uA03` yields 41.30% recovery (38/92 matches) in ~1.5-1.8s. Correctly classified as a single-target integration check, not a cross-fold benchmark.
8. **Target Contamination Assessment:** Training set membership of `1n5uA03` is formally classified as "not verifiable from accessible metadata" without downloading multi-GB cluster training sets.
9. **Compatibility Adaptations:** Historical dependencies (`kmbio`, UNIX `fcntl`, PyG 1.3 `scatter_`, unbatched graph assumptions, cross-device CUDA indexing) systematically documented and superseded by `compat/`.
