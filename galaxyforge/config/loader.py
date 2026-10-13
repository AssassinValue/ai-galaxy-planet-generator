"""YAML config loader with pydantic validation."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field, ValidationError


class RuntimeConfig(BaseModel):
    device: str = "auto"
    threads: int = 0
    deterministic: bool = True


class GenerationConfig(BaseModel):
    default_resolution: int = 2048
    heightmap_octaves: int = 7
    heightmap_lacunarity: float = 2.05
    heightmap_gain: float = 0.5
    erosion_passes: int = 24


class GalaxyConfig(BaseModel):
    default_arms: int = 4
    default_star_count: int = 8000
    arm_tightness: float = 6.2
    bulge_ratio: float = 0.18


class Preset(BaseModel):
    base_color: tuple[float, float, float]
    water_level: float = Field(ge=0.0, le=1.0)
    atmosphere_density: float = Field(ge=0.0, le=2.0)
    cloud_coverage: float = Field(ge=0.0, le=1.0)


class AppConfig(BaseModel):
    runtime: RuntimeConfig = RuntimeConfig()
    generation: GenerationConfig = GenerationConfig()
    galaxy: GalaxyConfig = GalaxyConfig()
    presets: dict[str, Preset] = {}


class ConfigError(RuntimeError):
    """Raised when the YAML is malformed or fails schema validation."""


def load_config(path: Path) -> AppConfig:
    if not path.is_file():
        raise ConfigError(f"config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    try:
        return AppConfig.model_validate(raw)
    except ValidationError as exc:
        raise ConfigError(f"invalid config at {path}: {exc}") from exc