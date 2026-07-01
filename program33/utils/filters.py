import pandas as pd

def filter_matches(df):
    # Convertim AX și AY la numere
    df["col50"] = pd.to_numeric(df["col50"].astype(str).str.strip(), errors="coerce").fillna(0)
    df["col51"] = pd.to_numeric(df["col51"].astype(str).str.strip(), errors="coerce").fillna(0)

    # Regula AX/AY > 6
    df = df[(df["col50"] > 6) & (df["col51"] > 6)]

    # Convertim coloanele folosite la calcule
    numeric_cols = ["col9", "col11", "col15", "col16", "col17", "col19"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.strip(), errors="coerce").fillna(0)

    # Regula probabilități HT/FT
    df = df[
        (df["col9"] + df["col11"] > 0.40) &
        (df["col15"] > 0.25) &
        (df["col16"] > 0.35) &
        (df["col17"] > 0.20) &
        (df["col19"] > 0.75)
    ]

    return df
