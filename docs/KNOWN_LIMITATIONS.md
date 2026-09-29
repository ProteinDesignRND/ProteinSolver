# Known Limitations & Scientific Boundaries

1. **Single-Target Integration Check vs. Benchmark:** Target `1n5uA03` (92 AA) is an integration sanity fixture. Its 41.30% recovery (38/92 residues) reproduces the project's previously validated single-target integration result. It is NOT a generalized benchmark or proof of multi-target recovery across protein folds. Systematic benchmarking is reserved exclusively for the research repository (`ProteinDesignRND/ProteinDesign`).
2. **Display-Only Confidence Heatmap:** In the frontend, per-residue confidence color bands (green $\ge 70\%$, amber $40-69\%$, rose $< 40\%$) reflect the raw softmax model selection probability. They are display visualization bands, not calibrated biological probabilities.
3. **CPU Constraint Satisfaction Execution:** Due to cross-device boolean indexing assertions introduced in PyTorch 2.6, iterative CSP design is executed on CPU (`device="cpu"`). CPU runtime is ~1.5s for 92 residues.
4. **External Proprietary Dependencies:** Upstream scoring scripts in `notebooks/16_david_analysis/` require external licensed installations of PyRosetta and Quark.
5. **External Training Shards:** Full training datasets (multi-gigabyte shards) are hosted externally and documented for reference.
