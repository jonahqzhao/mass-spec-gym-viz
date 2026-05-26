import sys

import pandas as pd

from PySide6.QtWidgets import QApplication

from data.loader import MoleculeLoader
from data.molecule_store import MoleculeStore
from ui.main_window import MainWindow


if __name__ == "__main__":
    df = pd.read_pickle("./df_peaks_and_classes_fixed.pkl")

    grouped = (
        df
        .groupby("inchikey")
        .agg({
            "mzs": list,
            "intensities": list,
            "collision_energy": list,
            "instrument_type": list,
            "adduct": list,
            "precursor_mz": list,
            "precursor_formula": list,
            "peak_formula_arrays": list,
            "ppm_errors": list,
            "smiles": "first",
            "formula": "first",
            "parent_mass": "first",
            "fold": "first",
            "class1": "first",
            "class2": "first",
            "class3": "first",
            "class4": "first",
            "simulation_challenge": "first",
        })
        .reset_index()
    )

    molecules = MoleculeLoader(grouped).load()

    app = QApplication(sys.argv)

    store = MoleculeStore(molecules)

    window = MainWindow(store)
    window.show()

    sys.exit(app.exec())