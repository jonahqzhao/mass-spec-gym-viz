import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from collections import Counter
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

OUTPUT_DIR = "misc-plots"

# =========================
# LOAD DATA
# =========================

df = pd.read_pickle("./df_peaks_and_classes.pkl")

print("Loaded dataframe")
print(df.shape)


# =========================
# BASIC CLEANUP
# =========================

df = df.copy()

df["parent_mass"] = pd.to_numeric(
    df["parent_mass"],
    errors="coerce"
)

df["collision_energy"] = pd.to_numeric(
    df["collision_energy"],
    errors="coerce"
)

df["instrument_type"] = (
    df["instrument_type"]
    .fillna("Unknown")
    .astype(str)
)

df["class1"] = (
    df["class1"]
    .fillna("Unknown")
    .astype(str)
)

df["class2"] = (
    df["class2"]
    .fillna("Unknown")
    .astype(str)
)

df["class3"] = (
    df["class3"]
    .fillna("Unknown")
    .astype(str)
)


# =========================
# 1. PARENT MASS DISTRIBUTION
# =========================

plt.figure(figsize=(12, 6))

for cls in df["class1"].value_counts().head(10).index:
    subset = df[df["class1"] == cls]

    plt.hist(
        subset["parent_mass"].dropna(),
        bins=50,
        alpha=0.5,
        label=cls
    )

plt.xlabel("Parent Mass")
plt.ylabel("Count")
plt.title("Parent Mass Distribution by Class1")
plt.legend()

