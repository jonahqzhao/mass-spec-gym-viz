import pandas as pd
import numpy as np

print("Loading dataframe...")

df = pd.read_pickle("./df_peaks_and_classes.pkl")

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

print(f"\nGrouped molecules: {len(grouped)}\n")

no_spectra = 0
empty_examples = []

for _, row in grouped.iterrows():
    mzs = row["mzs"]

    # handle different possible structures safely
    if mzs is None:
        count = 0
    elif isinstance(mzs, list):
        count = len(mzs)
    else:
        count = 1  # fallback if malformed

    if count == 0:
        no_spectra += 1
        if len(empty_examples) < 10:
            empty_examples.append(row["inchikey"])

print("\n================ SPECTRA COVERAGE =================\n")

print(f"Total molecules: {len(grouped)}")
print(f"Molecules with NO spectra: {no_spectra}")
print(f"Fraction missing spectra: {no_spectra / len(grouped):.4f}")

print("\n================ EXAMPLES (NO SPECTRA) =================\n")

for ik in empty_examples:
    print(ik)

print("\nDone.")