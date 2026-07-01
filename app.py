import streamlit as st
import pandas as pd

st.title("Biletul Miliardar – BetMachine Pro 55 ULTRA")

@st.cache_data
def load_data():
    return pd.read_csv("scores24.csv")

def filter_matches(df):
    # Convertim coloanele la numere
    df["col50"] = pd.to_numeric(df["col50"], errors="coerce")
    df["col51"] = pd.to_numeric(df["col51"], errors="coerce")

    # Regula AX/AY > 6
    df = df[(df["col50"] > 6) & (df["col51"] > 6)]

    # Regula probabilități HT/FT
    df = df[
        (df["col9"] + df["col11"] > 0.40) &
        (df["col15"] > 0.25) &
        (df["col16"] > 0.35) &
        (df["col17"] > 0.20) &
        (df["col19"] > 0.75)
    ]

    return df

def generate_predictions(df):
    tickets = []

    for _, row in df.iterrows():
        if row["col8"] == "0-0" and row["col11"] > 0.18:
            pick = "O0.5 HT"
        elif row["col9"] + row["col11"] > 0.45:
            pick = "O1.5 FT"
        elif row["col15"] > 0.30 and row["col17"] > 0.20:
            pick = "GG"
        elif row["col12"] == "X2" or row["col56"] == "X2":
            pick = "X2"
        elif row["col12"] == "1X" or row["col56"] == "1X":
            pick = "1X"
        else:
            pick = "O1.5 FT"

        tickets.append({
            "league": row["col1"],
            "home": row["col3"],
            "away": row["col4"],
            "prediction": pick
        })

    return tickets

df = load_data()
df_filtered = filter_matches(df)
tickets = generate_predictions(df_filtered)

st.subheader("Biletul Miliardar")

for t in tickets[:8]:
    st.write(f"**{t['league']}** — {t['home']} vs {t['away']} → **{t['prediction']}**")
