from dataclasses import dataclass, field
from typing import Optional
import numpy as np
import math
import re


@dataclass
class Spectrum:
    mzs: np.ndarray
    intensities: np.ndarray

    ppm_errors: Optional[np.ndarray] = None
    peak_formulas: Optional[np.ndarray] = None

    instrument_type: Optional[str] = None
    collision_energy: Optional[object] = None  # allow raw pandas/numpy types safely

    precursor_mz: Optional[float] = None
    precursor_formula: Optional[str] = None
    adduct: Optional[str] = None

    relative_intensities: np.ndarray = field(init=False)
    normalized_collision_energy: Optional[float] = field(init=False)

    def __post_init__(self):
        # hard normalization boundary (critical)
        self.instrument_type = self._clean_str(self.instrument_type)

        self.mzs = np.asarray(self.mzs, dtype=float)
        self.intensities = np.asarray(self.intensities, dtype=float)

        self.relative_intensities = self.compute_relative_intensities()
        self.normalized_collision_energy = self.parse_collision_energy()

    def _clean_str(self, x):
        if x is None:
            return ""
        if isinstance(x, float) and math.isnan(x):
            return ""
        return str(x)

    def compute_relative_intensities(self):
        if self.intensities.size == 0:
            return np.array([])

        max_i = np.max(self.intensities)

        if max_i == 0 or np.isnan(max_i):
            return self.intensities.copy()

        return 100.0 * self.intensities / max_i

    def parse_collision_energy(self):
        """
        Guarantees output is: float | None
        NEVER returns string, NEVER returns NaN
        """

        e = self.collision_energy

        if e is None:
            return None

        # numpy / pandas NaN handling
        if isinstance(e, float) and math.isnan(e):
            return None

        # already numeric
        if isinstance(e, (int, float, np.floating)):
            if isinstance(e, float) and math.isnan(e):
                return None
            return float(e)

        # fallback: extract numeric part from strings like "20 eV", "HCD35"
        try:
            match = re.search(r"([0-9]+\.?[0-9]*)", str(e))
            if match:
                return float(match.group(1))
        except Exception:
            pass

        return None