import os
import pandas as pd
import streamlit as st

# 1. Configurare pagină (Trebuie să fie prima instrucțiune Streamlit)
st.set_page_config(page_title="Program33 - Predictor", layout="wide")
st.title("⚽ Predicții Meciuri - Stil Program33")

# 2. Funcție ultra-rapidă cu citire brută și indexare automată
@st.cache_data(ttl=300)  # Memorează datele 5 minute pentru a nu bloca serverul
def incarca_date_brute():
    cale_fisier = "scores24.csv"
    
    if not os.path.exists(cale_fisier):
        return f"Eroare: Fișierul '{cale_fisier}' nu a fost găsit în directorul curent!"
        
    try:
        # Generăm automat 65 de nume de coloane: col1, col2 ... col65
        nume_coloane = [f"col{i}" for i in range(1, 66)]
        
        # Citim CSV-ul forțând toate celulele ca text (elimină blocajele de conversie automată)
        # header=None îi spune lui pandas că prima linie este deja un meci, nu cap de tabel
        df = pd.read_csv(
            cale_fisier, 
            names=nume_coloane, 
            header=None, 
            dtype=str, 
            on_bad_lines='skip'
        )
        return df
    except Exception as e:
        return f"Eroare la procesarea fișierului CSV: {str(e)}"

# Apelăm funcția de încărcare
df_raw = incarca_date_brute()

# Verificăm dacă încărcarea a eșuat sau a întors text de eroare
if isinstance(df_raw, str):
    st.error(df_raw)
    st.info("Asigură-te că fișierul 'scores24.csv' este încărcat corect în repozitorul tău de GitHub.")
    st.stop()

# 3. Aplicare Filtre Solicitate
try:
    # Curățăm spațiile goale accidentale din text
    for col in df_raw.columns:
        df_raw[col] = df_raw[col].fillna("").astype(str).str.strip()

    # Identificăm corect coloanele conform structurii tale:
    # col51 = HOME Played (Meciuri jucate acasă)
    # col52 = AWAY Played (Meciuri jucate deplasare)
    # col20 = Cota pentru victoria gazdelor (Piața A)
    
    df_raw['home_played_num'] = pd.to_numeric(df_raw['col51'], errors='coerce')
    df_raw['away_played_num'] = pd.to_numeric(df_raw['col52'], errors='coerce')
    df_raw['cota_1_num'] = pd.to_numeric(df_raw['col20'], errors='coerce')

    # Filtru: Să nu fie goale ("") și să aibă minimum 6 meciuri jucate
    df_filtrat = df_raw.dropna(subset=['home_played_num', 'away_played_num'])
    df_filtrat = df_filtrat[(df_filtrat['home_played_num'] >= 6) & (df_filtrat['away_played_num'] >= 6)]

    # Filtru: Cota minimă să fie 1.28
    df_filtrat = df_filtrat[df_filtrat['cota_1_num'] >= 1.28]

except Exception as filter_error:
    st.error(f"Eroare la filtrarea datelor: {filter_error}")
    st.stop()

# 4. Afișare rezultate în interfață
if df_filtrat.empty:
    st.warning("⚠️ Niciun meci din CSV nu îndeplinește criteriile: Minim 6 meciuri jucate (col51/col52) și Cotă 1 ≥ 1.28 (col20).")
else:
    st.success(f"⚡ Date procesate instant! Au fost găsite {len(df_filtrat)} meciuri care respectă filtrele.")

    # Generăm blocurile de predicții exact în formatul cerut
    for idx, row in df_filtrat.iterrows():
        # Titlu meci proeminent
        st.markdown(f"### 🏟️ {row['col1']} | {row['col2']} | **{row['col3']}** vs **{row['col4']}**")
        
        # Grid cu 4 coloane pentru organizarea informațiilor sportive
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown("**🎯 Scoruri Probabile**")
            st.write(f"Scor HT principal: `{row['col43']}`")
            st.write(f"Scor HT secundar: `{row['col45']}`")
            st.write(f"Scor FT principal: `{row['col7']}`")
            st.write(f"Scor FT secundar: `{row['col9']}`")
            
        with c2:
            st.markdown("**📊 Probabilități Procentuale**")
            st.write(f"HT (1 / X): `{row['col49']}` / `{row['col50']}`")
            st.write(f"FT (1 / X / 2): `{row['col14']}` / `{row['col15']}` / `{row['col16']}`")
            
        with c3:
            st.markdown("**💰 Cote Pariuri (Piața A)**")
            st.write(f"1: `{row['col20']}` | X: `{row['col21']}` | 2: `{row['col22']}`")
            st.write(f"1X: `{row['col23']}` | 12: `{row['col24']}` | X2: `{row['col25']}`")
            
        with c4:
            st.markdown("**⚽ Linii Goluri & Istoric**")
            st.write(f"Sugestie Goluri: `{row['col12']}` (Încredere: `{row['col18']}`)")
            st.write(f"Evaluare algoritm: `{row['col17']}`")
            st.write(f"Meciuri Jucate: **{int(row['home_played_num'])}** Gazde / **{int(row['away_played_num'])}** Oaspeți")
            
        # Linie de demarcație vizuală între meciuri
        st.markdown("<hr style='margin:12px 0px; border-top:1px dashed #bbb;'/>", unsafe_allow_html=True)
