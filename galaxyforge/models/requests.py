"""Request schemas — validated at the boundary."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PlanetRequest(BaseModel):
    seed: int = Field(ge=0, le=2**31 - 1)
    preset: str = "terran"
    resolution: int = Field(default=2048, ge=256, le=8192)
    ai_refine: bool = False


class GalaxyRequest(BaseModel):
    seed: int = Field(ge=0, le=2**31 - 1)
    arms: int = Field(default=4, ge=2, le=8)
    star_count: int = Field(default=8000, ge=100, le=200_000)