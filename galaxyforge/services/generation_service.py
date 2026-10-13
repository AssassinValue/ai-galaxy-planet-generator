"""Planet generation service.

Orchestrates: preset lookup -> heightmap -> erosion -> biome shading ->
optional AI refinement pass -> packed .gfp result.

Inputs: PlanetRequest (seed, preset, resolution, ai_refine).
Outputs: PlanetResult (heightmap ndarray, biome map, preview PNG bytes).
Side effects: none on disk — callers write via PlanetResult.write().
Concurrency: service is stateless; safe to call from multiple threads
  as long as the underlying torch model is not shared. Use one service
  per worker thread when ai_refine=True.
"""

from __future__ import annotations

import logging

import numpy as np

from galaxyforge.models.requests import PlanetRequest
from galaxyforge.models.results import PlanetResult
from galaxyforge.services.terrain_service import TerrainService
from galaxyforge.utils.noise import fbm_heightmap
from galaxyforge.utils.rng import seeded_numpy

log = logging.getLogger(__name__)


class GenerationService:
    def __init__(
        self,
        device: str,
        presets: dict[str, object],
        terrain: TerrainService | None = None,
    ) -> None:
        self._device = device
        self._presets = presets
        self._terrain = terrain or TerrainService()

    def generate_planet(self, request: PlanetRequest) -> PlanetResult:
        preset = self._presets.get(request.preset)
        if preset is None:
            raise KeyError(f"unknown preset: {request.preset!r}")

        rng = seeded_numpy(request.seed)
        height = fbm_heightmap(
            resolution=request.resolution,
            octaves=7,
            lacunarity=2.05,
            gain=0.5,
            rng=rng,
        )
        eroded = self._terrain.erode(height, passes=24)
        biome = self._terrain.classify_biome(eroded, water_level=preset.water_level)

        if request.ai_refine:
            log.info("ai_refine enabled — hooking model backend (seed=%d)", request.seed)
            eroded = self._terrain.ai_refine(eroded, device=self._device)

        preview = self._terrain.render_preview(eroded, biome, preset)
        return PlanetResult(
            seed=request.seed,
            preset=request.preset,
            resolution=request.resolution,
            heightmap=eroded,
            biome=biome,
            preview_png=preview,
            filename=f"planet_{request.preset}_{request.seed}.gfp",
        )