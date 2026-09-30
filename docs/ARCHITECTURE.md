# System Architecture Specification

## 1. Overview
ProteinSolver Milestone 1 is a layered inverse protein design suite executing on modern Python 3.11, PyTorch 2.6, and PyG 2.8.

## 2. Model Architecture Facts
- **Architecture Name:** `ProteinNet`
- **Class Implementation:** `proteinsolver.models.proteinnet.ProteinNet`
- **GNN Structure:** 4 sequential `EdgeConv` residual blocks
- **Node Input Dimensionality:** 21 (20 standard amino acids + 1 mask token `20`)
- **Edge Input Dimensionality:** 2 (minimum heavy-atom distance in Å + sequence separation probability)
- **Hidden Embedding Dimensionality:** **128** (empirically validated from weight tensors; NOT 162)
- **Output Dimensionality:** 20 (logits over standard amino acids)
- **Total Validated Parameters:** Exactly **567,060**
- **Checkpoint Checksum:** SHA-256 `1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727`

## 3. Communication Protocol
- **Transport Format:** JSON payload (`Content-Type: application/json`).
- Structure text is transmitted as raw PDB string within `{"pdb_content": "..."}`.
- Multipart form encoding is not used.
