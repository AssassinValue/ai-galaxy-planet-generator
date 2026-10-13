"""Result schemas — every service returns one of these."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from pydantic import BaseModel, ConfigDict, Field


class _ResultBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    filename: str


class PlanetResult(_ResultBase):
    seed: int
    preset: str
    resolution: int
    heightmap: np.ndarray = Field(repr=False)
    biome: np.ndarray = Field(repr=False)
    preview_png: bytes = Field(repr=False)

    def write(self, out_dir: Path) -> Path:
        out_dir.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            out_dir / self.filename,
            heightmap=self.heightmap,
            biome=self.biome,
            meta={"seed": self.seed, "preset": self.preset},
        )
        (out_dir / f"{self.filename}.preview.png").write_bytes(self.preview_png)
        return out_dir / self.filename


class GalaxyResult(_ResultBase):
    seed: int
    arms: int
    star_count: int
    positions: np.ndarray = Field(repr=False)

    def write(self, out_dir: Path) -> Path:
        out_dir.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(out_dir / self.filename, positions=self.positions)
        return out_dir / self.filename