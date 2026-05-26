import numpy as np
import pyqtgraph as pg

from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout


class SpectrumPlot(QWidget):
    def __init__(self, store):
        super().__init__()

        self.store = store

        self.plot_widget = pg.PlotWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_widget)

        self.spectrum = None

    def set_spectrum(self, spectrum):
        self.spectrum = spectrum
        self.redraw()

    def redraw(self):
        self.plot_widget.clear()

        if self.spectrum is None:
            return

        mzs = self.spectrum.mzs
        intensities = self.spectrum.relative_intensities

        x = np.repeat(mzs, 3)

        y = np.zeros(len(x))
        y[1::3] = intensities

        self.plot_widget.plot(x, y)

        if self.store.show_labels:
            self.draw_labels()

    def draw_labels(self):
        if self.spectrum.peak_formulas is None:
            return

        if self.spectrum.ppm_errors is None:
            return

        for mz, intensity, ppm, formula in zip(
            self.spectrum.mzs,
            self.spectrum.relative_intensities,
            self.spectrum.ppm_errors,
            self.spectrum.peak_formulas,
        ):
            if ppm is None:
                continue

            if abs(ppm) > self.store.ppm_cutoff:
                continue

            if intensity < self.store.intensity_cutoff:
                continue

            text = self.format_formula(formula)

            if not text:
                continue

            label = pg.TextItem(text, anchor=(0.5, 0))
            label.setPos(mz, intensity)

            self.plot_widget.addItem(label)

    @staticmethod
    def format_formula(arr):
        if arr is None:
            return ""

        elements = ["C", "H", "N", "O", "P", "S"]

        parts = []

        for el, count in zip(elements, arr):
            if count > 0:
                parts.append(f"{el}{int(count)}")

        return "".join(parts)