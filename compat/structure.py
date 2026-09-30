"""
Cleanroom structure parsing and contact graph extraction using BioPython.
Replaces obsolete kmbio/kmtools dependencies with verified modern equivalents.
"""

import io
from typing import List, Tuple, Dict, Any
import numpy as np
import torch
from scipy.spatial.distance import cdist
from Bio.PDB import PDBParser, MMCIFParser, is_aa
from Bio.SeqUtils import seq1

from compat.shims import apply_shims
apply_shims()

from proteinsolver.utils.protein_structure import ProteinData


def get_available_chains(pdb_content_or_path: str) -> List[Dict[str, Any]]:
    """Parse a PDB file or string and return metadata for all standard protein chains."""
    parser = PDBParser(QUIET=True)
    if "\n" in pdb_content_or_path:
        structure = parser.get_structure("target", io.StringIO(pdb_content_or_path))
    else:
        structure = parser.get_structure("target", pdb_content_or_path)

    first_model = next(iter(structure))
    chains_info = []

    for chain in first_model:
        std_residues = [r for r in chain if is_aa(r, standard=True)]
        if std_residues:
            chains_info.append({
                "chain_id": chain.id,
                "residue_count": len(std_residues),
                "first_res_id": std_residues[0].id[1],
                "last_res_id": std_residues[-1].id[1],
            })

    return chains_info


def parse_structure_to_protein_data(
    pdb_content_or_path: str,
    chain_id: str = "A",
    r_cutoff: float = 12.0
) -> Tuple[ProteinData, str]:
    """
    Parse a PDB file/string, extract heavy-atom coordinates, compute contacts (< 12A),
    and construct the exact ProteinData NamedTuple expected by proteinsolver.
    
    Returns:
        (ProteinData, native_sequence)
    """
    parser = PDBParser(QUIET=True)
    if "\n" in pdb_content_or_path:
        structure = parser.get_structure("target", io.StringIO(pdb_content_or_path))
    else:
        structure = parser.get_structure("target", pdb_content_or_path)

    first_model = next(iter(structure))
    
    if chain_id in first_model:
        chain = first_model[chain_id]
    else:
        # Fall back to first available chain
        chain = next(iter(first_model))

    residues = [r for r in chain if is_aa(r, standard=True)]
    if not residues:
        raise ValueError(f"No standard amino acid residues found in chain {chain_id}")

    native_sequence = "".join(seq1(r.get_resname()) for r in residues)
    seq_len = len(residues)

    # Extract non-hydrogen heavy-atom coordinates for each residue
    heavy_coords = [
        np.array([atom.get_coord() for atom in r if atom.element != "H"])
        for r in residues
    ]

    row_indices = []
    col_indices = []
    distances = []

    # Compute minimum heavy-atom distances between residue pairs
    for i in range(seq_len):
        for j in range(i + 1, seq_len):
            d = cdist(heavy_coords[i], heavy_coords[j]).min()
            if d < r_cutoff:
                row_indices.append(i)
                col_indices.append(j)
                distances.append(float(d))

    pdata = ProteinData(
        sequence=native_sequence,
        row_index=torch.tensor(row_indices, dtype=torch.long),
        col_index=torch.tensor(col_indices, dtype=torch.long),
        distances=torch.tensor(distances, dtype=torch.float),
    )

    return pdata, native_sequence
