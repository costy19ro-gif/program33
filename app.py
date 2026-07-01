import csv
import os
import streamlit as st

st.set_page_config(page_title="Program33 - Predictor", layout="wide")
st.title("⚽ Predicții Meciuri - Stil Program33")

cale_fisier = "scores24.csv"

if not os.path.exists(cale_fisier):
    st.error(f"Nu am găsit fișierul '{cale_fisier}' în GitHub!")
    st.stop()

# Setări Filtrare în Meniul Lateral
st.sidebar.header("🔧 Setări Filtrare")
activare_filtre = st.sidebar.checkbox("Activează filtrele stricte", value=True)
cota_minima_input = st.sidebar.number_input("Cotă minimă favorit", min_value=1.0, max_value=5.0, value=1.28, step=0.01)
meciuri_minime_input = st.sidebar.number_input("Min. meciuri jucate", min_value=1, max_value=30, value=6)

meciuri_valide = 0
total_meciuri_fisier = 0

with open(cale_fisier, "r", encoding="utf-8", errors="ignore") as f:
    cititor_csv = csv.reader(f, delimiter=',', quotechar='"')
    
    for row in cititor_csv:
        # Curățăm elementele goale de la sfârșitul listei
        row = [celula.strip() for celula in row if celula is not None]
        if not row or len(row) < 40:
            continue
            
        total_meciuri_fisier += 1
        
        try:
            # 📌 IDENTIFICARE DE LA COADĂ LA CAPĂT (Evită erorile de decaleaj din cauza virgulelor)
            # Concret, ultimele coloane din text sunt mereu statisticile HT și meciurile jucate
            home_played_text = row[-3]  # Coloana AW/AX din tabel (HOME Played)
            away_played_text = row[-2]  # Coloana AX/AY din tabel (AWAY Played)
            
            home_played = int(home_played_text) if home_played_text.isdigit() else 0
            away_played = int(away_played_text) if away_played_text.isdigit() else 0
            
            # Datele generale de identificare ale meciului
            ligă = row[0]
            dată_oră = row[1]
            gazde = row[2]
            oaspeți = row[3]
            
            # Scoruri Probabile Full Time (FT)
            scor_ft_1 = row[6]   # col7
            prob_ft_1 = row[7]   # col8
            scor_ft_2 = row[8]   # col9
            prob_ft_2 = row[9]   # col10
            pred_ft = row[10]    # col11
            
            # Probabilități 1X2 Full Time
            prob_1_ft = row[13]  # col14
            prob_x_ft = row[14]  # col15
            prob_2_ft = row[15]  # col16
            
            # Cote Pariuri 1X2 Piața A
            cota_1_A = row[19]   # col20
            cota_x_A = row[20]   # col21
            cota_2_A = row[21]   # col22
            cota_x2_A = row[24]  # col25
            
            # Scoruri Probabile Half Time (HT)
            scor_ht_1 = row[42]  # col43
            prob_ht_1 = row[43]  # col44
            scor_ht_2 = row[44]  # col45
            pred_ht = row[46]    # col47
            
            # Extragere valoare cotă pentru filtru
            try:
                val_cota = float(cota_1_A) if cota_1_A else 0.0
            except ValueError:
                val_cota = 0.0

            # 🛠️ APLICARE FILTRE LOGICE
            if activare_filtre:
                # Filtrul 1: Să aibă minimum numărul de meciuri cerut (AX și AY)
                if home_played < meciuri_minime_input or away_played < meciuri_minime_input:
                    continue
                # Filtrul 2: Cota să fie mai mare sau egală cu cea selectată
                if val_cota < cota_minima_input:
                    continue

            meciuri_valide += 1
            
            # Generare interfață vizuală compactă pentru meci
            with st.container():
                st.markdown(f"### 🏟️ {ligă} | {dată_oră} | **{gazde}** vs **{oaspeți}**")
                
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown("**🎯 Scoruri Probabile**")
                    st.write(f"Scor HT principal: `{scor_ht_1}` (Prob: `{prob_ht_1}`)")
                    st.write(f"Scor HT secundar: `{scor_ht_2}`")
                    st.write(f"Scor FT principal: `{scor_ft_1}` (Prob: `{prob_ft_1}`)")
                    st.write(f"Scor FT secundar: `{scor_ft_2}` (Prob: `{prob_ft_2}`)")
                with c2:
                    st.markdown("**📊 Probabilități Procentuale**")
                    st.write(f"FT (1 / X / 2): `{prob_1_ft}` / `{prob_x_ft}` / `{prob_2_ft}`")
                    st.write(f"Predicție Generală: HT: `{pred_ht}` | FT: `{pred_ft}`")
                with c3:
                    st.markdown("**💰 Cote Pariuri (Piața A)**")
                    st.write(f"1: `{cota_1_A}` | X: `{cota_x_A}` | 2: `{cota_2_A}`")
                    st.write(f"Șansă Dublă X2: `{cota_x2_A}`")
                with c4:
                    st.markdown("**⚽ Istoric Meciuri Jucate**")
                    st.write(f"Meciuri Gazde (Acasă): **{home_played}**")
                    st.write(f"Meciuri Oaspeți (Deplasare): **{away_played}**")
                
                st.markdown("<hr style='margin:12px 0px; border-top:1px dashed #bbb;'/>", unsafe_allow_html=True)
                
        except Exception:
            continue

# Statistici finale în meniu
st.sidebar.markdown("---")
st.sidebar.metric(label="Total meciuri în CSV", value=total_meciuri_fisier)
st.sidebar.metric(label="Meciuri afișate", value=meciuri_valide)

if meciuri_valide == 0:
    st.info(f"Sistemul funcționează corect (Meciuri totale găsite: {total_meciuri_fisier}), dar niciunul nu respectă criteriile stricte de filtrare. Încearcă să debifezi căsuța 'Activează filtrele stricte' din meniul din stânga.")
