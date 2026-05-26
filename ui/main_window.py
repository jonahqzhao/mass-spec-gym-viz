from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QMainWindow,
    QSplitter,
    QWidget,
)

from ui.molecule_table import MoleculeTable
from ui.panels.molecule_filters_panel import MoleculeFiltersPanel
from ui.panels.spectrum_controls_panel import SpectrumControlsPanel
from ui.spectrum_plot import SpectrumPlot


class MainWindow(QMainWindow):
    def __init__(self, store):
        super().__init__()

        self.store = store

        self.setWindowTitle("MS/MS Visualizer")
        self.resize(1800, 1000)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        self.filters_panel = MoleculeFiltersPanel(store)
        self.table = MoleculeTable(store)
        self.plot = SpectrumPlot(store)
        self.spectrum_controls = SpectrumControlsPanel(store)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(self.filters_panel)
        left_layout.addWidget(self.table)

        right_panel = QWidget()
        right_layout = QHBoxLayout(right_panel)
        right_layout.addWidget(self.plot)
        right_layout.addWidget(self.spectrum_controls)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)

        self.table.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )

        self.store.selected_spectrum_changed.connect(
            self.plot.set_spectrum
        )

    def on_selection_changed(self, selected, deselected):
        indexes = selected.indexes()

        if not indexes:
            return

        row = indexes[0].row()

        molecule = self.store.filtered_molecules[row]

        self.store.set_selected_molecule(molecule)