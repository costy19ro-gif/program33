import streamlit as st
import pandas as pd

from utils.filters import filter_matches
from utils.predictions import generate_predictions

st.title("Biletul Miliardar – BetMachine Pro 55 ULTRA")

@st.cache_data
def load_data():
    return pd.read_csv("scores24.csv")

# 1. Încărcăm CSV-ul
df = load_data()

# 2. Aplicăm filtrarea (AX/AY + probabilități)
df_filtered = filter_matches(df)

# 3. Generăm predicțiile
tickets = generate_predictions(df_filtered)

# 4. Afișăm biletul miliardar
st.subheader("Biletul Miliardar")

if len(tickets) == 0:
    st.warning("Nu există meciuri care să respecte regulile.")
else:
    for t in tickets[:8]:
        st.write(f"**{t['league']}** — {t['home']} vs {t['away']} → **{t['prediction']}**")

# 5. Afișăm tabelul cu meciurile filtrate
st.subheader("Meciuri filtrate")
st.dataframe(df_filtered)
