import streamlit as st
import pandas as pd
from utils.filters import filter_matches
from utils.predictions import (
    generate_predictions,
    generate_bilet_sigur,
    generate_bilet_combo,
    generate_bilet_bomba
)

st.set_page_config(page_title="BetMachine Pro 55 ULTRA", layout="wide")
st.title("BetMachine Pro 55 ULTRA – Generator de Bilete")

@st.cache_data
def load_data():
    return pd.read_csv("scores24.csv")

df = load_data()
df_filtered = filter_matches(df)

st.write("Număr meciuri filtrate:", len(df_filtered))

bilet_sigur = generate_bilet_sigur(df_filtered)
bilet_combo = generate_bilet_combo(df_filtered)
bilet_bomba = generate_bilet_bomba(df_filtered)
bilet_miliardar = generate_predictions(df_filtered)

st.subheader("Bilet SIGUR")
st.write(bilet_sigur)

st.subheader("Bilet COMBO")
st.write(bilet_combo)

st.subheader("Bilet BOMBĂ")
st.write(bilet_bomba)

st.subheader("Biletul Miliardar")
st.write(bilet_miliardar)
