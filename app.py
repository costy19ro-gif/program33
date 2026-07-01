import streamlit as st
import pandas as pd

from utils.filters import filter_matches
from utils.predictions import (
    generate_predictions,
    generate_bilet_sigur,
    generate_bilet_combo,
    generate_bilet_bomba
)

st.title("BetMachine Pro 55 ULTRA – Generator de Bilete")

@st.cache_data
def load_data():
    return pd.read_csv("scores24.csv")

df = load_data()
df_filtered = filter_matches(df)

st.subheader("Biletul Miliardar")
tickets = generate_predictions(df_filtered)
for t in tickets:
    st.write(f"**{t['league']}** — {t['home']} vs {t['away']} → **{t['prediction']}**")

st.subheader("Bilet SIGUR")
sigur = generate_bilet_sigur(df_filtered)
for t in sigur:
    st.write(f"**{t['league']}** — {t['home']} vs {t['away']} → **{t['prediction']}**")

st.subheader("Bilet COMBO")
combo = generate_bilet_combo(df_filtered)
for t in combo:
    st.write(f"**{t['league']}** — {t['home']} vs {t['away']} → **{t['prediction']}**")

st.subheader("Bilet BOMBĂ")
bomba = generate_bilet_bomba(df_filtered)
for t in bomba:
    st.write(f"**{t['league']}** — {t['home']} vs {t['away']} → **{t['prediction']}**")

st.subheader("Meciuri filtrate")
st.dataframe(df_filtered)
