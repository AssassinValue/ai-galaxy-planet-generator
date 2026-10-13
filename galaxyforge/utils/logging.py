"""Logging setup — quiet by default, verbose with GF_DEBUG=1."""

from __future__ import annotations

import logging
import os


def setup_logging() -> None:
    level = logging.DEBUG if os.environ.get("GF_DEBUG") == "1" else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )