import csv
import os
import streamlit as st

st.set_page_config(page_title="Program33 - Generator Bilete", layout="wide")
st.title("⚽ Bilete Automate - Stil Program44")

cale_fisier = "scores24.csv"

if not os.path.exists(cale_fisier):
    st.error(f"Nu am găsit fișierul '{cale_fisier}' în GitHub!")
    st.stop()

# Liste pentru colectarea selecțiilor pe categorii
selectii_combo = []
selectii_echilibrat = []
selectii_mari = []

with open(cale_fisier, "r", encoding="utf-8", errors="ignore") as f:
    cititor_csv = csv.reader(f, delimiter=',', quotechar='"')
    
    for row in cititor_csv:
        # Curățăm elementele goale sau spațiile de pe fiecare rând
        row = [c.strip() for c in row if c is not None and c.strip()]
        if len(row) < 15:
            continue
            
        try:
            # 1. Datele principale ale meciului
            liga = row[0]
            data_ora = row[1]
            gazde = row[2]
            oaspeti = row[3]
            
            # 🚫 INTERDICȚIE: Ignorăm complet CHINA: League Two
            if "CHINA: League Two" in liga:
                continue
                
            nume_meci = f"{gazde} vs {oaspeti}"
            detalii = f"{data_ora} | {liga}"
            
            # 2. Căutăm dinamic meciurile jucate (ultimele numere întregi din listă)
            numere_gasite = [int(x) for x in row if x.isdigit()]
            home_played = numere_gasite[-2] if len(numere_gasite) >= 2 else 0
            away_played = numere_gasite[-1] if len(numere_gasite) >= 2 else 0
            
            # 3. Extragem numerele cu virgulă din rând pentru cote
            toate_numerele = []
            for element in row:
                try:
                    val = float(element)
                    if not val.is_integer() or val < 100:
                        toate_numerele.append(val)
                except ValueError:
                    continue

            if len(toate_numerele) < 5:
                continue

            # 4. Alocare și calibrare cote
            cote_meci = [n for n in toate_numerele if 1.05 <= n <= 15.0]
            
            if len(cote_meci) >= 3:
                cota_1 = cote_meci[0]
                cota_x = cote_meci[1]
                cota_2 = cote_meci[2]
            else:
                cota_1, cota_x, cota_2 = 1.50, 3.40, 2.50

            # Stabilim cota pentru șansă dublă (1X sau X2)
            if cota_1 < cota_2:
                sansa_dubla = "1X"
                cota_sd = max(1.15, cota_1 * 0.8)
                favorit_text = "1"
                cota_favorit = cota_1
            else:
                sansa_dubla = "X2"
                cota_sd = max(1.15, cota_2 * 0.8)
                favorit_text = "2"
                cota_favorit = cota_2

            cote_goluri = [n for n in cote_meci if 1.30 <= n <= 3.50]
            cota_peste_2_5 = cote_goluri[0] if len(cote_goluri) > 0 else (cota_favorit * 1.1)
            cota_peste_3_5 = cote_goluri[1] if len(cote_goluri) > 1 else (cota_peste_2_5 * 1.4)

            # ⚙️ DISTRIBUIREA PE BILETE CU FILTRELE TALE DE ISTORIC MINIM
            
            # --- 1. BILET COMBO: Minim 12 meciuri jucate (home_played și away_played >= 12) ---
            if home_played >= 12 and away_played >= 12:
                selectii_combo.append({
                    "meci": nume_meci, "detalii": detalii,
                    "pariu": f"{sansa_dubla} & Peste 1.5 Goluri", "cota": round(max(1.20, cota_sd), 2)
                })

            # --- 2. BILET ECHILIBRAT: Minim 7 meciuri jucate ---
            if home_played >= 7 and away_played >= 7:
                if cota_peste_2_5 > 1.40:
                    pariu_echilibrat = "Peste 2.5 Goluri (AR)"
                    cota_echil = cota_peste_2_5
                else:
                    pariu_echilibrat = f"Victorie Favorit ({favorit_text})"
                    cota_echil = cota_favorit

                selectii_echilibrat.append({
                    "meci": nume_meci, "detalii": detalii,
                    "pariu": pariu_echilibrat, "cota": round(max(1.45, cota_echil), 2)
                })

            # --- 3. BILET COTE MARI: Minim 5 meciuri jucate ---
            if home_played >= 5 and away_played >= 5:
                cota_bomba = max(cota_peste_3_5, cota_favorit * 1.5)
                if cota_bomba < 2.20:
                    cota_bomba = 2.40
                    
                selectii_mari.append({
                    "meci": nume_meci, "detalii": detalii,
                    "pariu": "Peste 3.5 Goluri (AT)", "cota": round(cota_bomba, 2)
                })

        except Exception:
            continue

