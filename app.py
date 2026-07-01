import pandas as pd
import streamlit as st

# Setează configurarea paginii la început
st.set_page_config(page_title="Predictor Meciuri - Program33", layout="wide")
st.title("⚽ Predicții Meciuri din CSV (Stil Program33)")

# 🛠️ FUNCȚIE OPTIMIZATĂ CU CACHE - Încarcă și filtrează datele instant în memorie
@st.cache_data(ttl=600)  # Memorează datele timp de 10 minute, apoi verifică dacă CSV-ul s-a schimbat
def incarca_si_filtreaza_datele():
    try:
        # Citim CSV-ul utilizând doar coloanele indexate numeric de la 0 la 64
        coloane_numere = [f"col{i}" for i in range(1, 66)]
        
        # Încărcare rapidă: setăm header=0 și definim numele exacte ca să evităm erori de citire
        df = pd.read_csv("scores24.csv", names=coloane_numere, header=0, dtype=str)
        
        # Eliminăm spațiile goale din text
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
        # Convertim coloanele statistice pentru verificare (AX devine col51, AY devine col52)
        df['col51_num'] = pd.to_numeric(df['col51'], errors='coerce')
        df['col52_num'] = pd.to_numeric(df['col52'], errors='coerce')
        
        # Filtru 1: Elimină rândurile fără date și păstrează meciuri jucate >= 6
        df_filtrat = df.dropna(subset=['col51_num', 'col52_num'])
        df_filtrat = df_filtrat[(df_filtrat['col51_num'] >= 6) & (df_filtrat['col52_num'] >= 6)]
        
        # Convertim cota 1 (Piața A - col20) la număr pentru filtrare
        df_filtrat['col20_num'] = pd.to_numeric(df_filtrat['col20'], errors='coerce')
        
        # Filtru 2: Păstrează doar cotele valide mai mari sau egale cu 1.28
        df_filtrat = df_filtrat[df_filtrat['col20_num'] >= 1.28]
        
        return df_filtrat
    except Exception as e:
        return str(e)

# Apelarea funcției rapide din cache
date_meciuri = incarca_si_filtreaza_datele()

if isinstance(date_meciuri, str):
    st.error(f"Eroare la citirea fișierului 'scores24.csv'. Asigură-te că fișierul există în GitHub. Detalii: {date_meciuri}")
elif date_meciuri.empty:
    st.warning("Niciun meci nu îndeplinește condițiile stabilite (Minimum 6 meciuri jucate în AX/AY și Cotă minimă 1.28).")
else:
    st.success(f"Date încărcate instant! Meciuri găsite: {len(date_meciuri)}")

    # Afișarea structurată a meciurilor (Generare rapidă prin blocuri compacte)
    for index, row in date_meciuri.iterrows():
        with st.container():
            st.markdown(f"### 🔴 {row['col1']} | {row['col2']} | **{row['col3']}** vs **{row['col4']}**")
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown("**Scoruri Probabile**")
                st.write(f"Scor HT: `{row['col43']}` | Scor FT: `{row['col7']}`")
                st.write(f"Scor HT Secundar: `{row['col45']}` | Scor FT Secundar: `{row['col9']}`")
            with c2:
                st.markdown("**Probabilități 1X2**")
                st.write(f"HT: `{row['col49']}` / `{row['col50']}` / -")
                st.write(f"FT: `{row['col14']}` / `{row['col15']}` / `{row['col16']}`")
            with c3:
                st.markdown("**Cote Pariuri (1X2 / Șansă Dublă)**")
                st.write(f"1: `{row['col20']}` | X: `{row['col21']}` | 2: `{row['col22']}`")
                st.write(f"1X: `{row['col23']}` | 12: `{row['col24']}` | X2: `{row['col25']}`")
            with c4:
                st.markdown("**Linii Goluri & Meciuri**")
                st.write(f"Linii O0.5 / O1.5: `{row['col12']}` / `{row['col27']}`")
                st.write(f"Meciuri Jucate: **{int(row['col51_num'])}** Acasă / **{int(row['col52_num'])}** Deplasare")
            st.markdown("<hr style='margin:10px 0px;border-top:1px dashed #ccc;'/>", unsafe_allow_html=True)
