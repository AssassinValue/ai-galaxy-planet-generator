"""Galaxy generation service.

Builds a spiral-arm star field from a seed. Deterministic: same
(seed, arms, star_count) always yields the same placement.
"""

from __future__ import annotations

import numpy as np

from galaxyforge.models.requests import GalaxyRequest
from galaxyforge.models.results import GalaxyResult
from galaxyforge.utils.rng import seeded_numpy


class GalaxyService:
    ARM_TIGHTNESS = 6.2
    BULGE_RATIO = 0.18

    def generate(self, request: GalaxyRequest) -> GalaxyResult:
        rng = seeded_numpy(request.seed)
        n = request.star_count
        bulge_n = int(n * self.BULGE_RATIO)
        disk_n = n - bulge_n

        # Bulge: gaussian blob at origin.
        bulge = rng.normal(scale=0.12, size=(bulge_n, 3))
        bulge[:, 2] *= 0.4

        # Disk: logarithmic spiral arms with scatter.
        arm_idx = rng.integers(0, request.arms, size=disk_n)
        r = rng.gamma(shape=2.1, scale=0.22, size=disk_n)
        theta = (
            arm_idx * (2 * np.pi / request.arms)
            + self.ARM_TIGHTNESS * np.log(r + 1e-6)
            + rng.normal(scale=0.18, size=disk_n)
        )
        disk = np.stack(
            [r * np.cos(theta), r * np.sin(theta), rng.normal(scale=0.03, size=disk_n)],
            axis=1,
        )

        stars = np.vstack([bulge, disk]).astype(np.float32)
        return GalaxyResult(
            seed=request.seed,
            arms=request.arms,
            star_count=n,
            positions=stars,
            filename=f"galaxy_{request.arms}arm_{request.seed}.gfx",
        )