"""Thin handler for planet generation requests."""

from __future__ import annotations

from galaxyforge.models.requests import PlanetRequest
from galaxyforge.models.results import PlanetResult
from galaxyforge.services.generation_service import GenerationService


class PlanetHandler:
    def __init__(self, service: GenerationService) -> None:
        self._service = service

    def handle(self, request: PlanetRequest) -> PlanetResult:
        return self._service.generate_planet(request)