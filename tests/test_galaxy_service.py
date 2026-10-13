"""Determinism and shape tests for the galaxy service."""

from __future__ import annotations

import numpy as np

from galaxyforge.models.requests import GalaxyRequest
from galaxyforge.services.galaxy_service import GalaxyService


def test_same_seed_s