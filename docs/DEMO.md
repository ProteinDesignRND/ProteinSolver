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
- Set **Strategy: Argmax (MAP)** for deterministic greedy generation, or **Multinomial (T=0.1, Seed=42)** for stochastic sampling.

### Step 4: Execute Generation
- Click **Run ProteinSolver Design**.
- Observe the real-time execution timer. In ~1.7 seconds, the backend completes the GNN message-passing and iterative CSP sequence generation.

### Step 5: Review Results
- The **Generated Sequence** appears with total length (92 AA) and mean site confidence.
- Inspect the **Per-Residue Confidence** tiles: green residues indicate high model certainty, amber indicates moderate certainty.
- Click **Export FASTA** to download the designed sequence.

### Step 6: Diagnostic Verification (Optional)
- Switch mode to **Diagnostic Evaluation**.
- Click **Run Diagnostic Evaluation**.
- Explain to the mentor that on target 1n5uA03, valid all-masked MAP recovery reproduces **41.30% native sequence identity** in ~1.5 seconds. Emphasize that this is a single-target integration check on a single structure, not a general benchmark claim.
