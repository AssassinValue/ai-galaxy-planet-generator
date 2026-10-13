"""Torch refinement kernel — smooths and enhances heightmaps.

Loads weights with `weights_only=True`. Do not change that flag.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

_WEIGHTS = Path(__file__).with_name("refine_v1.pt")


class RefineNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.GELU(),
            nn.Conv2d(16, 16, 3, padding=1), nn.GELU(),
            nn.Conv2d(16, 1, 3, padding=1), nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


_CACHE: dict[str, RefineNet] = {}


def _load(device: str) -> RefineNet:
    if device in _CACHE:
        return _CACHE[device]
    model = RefineNet().to(device).eval()
    if _WEIGHTS.is_file():
        state = torch.load(_WEIGHTS, map_location=device, weights_only=True)
        model.load_state_dict(state)
    _CACHE[device] = model
    return model


@torch.inference_mode()
def refine_heightmap(height: np.ndarray, device: str = "cpu") -> np.ndarray:
    model = _load(device)
    t = torch.from_numpy(height[None, None].astype(np.float32)).to(device)
    out = model(t).squeeze().cpu().numpy()
    return np.clip(out, 0.0, 1.0)