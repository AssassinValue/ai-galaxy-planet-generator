"""Desktop entry point. Boots Qt, wires services, opens the main window."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from galaxyforge.adapters.gpu_probe import probe_device
from galaxyforge.adapters.win_paths import default_export_dir
from galaxyforge.config.loader import load_config
from galaxyforge.services.galaxy_service import GalaxyService
from galaxyforge.services.generation_service import GenerationService
from galaxyforge.services.terrain_service import TerrainService
from galaxyforge.ui.main_window import MainWindow
from galaxyforge.utils.logging import setup_logging


def build_services() -> dict[str, object]:
    cfg = load_config(Path(__file__).parents[2] / "config" / "default.yaml")
    device = probe_device()
    return {
        "generation": GenerationService(device=device, presets=cfg.presets),
        "terrain": TerrainService(),
        "galaxy": GalaxyService(),
        "export_dir": default_export_dir(),
    }


def main() -> int:
    setup_logging()
    app = QApplication(sys.argv)
    app.setApplicationName("ai-galaxy-planet-generator")
    services = build_services()
    window = MainWindow(services=services)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())