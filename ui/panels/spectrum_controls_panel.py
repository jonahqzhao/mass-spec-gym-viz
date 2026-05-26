from PySide6.QtWidgets import (
    QCheckBox,
    QDoubleSpinBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
)


class SpectrumControlsPanel(QWidget):
    def __init__(self, store):
        super().__init__()

        self.store = store

        layout = QVBoxLayout(self)

        self.prev_button = QPushButton("Previous Spectrum")
        self.next_button = QPushButton("Next Spectrum")

        self.instrument_label = QLabel("Instrument: None")
        self.energy_label = QLabel("Collision Energy: None")

        self.show_labels = QCheckBox("Show Labels")
        self.show_labels.setChecked(True)

        self.ppm_cutoff = QDoubleSpinBox()
        self.ppm_cutoff.setRange(0, 100)
        self.ppm_cutoff.setValue(10)
        self.ppm_cutoff.setPrefix("PPM Cutoff: ")

        self.intensity_cutoff = QDoubleSpinBox()
        self.intensity_cutoff.setRange(0, 100)
        self.intensity_cutoff.setValue(5)
        self.intensity_cutoff.setPrefix("Intensity %: ")

        layout.addWidget(self.prev_button)
        layout.addWidget(self.next_button)

        layout.addWidget(self.instrument_label)
        layout.addWidget(self.energy_label)

        layout.addWidget(self.show_labels)
        layout.addWidget(self.ppm_cutoff)
        layout.addWidget(self.intensity_cutoff)

        layout.addStretch()

        self.prev_button.clicked.connect(
            store.previous_spectrum
        )

        self.next_button.clicked.connect(
            store.next_spectrum
        )

        self.show_labels.stateChanged.connect(
            self.update_settings
        )

        self.ppm_cutoff.valueChanged.connect(
            self.update_settings
        )

        self.intensity_cutoff.valueChanged.connect(
            self.update_settings
        )

        store.selected_spectrum_changed.connect(
            self.update_metadata
        )

    def update_settings(self):
        self.store.show_labels = (
            self.show_labels.isChecked()
        )

        self.store.ppm_cutoff = (
            self.ppm_cutoff.value()
        )

        self.store.intensity_cutoff = (
            self.intensity_cutoff.value()
        )

        self.store.emit_selected_spectrum()

    def update_metadata(self, spectrum):
        if spectrum is None:
            self.instrument_label.setText(
                "Instrument: None"
            )

            self.energy_label.setText(
                "Collision Energy: None"
            )

            return

        instrument = (
            spectrum.instrument_type
            or "Unknown"
        )

        energy = (
            spectrum.collision_energy
            if spectrum.collision_energy is not None
            else "Unknown"
        )

        self.instrument_label.setText(
            f"Instrument: {instrument}"
        )

        self.energy_label.setText(
            f"Collision Energy: {energy}"
        )