plt.savefig(
    f"{OUTPUT_DIR}/mass-dist.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# =========================
# 2. CLASS IMBALANCE
# =========================

class_counts = (
    df["class1"]
    .value_counts()
    .head(30)
)

plt.figure(figsize=(14, 8))

class_counts.plot(kind="bar")

plt.ylabel("Count")
plt.title("Top 30 Class1 Categories")

plt.xticks(rotation=90)

plt.savefig(
    f"{OUTPUT_DIR}/class1-cat.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

class_counts = (
    df["class2"]
    .value_counts()
    .head(30)
)

plt.figure(figsize=(14, 8))

class_counts.plot(kind="bar")

plt.ylabel("Count")
plt.title("Top 30 Class2 Categories")

plt.xticks(rotation=90)

plt.savefig(
    f"{OUTPUT_DIR}/class2-cat.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

class_counts = (
    df["class3"]
    .value_counts()
    .head(30)
)

plt.figure(figsize=(14, 8))

class_counts.plot(kind="bar")

plt.ylabel("Count")
plt.title("Top 30 Class4 Categories")

plt.xticks(rotation=90)

plt.savefig(
    f"{OUTPUT_DIR}/class4-cat.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

class_counts = (
    df["class4"]
    .value_counts()
    .head(30)
)

plt.figure(figsize=(14, 8))

class_counts.plot(kind="bar")

plt.ylabel("Count")
plt.title("Top 30 Class4 Categories")

plt.xticks(rotation=90)

plt.savefig(
    f"{OUTPUT_DIR}/class4-cat.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

# =========================
# 3. PEAK COUNT VS PARENT MASS
# =========================

peak_counts = df["mzs"].apply(
    lambda x: len(x) if isinstance(x, list) else 0
)

plt.figure(figsize=(10, 6))

plt.scatter(
    df["parent_mass"],
    peak_counts,
    alpha=0.3
)

plt.xlabel("Parent Mass")
plt.ylabel("Number of Peaks")
plt.title("Peak Count vs Parent Mass")

plt.savefig(
    f"{OUTPUT_DIR}/peaks-vs-mass.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# =========================
# 4. COLLISION ENERGY VS PEAK COUNT
# =========================

plt.figure(figsize=(10, 6))

plt.scatter(
    df["collision_energy"],
    peak_counts,
    alpha=0.3
)

plt.xlabel("Collision Energy")
plt.ylabel("Number of Peaks")
plt.title("Collision Energy vs Peak Count")

plt.savefig(
    f"{OUTPUT_DIR}/ce-vs-peaks.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# =========================
# 5. GLOBAL FRAGMENT FREQUENCY
# =========================

all_mzs = []

for mzs in df["mzs"]:
    if mzs is None:
        continue

    try:
        arr = np.asarray(
            mzs,
            dtype=float
        )
    except Exception:
        continue

    arr = arr[~np.isnan(arr)]

    all_mzs.extend(arr.tolist())

all_mzs = np.array(all_mzs)

print("Total fragments:", len(all_mzs))

plt.figure(figsize=(14, 6))

plt.hist(
    all_mzs,
    bins=500
)

plt.xlabel("Fragment m/z")
plt.ylabel("Frequency")
plt.title("Global Fragment Frequency")

plt.savefig(
    f"{OUTPUT_DIR}/frag-freq.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# =========================
# 6. NEUTRAL LOSS DISTRIBUTION
# =========================

neutral_losses = []

for precursor, mzs in zip(
    df["precursor_mz"],
    df["mzs"]
):
    if precursor is None:
        continue

    if pd.isna(precursor):
        continue

    if mzs is None:
        continue

    try:
        mzs = np.asarray(mzs, dtype=float)
    except Exception:
        continue

    for mz in mzs:
        if np.isnan(mz):
            continue

        loss = precursor - mz

        if 0 < loss < 1000:
            neutral_losses.append(loss)

neutral_losses = np.array(neutral_losses)

print("Neutral losses:", len(neutral_losses))

plt.figure(figsize=(14, 6))

plt.hist(
    neutral_losses,
    bins=300
)

plt.xlabel("Neutral Loss")
plt.ylabel("Frequency")
plt.title("Neutral Loss Distribution")

plt.savefig(
    f"{OUTPUT_DIR}/neutral-losses.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# =========================
# 7. PPM ERROR DISTRIBUTION
# =========================

ppm_values = []

for ppm_list in df["ppm_errors"]:
    if isinstance(ppm_list, list):
        ppm_values.extend([
            x for x in ppm_list
            if x is not None
        ])

ppm_values = np.array(ppm_values)

plt.figure(figsize=(10, 6))

plt.hist(
    ppm_values,
    bins=200
)

plt.xlabel("PPM Error")
plt.ylabel("Frequency")
plt.title("PPM Error Distribution")

plt.xlim(-20, 20)

plt.savefig(
    f"{OUTPUT_DIR}/PPM-err.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# =========================
# 8. INSTRUMENT DISTRIBUTION
# =========================

instrument_counts = (
    df["instrument_type"]
    .value_counts()
    .head(20)
)

plt.figure(figsize=(12, 6))

instrument_counts.plot(kind="bar")

plt.ylabel("Count")
plt.title("Instrument Type Distribution")

plt.xticks(rotation=45)

plt.savefig(
    f"{OUTPUT_DIR}/ID.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# =========================
# 9. MISSING METADATA HEATMAP
# =========================

missing = df[
    [
        "collision_energy",
        "instrument_type",
        "adduct",
        "ppm_errors",
        "peak_formula_arrays",
    ]
].isnull()

plt.figure(figsize=(8, 6))

plt.imshow(
    missing.T,
    aspect="auto"
)

plt.yticks(
    range(len(missing.columns)),
    missing.columns
)

plt.title("Missing Metadata Heatmap")

plt.savefig(
    f"{OUTPUT_DIR}/MMH.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# =========================
# 10. SIMPLE SPECTRUM ENTROPY
# =========================

def spectrum_entropy(intensities):
    if intensities is None:
        return np.nan

    try:
        arr = np.asarray(
            intensities,
            dtype=float
        )
    except Exception:
        return np.nan

    arr = arr[~np.isnan(arr)]

    if len(arr) == 0:
        return np.nan

    total = np.sum(arr)

    if total <= 0:
        return np.nan

    probs = arr / total

    return -np.sum(
        probs * np.log(probs + 1e-12)
    )


entropy_values = df["intensities"].apply(
    spectrum_entropy
)

entropy_values = entropy_values.dropna()

print("Entropy values:", len(entropy_values))

plt.figure(figsize=(10, 6))

plt.hist(
    entropy_values,
    bins=100
)

plt.xlabel("Spectrum Entropy")
plt.ylabel("Frequency")
plt.title("Spectrum Entropy Distribution")

plt.savefig(
    f"{OUTPUT_DIR}/SED.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()
