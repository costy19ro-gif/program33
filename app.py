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

st.title("🎫 Biletele Generate de Algoritmul Poisson/Dixon-Coles")

@st.cache_data
def load_data():
    return pd.read_csv("scores24.csv")

df = load_data()
df_filtered = filter_matches(df)

# --- BILET SIGUR ---
sigur = generate_bilet_sigur(df_filtered)
sigur_df = pd.DataFrame(sigur)
sigur_total = round(len(sigur_df) * 1.35, 2)  # exemplu calcul cota totală

with st.container():
    st.markdown("### 🟡 BILET SIGUR")
    st.write(f"**Cota totală:** {sigur_total}")
    st.write("🔼 Sub 20.00")
    st.table(sigur_df)
    st.write("💰 5 RON ➜ câștig potențial: {:.1f} RON".format(sigur_total * 5))

# --- BILET COMBO ---
combo = generate_bilet_combo(df_filtered)
combo_df = pd.DataFrame(combo)
combo_total = round(len(combo_df) * 2.25, 2)

with st.container():
    st.markdown("### 🔵 BILET COMBO VALUE")
    st.write(f"**Cota totală:** {combo_total}")
    st.write("🔼 3–4 selecții echilibrate")
    st.table(combo_df)
    st.write("💰 5 RON ➜ câștig potențial: {:.1f} RON".format(combo_total * 5))

# --- BILET BOMBĂ ---
bomba = generate_bilet_bomba(df_filtered)
bomba_df = pd.DataFrame(bomba)
bomba_total = round(len(bomba_df) * 3.00, 2)

with st.container():
    st.markdown("### 🔴 BILET BOMBĂ")
    st.write(f"**Cota totală:** {bomba_total}")
    if bomba_total < 3:
        st.warning("Nu s-au găsit selecții cu cotă ≥ 3.00")
    else:
        st.table(bomba_df)
    st.write("💰 2 RON ➜ câștig potențial: {:.1f} RON".format(bomba_total * 2))
