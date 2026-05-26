from PySide6.QtCore import QObject, Signal

from data.filtering import MoleculeFilter


class MoleculeStore(QObject):
    molecules_changed = Signal()
    selected_molecule_changed = Signal(object)
    selected_spectrum_changed = Signal(object)

    def __init__(self, molecules):
        super().__init__()

        self.all_molecules = molecules
        self.filtered_molecules = molecules.copy()

        self.selected_molecule = None

        self.filter = MoleculeFilter()

        self.filtered_spectra = []
        self.selected_spectrum_index = 0

        self.show_labels = True
        self.ppm_cutoff = 10
        self.intensity_cutoff = 5

    def apply_filters(self):
        self.filtered_molecules = [
            m for m in self.all_molecules
            if self.filter.matches(m)
        ]

        self.molecules_changed.emit()

    def set_selected_molecule(self, molecule):
        self.selected_molecule = molecule

        self.filtered_spectra = sorted(
            molecule.spectra,
            key=lambda s: (
                s.collision_energy is None,
                s.collision_energy,
            )
        )

        self.selected_spectrum_index = 0

        self.selected_molecule_changed.emit(molecule)

        self.emit_selected_spectrum()

    @property
    def selected_spectrum(self):
        if not self.filtered_spectra:
            return None

        return self.filtered_spectra[self.selected_spectrum_index]

    def emit_selected_spectrum(self):
        self.selected_spectrum_changed.emit(
            self.selected_spectrum
        )

    def next_spectrum(self):
        if self.selected_spectrum_index >= len(self.filtered_spectra) - 1:
            return

        self.selected_spectrum_index += 1

        self.emit_selected_spectrum()

    def previous_spectrum(self):
        if self.selected_spectrum_index <= 0:
            return

        self.selected_spectrum_index -= 1

        self.emit_selected_spectrum()