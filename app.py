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
        row = [c.strip() for c in row if c is not None]
        if len(row) < 45:
            continue
            
        try:
            # Extragere date meci
            liga = row[0]
            data_ora = row[1]
            gazde = row[2]
            oaspeti = row[3]
            
            # Verificare meciuri jucate din coloanele de la final (AW/AX și AX/AY)
            home_played = int(row[-3]) if row[-3].isdigit() else 0
            away_played = int(row[-2]) if row[-2].isdigit() else 0
            
            # Filtru de bază obligatoriu: minim 6 meciuri jucate
            if home_played < 6 or away_played < 6:
                continue
                
            # Extragere predictie principală text (col11) și linie goluri (col12)
            predictie_1x2 = row[10] 
            linie_goluri = row[11]
            
            # Extragere cote numerice (col20 = Cota 1, col21 = Cota X, col22 = Cota 2)
            cota_1 = float(row[19]) if row[19].replace('.', '', 1).isdigit() else 1.0
            cota_x = float(row[20]) if row[20].replace('.', '', 1).isdigit() else 1.0
            cota_2 = float(row[21]) if row[21].replace('.', '', 1).isdigit() else 1.0
            cota_1x = float(row[22]) if row[22].replace('.', '', 1).isdigit() else 1.0
            cota_x2 = float(row[24]) if row[24].replace('.', '', 1).isdigit() else 1.0

            # SPRING LOGIC: Identificăm favoritul și tipul de pariu optim
            if cota_1 > 1.01 and cota_1 < cota_2:
                favorit = "1"
                cota_favorit = cota_1
                sansa_dubla = "1X"
                cota_sd = cota_1x
            else:
                favorit = "2"
                cota_favorit = cota_2
                sansa_dubla = "X2"
                cota_sd = cota_x2

            nume_meci = f"{gazde} vs {oaspeti}"

            # 1. CATEGORIA COMBO (Double Chance / Peste 1.5 - Cote între 1.15 și 1.45)
            if 1.15 <= cota_sd <= 1.45:
                selectii_combo.append({
                    "meci": nume_meci, "detalii": f"{data_ora} | {liga}",
                    "pariu": f"{sansa_dubla} sau Peste 1.5 Goluri", "cota": cota_sd
                })
            elif 1.15 <= cota_favorit <= 1.45:
                selectii_combo.append({
                    "meci": nume_meci, "detalii": f"{data_ora} | {liga}",
                    "pariu": f"Victorie Favorit ({favorit})", "cota": cota_favorit
                })

            # 2. CATEGORIA ECHILIBRAT (1 / 2 / GG - Cote între 1.45 și 2.20)
            if 1.45 < cota_favorit <= 2.20:
                selectii_echilibrat.append({
                    "meci": nume_meci, "detalii": f"{data_ora} | {liga}",
                    "pariu": f"Victorie ({favorit})", "cota": cota_favorit
                })

            # 3. CATEGORIA COTE MARI (Cote peste 2.20)
            if cota_favorit > 2.20:
                selectii_mari.append({
                    "meci": nume_meci, "detalii": f"{data_ora} | {liga}",
                    "pariu": f"Solist ({favorit}) / Scor Corect", "cota": cota_favorit
                })

        except Exception:
            continue

# 📊 AFISARE PE 3 COLOANE SIMETRICE CA IN PROGRAM44
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📋 Bilet Combo")
    cota_totala_combo = 1.0
    for s in selectii_combo[:8]:  # Maxim 8 meciuri pe bilet
        cota_totala_combo *= s["cota"]
    
    st.markdown(f"### Cota Totală: `{cota_totala_combo:.2f}`")
    st.caption("✔️ Pariuri de tip Șansă Dublă / Total Goluri sigure")
    st.markdown("---")
    
    for s in selectii_combo[:8]:
        st.markdown(f"🔹 **{s['cota']:.2f}** ({s['detalii']}) **{s['meci']}** ➡️ `{s['pariu']}`")
    
    if selectii_combo:
        st.warning(f"💰 Miza: 20 RON ➡️ Câștig potențial: {20 * cota_totala_combo:.1f} RON")

with col2:
    st.subheader("⚖️ Bilet Echilibrat")
    cota_totala_echilibrat = 1.0
    for s in selectii_echilibrat[:5]:  # Maxim 5 meciuri pe bilet
        cota_totala_echilibrat *= s["cota"]
        
    st.markdown(f"### Cota Totală: `{cota_totala_echilibrat:.2f}`")
    st.caption("⚠️ 3-5 Selecții de soliști sau GG-uri competitive")
    st.markdown("---")
    
    for s in selectii_echilibrat[:5]:
        st.markdown(f"🔸 **{s['cota']:.2f}** ({s['detalii']}) **{s['meci']}** ➡️ `{s['pariu']}`")
        
    if selectii_echilibrat:
        st.success(f"💰 Miza: 10 RON ➡️ Câștig potențial: {10 * cota_totala_echilibrat:.1f} RON")

with col3:
    st.subheader("💣 Bilet Cote Mari")
    cota_totala_mari = 1.0
    for s in selectii_mari[:4]:  # Maxim 4 meciuri pe bilet
        cota_totala_mari *= s["cota"]
        
    st.markdown(f"### Cota Totală: `{cota_totala_mari:.2f}`")
    st.caption("🚀 Fiecare selecție individuală are cotă mare")
    st.markdown("---")
    
    for s in selectii_mari[:4]:
        st.markdown(f"❌ **{s['cota']:.2f}** ({s['detalii']}) **{s['meci']}** ➡️ `{s['pariu']}`")
        
    if not selectii_mari:
        st.info("Nu s-au găsit selecții cu cotă ridicată în acest moment.")
    else:
        st.error(f"💰 Miza: 5 RON ➡️ Câștig potențial: {5 * cota_totala_mari:.1f} RON")
