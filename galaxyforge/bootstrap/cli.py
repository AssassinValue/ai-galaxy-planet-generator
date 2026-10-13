"""Headless CLI. `gf-cli planet --seed 6767 --preset terran --out out/`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from galaxyforge.adapters.gpu_probe import probe_device
from galaxyforge.config.loader import load_config
from galaxyforge.models.requests import GalaxyRequest, PlanetRequest
from galaxyforge.services.galaxy_service import GalaxyService
from galaxyforge.services.generation_service import GenerationService


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="gf-cli", description="ai-galaxy-planet-generator")
    sub = p.add_subparsers(dest="cmd", required=True)

    planet = sub.add_parser("planet", help="generate a single planet")
    planet.add_argument("--seed", type=int, required=True)
    planet.add_argument("--preset", default="terran")
    planet.add_argument("--out", type=Path, default=Path("out"))
    planet.add_argument("--resolution", type=int, default=2048)

    galaxy = sub.add_parser("galaxy", help="generate a galaxy")
    galaxy.add_argument("--seed", type=int, required=True)
    galaxy.add_argument("--arms", type=int, default=4)
    galaxy.add_argument("--stars", type=int, default=8000)
    galaxy.add_argument("--out", type=Path, default=Path("out"))

    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    cfg = load_config(Path(__file__).parents[2] / "config" / "default.yaml")

    if args.cmd == "planet":
        svc = GenerationService(device=probe_device(), presets=cfg.presets)
        req = PlanetRequest(seed=args.seed, preset=args.preset, resolution=args.resolution)
        result = svc.generate_planet(req)
        result.write(args.out)
        print(f"wrote {args.out / result.filename}")
        return 0

    if args.cmd == "galaxy":
        svc = GalaxyService()
        req = GalaxyRequest(seed=args.seed, arms=args.arms, star_count=args.stars)
        result = svc.generate(req)
        result.write(args.out)
        print(f"wrote {args.out / result.filename} ({result.star_count} stars)")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))