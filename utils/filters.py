import pandas as pd

def filter_matches(df):
    # Convertim AX și AY la numere
    df["col50"] = pd.to_numeric(df["col50"].astype(str).str.strip(), errors="coerce").fillna(0)
    df["col51"] = pd.to_numeric(df["col51"].astype(str).str.strip(), errors="coerce").fillna(0)

    # Convertim coloanele folosite la calcule
    numeric_cols = ["col9", "col11", "col15", "col16", "col17", "col19"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.strip(), errors="coerce").fillna(0)

    # Filtru echilibrat: AX/AY > 3 și probabilități rezonabile
    df = df[
        (df["col50"] > 3) &
        (df["col51"] > 3) &
        (df["col9"] + df["col11"] > 0.20) &
        (df["col15"] > 0.10) &
        (df["col16"] > 0.15) &
        (df["col17"] > 0.05) &
        (df["col19"] > 0.40)
    ]

    return df
