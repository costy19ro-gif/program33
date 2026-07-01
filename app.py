import csv
import os
import streamlit as st

st.set_page_config(page_title="Program33 - Generator Profit", layout="wide")
st.title("⚽ Bilete Automate de Profit - Stil Program44")

cale_fisier = "scores24.csv"

if not os.path.exists(cale_fisier):
    st.error(f"Nu am găsit fișierul '{cale_fisier}' în GitHub!")
    st.stop()

# Liste pentru cele 3 strategii de bilet
selectii_combo = []       # Strategia 1: Șansă Dublă / Peste 1.5
selectii_echilibrat = []  # Strategia 2: Peste 2.5 goluri (Coloana AR)
selectii_bomba = []       # Strategia 3: Peste 3.5 goluri (Coloana AT)

with open(cale_fisier, "r", encoding="utf-8", errors="ignore") as f:
    cititor_csv = csv.reader(f, delimiter=',', quotechar='"')
    
    for row in cititor_csv:
        row = [c.strip() for c in row if c is not None]
        # Un rând stabil trebuie să aibă suficiente coloane pentru a prinde AT (coloana 46+)
        if len(row) < 55:
            continue
            
        try:
            # 1. Date Generale Meci
            liga = row[0]
            data_ora = row[1]
            gazde = row[2]
            oaspeti = row[3]
            nume_meci = f"{gazde} vs {oaspeti}"
            
            # 2. Istoric meciuri (Ultimele elemente pentru siguranță)
            home_played = int(row[-3]) if row[-3].isdigit() else 0
            away_played = int(row[-2]) if row[-2].isdigit() else 0
            
            # FILTRU DE AUR: Dacă nu au minim 6 meciuri jucate în sezon, e la ghici. Îl tăiem!
            if home_played < 6 or away_played < 6:
                continue
                
            # 3. Extragere Cote Corecte conform tabelelor tale:
            # col20 (U) = Cota 1 | col23 (X) = Cota 1X | col25 (AA) = Cota X2
            cota_1 = float(row[19]) if row[19].replace('.', '', 1).isdigit() else 0.0
            cota_2 = float(row[21]) if row[21].replace('.', '', 1).isdigit() else 0.0
            cota_1x = float(row[22]) if row[22].replace('.', '', 1).isdigit() else 1.25
            cota_x2 = float(row[24]) if row[24].replace('.', '', 1).isdigit() else 1.25
            
            # MAPPING COLOANE SOLICITATE DE TINE:
            # În indexarea Python de la 0, col44 (AR) = index 43, col46 (AT) = index 45
            cota_peste_2_5 = float(row[43]) if row[43].replace('.', '', 1).isdigit() else 0.0  # Coloana AR
            cota_peste_3_5 = float(row[45]) if row[45].replace('.', '', 1).isdigit() else 0.0  # Coloana AT

            # Determinăm cine e echipa favorită în meci
            if cota_1 > 1.01 and cota_1 < cota_2:
                sansa_dubla_favorit = "1X"
                cota_sd = cota_1x
            else:
                sansa_dubla_favorit = "X2"
                cota_sd = cota_x2

            # --- STRATEGIA 1: BILET COMBO (Siguranță 95%) ---
            # Căutăm cote de siguranță la șansă dublă sau meciuri clare de peste 1.5 goluri
            if 1.18 <= cota_sd <= 1.45:
                selectii_combo.append({
                    "meci": nume_meci, "info": f"{data_ora} | {liga}",
                    "pariu": f"{sansa_dubla_favorit} & Peste 1.5 Goluri", "cota": cota_sd
                })

            # --- STRATEGIA 2: BILET ECHILIBRAT (Profit din Coloana AR -> Peste 2.5) ---
            # Dacă cota la Peste 2.5 din coloana AR este într-o zonă profitabilă (ex: 1.50 - 2.15)
            if 1.50 <= cota_peste_2_5 <= 2.15:
                selectii_echilibrat.append({
                    "meci": nume_meci, "info": f"{data_ora} | {liga}",
                    "pariu": "Peste 2.5 Goluri (AR)", "cota": cota_peste_2_5
                })

            # --- STRATEGIA 3: BILET BOMBĂ (Cote Mari din Coloana AT -> Peste 3.5) ---
            # Vânăm cotele mari de peste 3.5 goluri (coloana AT) doar la meciurile cu potențial uriaș
            if cota_peste_3_5 >= 2.20:
                selectii_bomba.append({
                    "meci": nume_meci, "info": f"{data_ora} | {liga}",
                    "pariu": "Peste 3.5 Goluri (AT)", "cota": cota_peste_3_5
                })

        except Exception:
            continue

# 📊 CONFIGURARE PANEL VIZUAL PE 3 COLOANE (STIL PROGRAM44)
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📋 1. Bilet Combo (Sigur)")
    cota_combo = 1.0
    for s in selectii_combo[:6]:  # Limităm la 6 cele mai bune meciuri
        cota_combo *= s["cota"]
        
    st.markdown(f"### Cotă Totală: `{cota_combo:.2f}`")
    st.caption("🎯 Strategia de rulaj: Șanse duble și goluri minime.")
    st.markdown("---")
    
    for s in selectii_combo[:6]:
        st.markdown(f"🟢 **{s['cota']:.2f}** | {s['meci']} ➡️ `{s['pariu']}`")
        
    if selectii_combo:
        st.warning(f"💵 Miza recomandată: **50 RON**\n\n💰 Câștig Potențial: **{50 * cota_combo:.2f} RON**")
    else:
        st.info("Fără selecții Combo sigure în acest moment.")

with col2:
    st.subheader("⚖️ 2. Bilet Echilibrat (AR)")
    cota_echilibrat = 1.0
    for s in selectii_echilibrat[:4]:  # 4 meciuri cu Peste 2.5 goluri sunt ideale
        cota_echilibrat *= s["cota"]
        
    st.markdown(f"### Cotă Totală: `{cota_echilibrat:.2f}`")
    st.caption("⚽ Strategia de bază: Peste 2.5 goluri extrase curat din coloana AR.")
    st.markdown("---")
    
    for s in selectii_echilibrat[:4]:
        st.markdown(f"🟡 **{s['cota']:.2f}** | {s['meci']} ➡️ `{s['pariu']}`")
        
    if selectii_echilibrat:
        st.success(f"💵 Miza recomandată: **30 RON**\n\n💰 Câștig Potențial: **{30 * cota_echilibrat:.2f} RON**")
    else:
        st.info("Niciun meci nu are o cotă stabilă de Peste 2.5 în coloana AR.")

with col3:
    st.subheader("💣 3. Bilet Cote Mari (AT)")
    cota_bomba = 1.0
    for s in selectii_bomba[:3]:  # Maxim 3 „bombe” pe bilet ca să nu stricăm șansele
        cota_bomba *= s["cota"]
        
    st.markdown(f"### Cotă Totală: `{cota_bomba:.2f}`")
    st.caption("🚀 Strategia speculativă: Peste 3.5 goluri din coloana AT la meciuri spectacol.")
    st.markdown("---")
    
    for s in selectii_bomba[:3]:
        st.markdown(f"🔥 **{s['cota']:.2f}** | {s['meci']} ➡️ `{s['pariu']}`")
        
    if selectii_bomba:
        st.error(f"💵 Miza recomandată: **10 RON**\n\n💰 Câștig Potențial: **{10 * cota_bomba:.2f} RON**")
    else:
        st.info("Niciun meci nu are o cotă destul de mare de Peste 3.5 în coloana AT.")
