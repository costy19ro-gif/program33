import os
import streamlit as st

st.set_page_config(page_title="Program33 - Predictor", layout="wide")
st.title("⚽ Predicții Meciuri - Stil Program33")

cale_fisier = "scores24.csv"

if not os.path.exists(cale_fisier):
    st.error(f"Nu am găsit fișierul '{cale_fisier}' în GitHub!")
    st.stop()

meciuri_valide = 0

with open(cale_fisier, "r", encoding="utf-8", errors="ignore") as f:
    for linie in f:
        parti = [p.strip() for p in linie.split(",")]
        
        if len(parti) < 60:
            continue
            
        try:
            # 1. Extragere meciuri jucate (col51 pentru Gazde, col52 pentru Oaspeți)
            home_played = int(parti[50]) if parti[50].isdigit() else 0  
            away_played = int(parti[51]) if parti[51].isdigit() else 0  
            
            # Sari peste meciurile care nu au destul istoric (minim 6 meciuri)
            if home_played < 6 or away_played < 6:
                continue

            # 2. Extragere cote pentru verificare din ambele piețe (Piața A vs Piața B)
            try:
                cota_piata_A = float(parti[19]) if parti[19] else 0.0 # col20
                cota_piata_B = float(parti[34]) if parti[34] else 0.0 # col35
            except ValueError:
                cota_piata_A, cota_piata_B = 0.0, 0.0

            # Luăm cea mai mare cotă găsită pentru echipa favorită ca să vedem dacă trece de pragul de 1.28
            cota_maxima_favorit = max(cota_piata_A, cota_piata_B)

            # 3. Aplicarea filtrului de cotă minimă 1.28
            if cota_maxima_favorit >= 1.28:
                meciuri_valide += 1
                
                # Afișare meci formatat curat
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
                    st.markdown("**💰 Cote Pariuri**")
                    st.write(f"Piața A (col20): `{parti[19]}` | Piața B (col35): `{parti[34]}`")
                    st.write(f"Șansă Dublă X2: `{parti[24]}` | 12: `{parti[23]}`")
                with c4:
                    st.markdown("**⚽ Linii Goluri & Istoric**")
                    st.write(f"Sugestie Goluri: `{parti[11]}` (Încredere: `{parti[17]}`)")
                    st.write(f"Meciuri Jucate: **{home_played}** Gazde / **{away_played}** Oaspeți")
                
                st.markdown("<hr style='margin:12px 0px; border-top:1px dashed #bbb;'/>", unsafe_allow_html=True)
                
        except Exception:
            continue

if meciuri_valide == 0:
    st.info("Sistemul funcționează corect, dar momentan niciun meci din fișier nu îndeplinește criteriile (Min 6 meciuri și Cotă 1 ≥ 1.28).")
