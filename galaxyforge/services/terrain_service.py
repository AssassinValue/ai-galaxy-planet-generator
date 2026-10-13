"""Terrain service — erosion, biome classification, preview rendering."""

from __future__ import annotations

import io

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

from galaxyforge.utils.noise import ridged_multifractal


class TerrainService:
    def erode(self, height: np.ndarray, passes: int = 24) -> np.ndarray:
        """Cheap hydraulic-ish erosion: repeated blurred slope subtraction.

        Not physically accurate — tuned for visual plausibility at
        ~200 ms for 2048^2 on a Ryzen 7 5800X.
        """
        h = height.astype(np.float32, copy=True)
        for _ in range(passes):
            blurred = gaussian_filter(h, sigma=1.2)
            slope = h - blurred
            h -= 0.06 * slope
        return np.clip(h, 0.0, 1.0)

    def classify_biome(self, height: np.ndarray, water_level: float) -> np.ndarray:
        """Return an int8 biome map: 0=deep water, 1=shallow, 2=lowland,
        3=highland, 4=mountain, 5=peak."""
        b = np.zeros_like(height, dtype=np.int8)
        b[height >= water_level * 0.5] = 1
        b[height >= water_level] = 2
        b[height >= water_level + 0.15] = 3
        b[height >= water_level + 0.30] = 4
        b[height >= water_level + 0.45] = 5
        return b

    def ai_refine(self, height: np.ndarray, device: str) -> np.ndarray:
        """Placeholder hook for the torch refinement pass.

        Real inference lives in galaxyforge.models.kernels.refine. This
        keeps the service importable without torch loaded.
        """
        try:
            from galaxyforge.models.kernels.refine import refine_heightmap
        except ImportError:
            return height
        return refine_heightmap(height, device=device)

    def render_preview(
        self,
        height: np.ndarray,
        biome: np.ndarray,
        preset: object,
    ) -> bytes:
        base = np.asarray(getattr(preset, "base_color"), dtype=np.float32)
        rgb = np.zeros((*height.shape, 3), dtype=np.float32)
        rgb[...] = base
        rgb[biome == 0] = base * 0.35
        rgb[biome == 1] = base * 0.6
        rgb[biome >= 4] = np.clip(base + 0.25, 0, 1)
        rgb = (rgb * 255).astype(np.uint8)

        buf = io.BytesIO()
        Image.fromarray(rgb, mode="RGB").save(buf, format="PNG", optimize=True)
        return buf.getvalue()