"""Main window — wires buttons to handlers, nothing else."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from galaxyforge.handlers.galaxy_handler import GalaxyHandler
from galaxyforge.handlers.planet_handler import PlanetHandler
from galaxyforge.models.requests import GalaxyRequest, PlanetRequest


class MainWindow(QMainWindow):
    def __init__(self, services: dict[str, object]) -> None:
        super().__init__()
        self.setWindowTitle("ai-galaxy-planet-generator")
        self.resize(960, 640)

        self._planet_handler = PlanetHandler(services["generation"])  # type: ignore[arg-type]
        self._galaxy_handler = GalaxyHandler(services["galaxy"])  # type: ignore[arg-type]
        self._export_dir = services["export_dir"]

        root = QWidget()
        layout = QVBoxLayout(root)

        self._preset = QComboBox()
        self._preset.addItems(["terran", "desert", "ice", "volcanic"])
        self._seed = QSpinBox()
        self._seed.setRange(0, 2**31 - 1)
        self._seed.setValue(6767)

        row = QHBoxLayout()
        row.addWidget(QLabel("Preset"))
        row.addWidget(self._preset)
        row.addWidget(QLabel("Seed"))
        row.addWidget(self._seed)
        layout.addLayout(row)

        gen_planet = QPushButton("Generate planet")
        gen_planet.clicked.connect(self._on_planet)
        layout.addWidget(gen_planet)

        gen_galaxy = QPushButton("Generate galaxy")
        gen_galaxy.clicked.connect(self._on_galaxy)
        layout.addWidget(gen_galaxy)

        self._status = QLabel("ready")
        self._status.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self._status)

        self.setCentralWidget(root)

    def _on_planet(self) -> None:
        req = PlanetRequest(seed=self._seed.value(), preset=self._preset.currentText())
        result = self._planet_handler.handle(req)
        path = result.write(self._export_dir)  # type: ignore[arg-type]
        self._status.setText(f"wrote {path.name}")

    def _on_galaxy(self) -> None:
        req = GalaxyRequest(seed=self._seed.value())
        result = self._galaxy_handler.handle(req)
        path = result.write(self._export_dir)  # type: ignore[arg-type]
        self._status.setText(f"wrote {path.name} ({result.star_count} stars)")