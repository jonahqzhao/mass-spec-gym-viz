import pandas as pd
import numpy as np

def is_bad_row(row):
    c1, c2, c3, c4 = row["class1"], row["class2"], row["class3"], row["class4"]

    return (c1 == None and c2 == None and c3 == None and c4 == None)

if __name__ == "__main__":

    df = pd.read_pickle("./df_peaks_and_classes_fixed.pkl")

    print("Loaded:", df.shape)

    # find bad molecules
    bad_mask = df.apply(is_bad_row, axis=1)

    bad_df = df[bad_mask].copy()
    good_df = df[~bad_mask].copy()

    print("Bad molecules:", len(bad_df))
    print("Good molecules:", len(good_df))

    sample = bad_df.sample(min(10, len(bad_df)), random_state=42)

    for i, row in sample.iterrows():
        print("\n--- MOLECULE ---")
        print("inchikey:", row["inchikey"])
        print("smiles:", row["smiles"])
        print("class1:", row["class1"])
        print("class2:", row["class2"])
        print("class3:", row["class3"])
        print("class4:", row["class4"])

    # re-annotate ONLY bad ones
    #bad_df = reannotate_unique_smiles(bad_df)

    # merge back
    #df_fixed = pd.concat([good_df, bad_df], ignore_index=True)

    # save
    #df_fixed.to_pickle("./df_peaks_and_classes_fixed.pkl")

    print("Done.")