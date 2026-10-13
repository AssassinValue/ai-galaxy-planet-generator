"""Torch device selection. Falls back to CPU silently on failure."""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


def probe_device() -> str:
    try:
        import torch
    except ImportError:
        return "cpu"
    if torch.cuda.is_available():
        name = torch.cuda.get_device_name(0)
        log.info("CUDA device: %s", name)
        return "cuda"
    return "cpu"