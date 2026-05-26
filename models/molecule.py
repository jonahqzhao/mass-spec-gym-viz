from dataclasses import dataclass
from typing import List, Set

from models.spectrum import Spectrum


@dataclass
class Molecule:
    inchikey: str
    formula: str
    parent_mass: float

    smiles: str | None

    fold: str | None

    class1: str | None
    class2: str | None
    class3: str | None
    class4: str | None

    simulation_challenge: str | None

    spectra: List[Spectrum]

    elements: Set[str]

    def __post_init__(self):
        if self.spectra is None:
            self.spectra = []
    @property
    def spectrum_count(self):
        return len(self.spectra)