"""Seeded RNG helpers. Every generator takes a seed — no globals."""

from __future__ import annotations

import numpy as np


def seeded_numpy(seed: int) -> np.random.Generator:
    """Return a numpy Generator seeded deterministically.

    Uses PCG64 explicitly so behavior is stable across numpy versions.
    """
    return np.random.Generator(np.random.PCG64(seed))


def derive_seed(parent: int, *path: int) -> int:
    """Derive a child seed from a parent and a path.

    Same (parent, path) always yields the same child. Used to give
    sub-generators (atmosphere, clouds, moons) their own streams.
    """
    h = parent & 0xFFFFFFFF
    for p in path:
        h = (h * 0x9E3779B1 + (p & 0xFFFFFFFF)) & 0xFFFFFFFF
    return h