import pandas as pd


def valid(x):
    return pd.notna(x)


def is_bad_row(row):
    c1, c2, c3, c4 = (
        row["class1"],
        row["class2"],
        row["class3"],
        row["class4"],
    )

    return (
        (valid(c1) and valid(c2) and c1 == c2) or
        (valid(c2) and valid(c3) and c2 == c3) or
        (valid(c3) and valid(c4) and c3 == c4)
    )


# -----------------------------
# main
# -----------------------------
if __name__ == "__main__":

    df = pd.read_pickle("./df_peaks_and_classes.pkl")

    print("Loaded:", df.shape)

    # find bad molecules
    bad_mask = df.apply(is_bad_row, axis=1)

    bad_df = df[bad_mask].copy()

    print("Bad rows:", len(bad_df))

    # unique smiles only
    unique_bad = (
        bad_df[["inchikey", "smiles"]]
        .dropna(subset=["smiles"])
        .drop_duplicates(subset=["smiles"])
        .reset_index(drop=True)
    )

    print("Unique bad SMILES:", len(unique_bad))

    iters = len(unique_bad)//1000 + 1

    contents = [[] for _ in range(iters)]

    for i, row in unique_bad.iterrows():
        smiles = row["smiles"]
        contents[i//1000].append(smiles)

    for i in range(iters):
    
        # write output
        output_file = "input" + str(i) + ".txt"

        with open(output_file, "w") as f:
            for smiles in contents[i]:
                f.write(f"{smiles}\n")
        print(f"Wrote: {output_file}")