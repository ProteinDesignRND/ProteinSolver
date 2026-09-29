# Mentor Demonstration Guide

**Document:** `docs/DEMO.md`  
**Repository:** `ProteinDesignRND/ProteinSolver`  

---

## 1. Objective of Demonstration
Showcase the modern, functionally verified ProteinSolver application suite on a modern development stack:
1. Validating input PDB structure.
2. Generating a novel protein sequence using all-masked graph neural network inverse folding.
3. Inspecting per-residue confidence scores.
4. Explaining the historical provenance, architecture, and compatibility innovations.

---

## 2. Step-by-Step Demonstration Script

### Step 1: Launch the Application
- Open browser to `http://localhost:5173`.
- Verify the header badge indicates: `Backend Connected | Checkpoint Loaded | 567,060 Parameters`.

### Step 2: Select a Target Structure
- In the **Structure Input** section, click **Load Example: 1n5uA03 (CATH domain, 92 AA)**.
- Observe that chain `A` is automatically selected and the structure validates (92 residues, standard amino acids).

### Step 3: Configure Design Parameters
- Select **Design Mode: Inverse Folding (All-Masked)**.
- Emphasize to the mentor that inverse folding generates a sequence from the structure with purely all-masked input ($data.x = 20, data.y = None$); the native sequence is not visible to the design network.
- Set **Strategy: Argmax (MAP)** for deterministic greedy generation, or **Multinomial (T=0.1, Seed=42)** for stochastic sampling.

### Step 4: Execute Generation
- Click **Run ProteinSolver Design**.
- Observe the real-time execution timer. Execution is typically around 1.5–2.1 seconds on the verified CPU environment (exact runtime is run-dependent), during which the backend completes the GNN message-passing and iterative CSP sequence generation.

### Step 5: Review Results
- The **Generated Sequence** appears with total length (92 AA) and mean site confidence.
- Inspect the **Per-Residue Confidence** tiles: green residues indicate high model selection probability ($\ge 70\%$), amber indicates moderate probability ($40-69\%$), and rose indicates lower probability ($< 40\%$). Note that these are display-only visualization bands representing raw model selection probabilities, not calibrated biological probabilities.
- Click **Export FASTA** to download the designed sequence.

### Step 6: Diagnostic Verification (Optional)
- Switch mode to **Diagnostic Evaluation**.
- Click **Run Diagnostic Evaluation**.
- Explain that the diagnostic endpoint retrospectively compares the generated sequence against the native sequence (which was strictly withheld from the design network).
- Explain to the mentor that on target 1n5uA03, valid all-masked MAP recovery reproduces **41.30% native sequence identity** (38/92 residues, typically around 1.5–2.1 seconds on the verified CPU environment; exact runtime is run-dependent). Emphasize that this is a previously validated single-target all-masked integration result on a single structure, not a general benchmark claim, and training-set membership of 1n5uA03 is not independently verifiable from accessible metadata.