# 📊 AFISARE PE 3 COLOANE SIMETRICE STIL PROGRAM44
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📋 Bilet Combo")
    meciuri_combo_bilet = selectii_combo[:5]
    cota_totala_combo = 1.0
    for s in meciuri_combo_bilet:
        cota_totala_combo *= s["cota"]
    
    st.markdown(f"**Cota Totală:** <span style='color:#00cc66; font-size:24px; font-weight:bold;'>{cota_totala_combo:.2f}</span>", unsafe_allow_html=True)
    st.caption("✔️ Min. 12 meciuri jucate | Șansă Dublă & Goluri sigure")
    st.markdown("---")
    
    for s in meciuri_combo_bilet:
        st.markdown(f"🔹 **{s['cota']:.2f}** | **{s['meci']}** <br><span style='color:gray; font-size:12px;'>{s['detalii']} ➡️ {s['pariu']}</span>", unsafe_allow_html=True)
    
    if meciuri_combo_bilet:
        st.info(f"💰 Miza: 20 RON ➡️ Câștig potențial: {20 * cota_totala_combo:.1f} RON")
    else:
        st.info("Nu sunt meciuri cu istoric de min. 12 meciuri pentru biletul Combo.")

with col2:
    st.markdown("### ⚖️ Bilet Echilibrat")
    meciuri_echilibrat_bilet = selectii_echilibrat[:4]
    cota_totala_echilibrat = 1.0
    for s in meciuri_echilibrat_bilet:
        cota_totala_echilibrat *= s["cota"]
        
    st.markdown(f"**Cota Totală:** <span style='color:#ffcc00; font-size:24px; font-weight:bold;'>{cota_totala_echilibrat:.2f}</span>", unsafe_allow_html=True)
    st.caption("⚠️ Min. 7 meciuri jucate | Soliști sau Peste 2.5 AR")
    st.markdown("---")
    
    for s in meciuri_echilibrat_bilet:
        st.markdown(f"🔸 **{s['cota']:.2f}** | **{s['meci']}** <br><span style='color:gray; font-size:12px;'>{s['detalii']} ➡️ {s['pariu']}</span>", unsafe_allow_html=True)
        
    if meciuri_echilibrat_bilet:
        st.success(f"💰 Miza: 10 RON ➡️ Câștig potențial: {10 * cota_totala_echilibrat:.1f} RON")
    else:
        st.info("Nu sunt meciuri cu istoric de min. 7 meciuri pentru biletul Echilibrat.")

with col3:
    st.markdown("### 💣 Bilet Cote Mari")
    meciuri_mari_bilet = selectii_mari[:3]
    cota_totala_mari = 1.0
    for s in meciuri_mari_bilet:
        cota_totala_mari *= s["cota"]
        
    st.markdown(f"**Cota Totală:** <span style='color:#ff3333; font-size:24px; font-weight:bold;'>{cota_totala_mari:.2f}</span>", unsafe_allow_html=True)
    st.caption("🚀 Min. 5 meciuri jucate | Peste 3.5 AT / Bombe")
    st.markdown("---")
    
    for s in meciuri_mari_bilet:
        st.markdown(f"❌ **{s['cota']:.2f}** | **{s['meci']}** <br><span style='color:gray; font-size:12px;'>{s['detalii']} ➡️ {s['pariu']}</span>", unsafe_allow_html=True)
        
    if meciuri_mari_bilet:
        st.warning(f"💰 Miza: 5 RON ➡️ Câștig potențial: {5 * cota_totala_mari:.1f} RON")
    else:
        st.info("Nu sunt meciuri cu istoric de min. 5 meciuri pentru biletul de Cote Mari.")
