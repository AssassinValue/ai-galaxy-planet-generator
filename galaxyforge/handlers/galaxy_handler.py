"""Thin handler for galaxy generation requests."""

from __future__ import annotations

from galaxyforge.models.requests import GalaxyRequest
from galaxyforge.models.results import GalaxyResult
from galaxyforge.services.galaxy_service import GalaxyService


class GalaxyHandler:
    def __init__(self, service: GalaxyService) -> None:
        self._service = service

    def handle(self, request: GalaxyRequest) -> GalaxyResult:
        return self._service.generate(request)