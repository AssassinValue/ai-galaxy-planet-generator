# Contributing to ai-galaxy-planet-generator

`ai-galaxy-planet-generator` is a Windows desktop tool for procedurally
synthesizing planets and galaxies with AI-assisted inference. It ships a
PySide6 front-end, a service-oriented core, and a pluggable model backend
(CPU via PyTorch, optional CUDA).

## Repo layout

```
galaxyforge/
  bootstrap/     entry points (desktop app, CLI)
  handlers/      thin request handlers — parse, delegate, return
  services/      business logic (generation, terrain, star systems)
  models/        pydantic schemas + torch modules
  adapters/      platform adapters (Windows paths, GPU probe, file IO)
  ui/            PySide6 views (thin — no business logic)
  config/        YAML presets and runtime config loader
  utils/         math, noise, logging, RNG helpers
tests/
```

## Dev setup

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
ruff check .
mypy galaxyforge
```

## Rules

- Handlers stay thin. Business logic lives in `services/`.
- Every public service returns a pydantic model, never a raw dict.
- New generation kernels go in `models/kernels/` and register in
  `services/generation_service.py`.
- Determinism: every generator takes an explicit `seed: int`. No
  hidden global RNG. If you need randomness, take it as a parameter.
- Windows-only paths go through `adapters/win_paths.py`. No bare
  `C:\` strings in services.

## PR checklist

- [ ] `pytest` passes
- [ ] `ruff check .` clean
- [ ] `mypy galaxyforge` clean
- [ ] New service has a pydantic input/output model
- [ ] No new global state

## Reporting

Open an issue with the seed, preset name, and the `.gfp` output. We can
reproduce any planet from `(seed, preset)`.