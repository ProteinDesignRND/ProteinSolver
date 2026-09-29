"""
Published checkpoint loading with state-dict key translation.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import torch

from compat.shims import apply_shims
apply_shims()

from proteinsolver.models.proteinnet import ProteinNet

EXPECTED_SHA256 = "1E8272F05EC19041394568C949BBDBF012EE72C1595BE7157C4BB0324D0B5727"
EXPECTED_PARAMS = 567060

# Translation mapping from training run names to packaged ProteinNet names
KEY_MAPPING = {
    "graph_conv_0.": "graph_conv_1.",
    "graph_conv.0.": "graph_conv_2.",
    "graph_conv.1.": "graph_conv_3.",
    "graph_conv.2.": "graph_conv_4.",
}


def translate_state_dict_keys(raw_state_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Map training-time state_dict keys to packaged ProteinNet layer attributes."""
    mapped = {}
    for k, v in raw_state_dict.items():
        new_k = k
        for src, dst in KEY_MAPPING.items():
            if k.startswith(src):
                new_k = k.replace(src, dst, 1)
                break
        mapped[new_k] = v
    return mapped


def load_proteinsolver_model(
    checkpoint_path: Optional[str] = None,
    device: str = "cpu"
) -> ProteinNet:
    """
    Instantiate ProteinNet, load mapped published weights, validate shapes, and set eval mode.
    """
    if checkpoint_path is None:
        default_path = Path(__file__).resolve().parent.parent / "data" / "e53-s1952148-d93703104.state"
        checkpoint_path = str(default_path)

    net = ProteinNet(x_input_size=21, adj_input_size=2, hidden_size=128, output_size=20)
    
    raw_state_dict = torch.load(checkpoint_path, map_location=device, weights_only=True)
    mapped_state_dict = translate_state_dict_keys(raw_state_dict)

    load_result = net.load_state_dict(mapped_state_dict, strict=True)
    assert len(load_result.missing_keys) == 0, f"Missing keys: {load_result.missing_keys}"
    assert len(load_result.unexpected_keys) == 0, f"Unexpected keys: {load_result.unexpected_keys}"

    net = net.to(device)
    net.eval()
    return net
