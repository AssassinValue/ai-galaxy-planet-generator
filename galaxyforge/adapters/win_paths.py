"""Windows path helpers. All export paths go through safe_join."""

from __future__ import annotations

import os
from pathlib import Path


def default_export_dir() -> Path:
    base = os.environ.get("LOCALAPPDATA") or str(Path.home())
    return Path(base) / "ai-galaxy-planet-generator" / "exports"


def safe_join(root: Path, *parts: str) -> Path:
    """Join parts under root, refusing anything that escapes root."""
    root = root.resolve()
    candidate = root.joinpath(*parts).resolve()
    if root != candidate and root not in candidate.parents:
        raise ValueError(f"path escapes export root: {candidate}")
    return candidate