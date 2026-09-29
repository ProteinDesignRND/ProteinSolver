# Known Limitations & Technical Boundaries

**Document:** `docs/KNOWN_LIMITATIONS.md`  
**Repository:** `ProteinDesignRND/ProteinSolver`  

---

## 1. Single-Target vs General Benchmark Boundary
- On target 1n5uA03, valid all-masked inverse folding achieves 41.30% native sequence recovery.
- **Boundary:** This recovery metric is a single-target runtime and mathematical integration check. It is **NOT** a generalization benchmark across diverse protein folds.

## 2. Historical Training Set Membership
- Historical ProteinSolver training Parquet corpora (72 million structures) were hosted on external HPC clusters and are not included in Git metadata.
- Therefore, training set membership for specific benchmark targets cannot be verified from accessible metadata. Targets are classified as `NOT VERIFIABLE FROM ACCESSIBLE METADATA`.

## 3. Iterative CSP Execution Device
- Iterative CSP design (`design_sequence()`) is executed on CPU because modern PyTorch 2.6 restricts cross-device tensor indexing on CUDA.
- **Impact:** CPU inference takes ~1.7 seconds for 92 AA, which is fast enough for interactive web use without requiring invasive modifications to historical source code.

## 4. Upstream Rosetta / Modeller Utilities
- `proteinsolver.utils.model_scoring` contains legacy wrappers for Rosetta and Modeller, which require external commercial/proprietary licenses and installations not provided in this repository.
