"""Fractal noise helpers. All functions take an explicit rng."""

from __future__ import annotations

import numpy as np


def fbm_heightmap(
    resolution: int,
    octaves: int,
    lacunarity: float,
    gain: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Fractional Brownian motion heightmap in [0, 1]."""
    height = np.zeros((resolution, resolution), dtype=np.float32)
    amplitude = 1.0
    total = 0.0
    for o in range(octaves):
        freq = resolution >> (octaves - o - 1)
        grid = rng.random((max(freq, 2), max(freq, 2))).astype(np.float32)
        height += amplitude * _upsample(grid, resolution)
        total += amplitude
        amplitude *= gain
        _ = lacunarity  # reserved for anisotropic octaves
    height /= max(total, 1e-6)
    return np.clip(height, 0.0, 1.0)


def ridged_multifractal(
    resolution: int,
    octaves: int,
    rng: np.random.Generator,
) -> np.ndarray:
    base = fbm_heightmap(resolution, octaves, 2.0, 0.5, rng)
    return 1.0 - np.abs(2.0 * base - 1.0)


def _upsample(grid: np.ndarray, target: int) -> np.ndarray:
    from scipy.ndimage import zoom

    factor = target / grid.shape[0]
    return zoom(grid, factor, order=1)[:target, :target]