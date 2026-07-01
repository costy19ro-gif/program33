import pandas as pd

def filter_matches(df):
    # Convertim AX și AY (col50, col51) la numere
    df["col50"] = pd.to_numeric(df["col50"].astype(str).str.strip(), errors="coerce").fillna(0)
    df["col51"] = pd.to_numeric(df["col51"].astype(str).str.strip(), errors="coerce").fillna(0)

    # Convertim coloanele folosite la calcule
    numeric_cols = ["col9", "col11", "col15", "col16", "col17", "col19"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.strip(), errors="coerce").fillna(0)

    # Singura regulă de bază: AX și AY suficient de mari
    df = df[(df["col50"] > 4) & (df["col51"] > 4)]

    return df
