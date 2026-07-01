import pandas as pd
import streamlit as st

# Setare pagină stilizată
st.set_page_config(page_title="Predictor Meciuri - Program33", layout="wide")
st.title("⚽ Predicții Meciuri din CSV (Stil Program33)")

# 1. Încărcare date
try:
    # Se încarcă fișierul CSV salvat de scraper-ul tău
    df = pd.read_csv("scores24.csv")
    
    # Curățare denumiri coloane în caz că au spații goale
    df.columns = [c.strip() for c in df.columns]
    
    st.success(f"Fișierul CSV a fost încărcat cu succes! Total meciuri brute: {len(df)}")
except Exception as e:
    st.error(f"Nu s-a putut găsi sau citi fișierul 'scores24.csv'. Asigură-te că este în același folder. Eroare: {e}")
    st.stop()

# 2. Aplicare Filtre Solicitate
# Convertim coloanele AX (HOME Played) și AY (AWAY Played) la valori numerice, erorile devenind NaN (goluri)
df['col51'] = pd.to_numeric(df['col51'], errors='coerce')  # Înlocuiește 'col51' cu numele real dacă diferă (ex: 'AW' sau 'col51' conform indexului imaginii 2)
df['col52'] = pd.to_numeric(df['col52'], errors='coerce')  # Înlocuiește cu indexul corespunzător AY

# Notă: Ajustează indexul coloanelor de cote conform structurii exacte. Presupunem 'col20' ca fiind cota 1 de pe piața principală.
df['col20'] = pd.to_numeric(df['col20'], errors='coerce') 

# Filtrare: Minim 6 meciuri jucate și eliminare rânduri fără date ("")
df_filtered = df.dropna(subset=['col51', 'col52'])
df_filtered = df_filtered[(df_filtered['col51'] >= 6) & (df_filtered['col52'] >= 6)]

# Filtrare: Cotă minimă 1.28
df_filtered = df_filtered[df_filtered['col20'] >= 1.28]

if df_filtered.empty:
    st.warning("Niciun meci nu a trecut de filtrele aplicate (Min 6 meciuri jucate și Cotă $\geq$ 1.28).")
else:
    st.metric(label="Meciuri filtrate și pregătite pentru predicție", value=len(df_filtered))

    # 3. Iterare și afișare meciuri în formatul dorit
    for index, row in df_filtered.iterrows():
        # Creăm un container vizual pentru fiecare meci
        with st.expander(f"🔴 {row['col1']} | {row['col2']} | {row['col3']} vs {row['col4']}", expanded=True):
            
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown("### ⏱️ Repriza 1 (HT)")
                st.write(f"**Scor HT probabil:** {row['col43']} (Probabilitate: {int(float(row['col44'])*100)}%)")
                st.write(f"**Scor HT secundar:** {row['col45']} (Probabilitate: {int(float(row['col46'])*100)}%)")
                st.write(f"**Predicție HT:** {row['col47']}")
                
                # Probabilități 1X2 la pauză
                p_ht_1 = int(float(row['col49']) * 100) if pd.notnull(row['col49']) else 0
                p_ht_x = int(float(row['col50']) * 100) if pd.notnull(row['col50']) else 0
                p_ht_2 = 100 - (p_ht_1 + p_ht_x)
                st.write(f"📊 **Probabilități HT (1/X/2):** {p_ht_1}% / {p_ht_x}% / {p_ht_2}%")

            with col_right:
                st.markdown("### 🏆 Meci Întreg (FT)")
                st.write(f"**Scor FT probabil:** {row['col7']} (Probabilitate: {int(float(row['col8'])*100)}%)")
                st.write(f"**Scor FT secundar:** {row['col9']} (Probabilitate: {int(float(row['col10'])*100)}%)")
                st.write(f"**Predicție FT:** {row['col11']}")
                
                # Probabilități 1X2 meci întreg
                p_ft_1 = int(float(row['col14']) * 100) if pd.notnull(row['col14']) else 0
                p_ft_x = int(float(row['col15']) * 100) if pd.notnull(row['col15']) else 0
                p_ft_2 = int(float(row['col16']) * 100) if pd.notnull(row['col16']) else 0
                st.write(f"📊 **Probabilități FT (1/X/2):** {p_ft_1}% / {p_ft_x}% / {p_ft_2}%")

            # Secțiunea de Cote și Linii Goluri
            st.markdown("---")
            c1, c2, c3, c4 = st.columns(4)
            
            with c1:
                st.markdown("**Cote 1X2 & Șansă Dublă**")
                st.write(f"1: `{row['col20']}` | X: `{row['col21']}` | 2: `{row['col22']}`")
                st.write(f"1X: `{row['col23']}` | 12: `{row['col24']}` | X2: `{row['col25']}`")
                
            with c2:
                st.markdown("**Linii Goluri (Peste)**")
                st.write(f"O0.5: `{row['col12']}` (Încredere: {int(float(row['col18'])*100)}%)")
                st.write(f"O1.5: `{row['col27'] if pd.notnull(row['col27']) else '-'}`")
                st.write(f"O2.5: `{row['col29'] if pd.notnull(row['col29']) else '-'}`")
                
            with c3:
                st.markdown("**Linii Goluri (Sub / Evaluare)**")
                st.write(f"Evaluare Goluri: `{row['col17']}`")
                st.write(f"Status Algoritm: `{row['col54'] if 'col54' in row else 'N/A'}`")
                
            with c4:
                st.markdown("**Meciuri Jucate**")
                st.write(f"Acasă (M): **{int(row['col51'])}**")
                st.write(f"Deplasare (M): **{int(row['col52'])}**")
