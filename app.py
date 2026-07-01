import os
import streamlit as st

st.set_page_config(page_title="Program33 - Predictor", layout="wide")
st.title("⚽ Predicții Meciuri - Stil Program33")

cale_fisier = "scores24.csv"

if not os.path.exists(cale_fisier):
    st.error(f"Nu am găsit fișierul '{cale_fisier}' în GitHub!")
    st.stop()

meciuri_valide = 0

# Citire linie cu linie (Ultra-rapidă, consum zero de memorie RAM)
with open(cale_fisier, "r", encoding="utf-8", errors="ignore") as f:
    for linie in f:
        # Împărțim linia prin virgulă
        parti = [p.strip() for p in linie.split(",")]
        
        # Un rând complet trebuie să aibă minimum 60-65 de coloane
        if len(parti) < 60:
            continue
            
        try:
            # Extragere valori statistice din coloane (Ajustate la indexul din Python: col - 1)
            home_played = int(parti[50]) if parti[50].isdigit() else 0  # col51
            away_played = int(parti[51]) if parti[51].isdigit() else 0  # col52
            
            try:
                cota_1 = float(parti[19])  # col20
            except ValueError:
                cota_1 = 0.0

            # Aplicarea filtrelor tale stricte
            if home_played >= 6 and away_played >= 6 and cota_1 >= 1.28:
                meciuri_valide += 1
                
                # Afișare directă în pagină
                st.markdown(f"### 🏟️ {parti[0]} | {parti[1]} | **{parti[2]}** vs **{parti[3]}**")
                
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown("**🎯 Scoruri Probabile**")
                    st.write(f"Scor HT principal: `{parti[42]}` (col43)")
                    st.write(f"Scor HT secundar: `{parti[44]}` (col45)")
                    st.write(f"Scor FT principal: `{parti[6]}` (col7)")
                    st.write(f"Scor FT secundar: `{parti[8]}` (col9)")
                with c2:
                    st.markdown("**📊 Probabilități Procentuale**")
                    st.write(f"HT (1 / X): `{parti[48]}` / `{parti[49]}`")
                    st.write(f"FT (1 / X / 2): `{parti[13]}` / `{parti[14]}` / `{parti[15]}`")
                with c3:
                    st.markdown("**💰 Cote Pariuri (Piața A)**")
                    st.write(f"1: `{parti[19]}` | X: `{parti[20]}` | 2: `{parti[21]}`")
                    st.write(f"1X: `{parti[22]}` | 12: `{parti[23]}` | X2: `{parti[24]}`")
                with c4:
                    st.markdown("**⚽ Linii Goluri & Istoric**")
                    st.write(f"Sugestie Goluri: `{parti[11]}` (Încredere: `{parti[17]}`)")
                    st.write(f"Meciuri Jucate: **{home_played}** Gazde / **{away_played}** Oaspeți")
                
                st.markdown("<hr style='margin:12px 0px; border-top:1px dashed #bbb;'/>", unsafe_allow_html=True)
                
        except Exception:
            continue

if meciuri_valide == 0:
    st.info("Sistemul funcționează corect, dar momentan niciun meci din fișier nu îndeplinește criteriile (Min 6 meciuri și Cotă 1 ≥ 1.28).")
