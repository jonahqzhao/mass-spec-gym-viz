import re

import numpy as np
import pandas as pd

from models.molecule import Molecule
from models.spectrum import Spectrum


ELEMENT_REGEX = r"[A-Z][a-z]?"


class MoleculeLoader:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def load(self):
        molecules = []

        for _, row in self.df.iterrows():
            molecule = self.row_to_molecule(row)
            molecules.append(molecule)

        return molecules

    def row_to_molecule(self, row):
        spectra = self.build_spectra(row)

        return Molecule(
            inchikey=row["inchikey"],
            formula=row["formula"],
            parent_mass=row["parent_mass"],
            smiles=row.get("smiles"),
            fold=row.get("fold"),
            class1=row.get("class1"),
            class2=row.get("class2"),
            class3=row.get("class3"),
            class4=row.get("class4"),
            simulation_challenge=row.get("simulation_challenge"),
            spectra=spectra,
            elements=self.extract_elements(row["formula"]),
        )

    def build_spectra(self, row):
        mzs_list = self.ensure_list(row["mzs"])
        intensities_list = self.ensure_list(row["intensities"])

        ppm_list = self.ensure_list(row.get("ppm_errors"))
        formulas_list = self.ensure_list(row.get("peak_formula_arrays"))

        instrument_list = self.ensure_list(row.get("instrument_type"))
        energy_list = self.ensure_list(row.get("collision_energy"))

        precursor_mz_list = self.ensure_list(row.get("precursor_mz"))
        precursor_formula_list = self.ensure_list(row.get("precursor_formula"))
        adduct_list = self.ensure_list(row.get("adduct"))

        n = len(mzs_list)

        spectra = []

        for i in range(n):
            mzs = self.safe_get(mzs_list, i)
            if mzs is None:
                mzs = []

            intensities = self.safe_get(intensities_list, i)
            if intensities is None:
                intensities = []

            spectrum = Spectrum(
                mzs=np.array(mzs),
                intensities=np.array(intensities),

                ppm_errors=self.optional_array(ppm_list, i),
                peak_formulas=self.optional_array(formulas_list, i),

                instrument_type=self.safe_get(instrument_list, i),
                collision_energy=self.safe_get(energy_list, i),

                precursor_mz=self.safe_get(precursor_mz_list, i),
                precursor_formula=self.safe_get(precursor_formula_list, i),
                adduct=self.safe_get(adduct_list, i),
            )

            spectra.append(spectrum)
        def safe_energy(e):
            if e is None:
                return float("inf")
            try:
                return float(e)
            except Exception:
                return float("inf")

        def spectrum_sort_key(s):
            instrument = str(s.instrument_type or "")
            energy = safe_energy(s.normalized_collision_energy)
            return (instrument, energy)

        spectra.sort(key=spectrum_sort_key)
        return spectra

    def extract_elements(self, formula):
        return set(re.findall(ELEMENT_REGEX, formula))

    def ensure_list(self, value):
        if isinstance(value, list):
            return value

        if isinstance(value, np.ndarray):
            return list(value)

        if value is None:
            return []

        if isinstance(value, float) and np.isnan(value):
            return []

        return [value]

    def safe_get(self, values, index):
        if index >= len(values):
            return None

        return values[index]

    def optional_array(self, values, index):
        value = self.safe_get(values, index)

        if value is None:
            return None

        return np.array(value)