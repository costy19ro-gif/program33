import csv
import os
import streamlit as st

st.set_page_config(page_title="Program33 - Predictor", layout="wide")
st.title("⚽ Predicții Meciuri - Stil Program33")

cale_fisier = "scores24.csv"

if not os.path.exists(cale_fisier):
    st.error(f"Nu am găsit fișierul '{cale_fisier}' în GitHub!")
    st.stop()

# Opțiune în Sidebar pentru controlul filtrelor în timp real
st.sidebar.header("🔧 Setări Filtrare")
activare_filtre = st.sidebar.checkbox("Activează filtrele stricte", value=True)
cota_minima_input = st.sidebar.number_input("Cotă minimă favorit", min_value=1.0, max_value=5.0, value=1.28, step=0.01)
meciuri_minime_input = st.sidebar.number_input("Min. meciuri jucate (AX/AY)", min_value=1, max_value=30, value=6)

meciuri_valide = 0
total_meciuri_fisier = 0

with open(cale_fisier, "r", encoding="utf-8", errors="ignore") as f:
    # Cititorul inteligent de CSV care știe să ignore virgulele din interiorul ghilimelelor ","
    cititor_csv = csv.reader(f, delimiter=',', quotechar='"')
    
    for row in cititor_csv:
        if not row or len(row) < 55:
            continue
            
        total_meciuri_fisier += 1
        
        try:
            # Identificarea corectă a coloanelor pe baza indexului Python (care începe de la 0)
            # col1=0, col2=1 ... col20=19, col51=50, col52=51
            ligă = row[0]
            dată_oră = row[1]
            gazde = row[2]
            oaspeți = row[3]
            
            # Scoruri și predicții final meci (FT)
            scor_ft_1 = row[6]   # col7
            prob_ft_1 = row[7]   # col8
            scor_ft_2 = row[8]   # col9
            prob_ft_2 = row[9]   # col10
            pred_ft = row[10]    # col11
            linie_gol_ft = row[11] # col12
            
            prob_1_ft = row[13]  # col14
            prob_x_ft = row[14]  # col15
            prob_2_ft = row[15]  # col16
            
            # Cote 1X2 și Șansă Dublă Piața A
            cota_1_A = row[19]   # col20
            cota_x_A = row[20]   # col21
            cota_2_A = row[21]   # col22
            cota_1x_A = row[22]  # col23
            cota_12_A = row[23]  # col24
            cota_x2_A = row[24]  # col25
            
            # Cote Piața B
            cota_1_B = row[34]   # col35
            
            # Predicții Prima Repriză (HT) - extrase din ultimele coloane
            scor_ht_1 = row[42]   # col43
            prob_ht_1 = row[43]   # col44
            scor_ht_2 = row[44]   # col45
            pred_ht = row[46]     # col47
            prob_1_ht = row[48]   # col49
            prob_x_ht = row[49]   # col50
            
            # Statistici meciuri jucate (col51 și col52)
            meciuri_gazde_text = row[50].strip()
            meciuri_oaspeti_text = row[51].strip()
            
            home_played = int(meciuri_gazde_text) if meciuri_gazde_text.isdigit() else 0
            away_played = int(meciuri_oaspeti_text) if meciuri_oaspeti_text.isdigit() else 0
            
            # Extragere și curățare cote numerice
            try:
                val_cota_A = float(cota_1_A) if cota_1_A else 0.0
                val_cota_B = float(cota_1_B) if cota_1_B else 0.0
            except ValueError:
                val_cota_A, val_cota_B = 0.0, 0.0
                
            cota_maxima = max(val_cota_A, val_cota_B)

            # Logica de filtrare flexibilă
            if activare_filtre:
                if home_played < meciuri_minime_input or away_played < meciuri_minime_input:
                    continue
                if cota_maxima < cota_minima_input:
                    continue

            # Dacă trece de filtre sau filtrele sunt oprite, afișăm meciul
            meciuri_valide += 1
            
            with st.container():
                st.markdown(f"### 🏟️ {ligă} | {dată_oră} | **{gazde}** vs **{oaspeți}**")
                
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown("**🎯 Scoruri Probabile**")
                    st.write(f"Scor HT principal: `{scor_ht_1}` | Secundar: `{scor_ht_2}`")
                    st.write(f"Scor FT principal: `{scor_ft_1}` (Prob: `{prob_ft_1}`)")
                    st.write(f"Scor FT secundar: `{scor_ft_2}` (Prob: `{prob_ft_2}`)")
                with c2:
                    st.markdown("**📊 Probabilități Procentuale**")
                    st.write(f"HT (1 / X): `{prob_1_ht}` / `{prob_x_ht}`")
                    st.write(f"FT (1 / X / 2): `{prob_1_ft}` / `{prob_x_ft}` / `{prob_2_ft}`")
                    st.write(f"Predicție: HT: `{pred_ht}` | FT: `{pred_ft}`")
                with c3:
                    st.markdown("**💰 Cote Pariuri (Piața A)**")
                    st.write(f"1: `{cota_1_A}` | X: `{cota_x_A}` | 2: `{cota_2_A}`")
                    st.write(f"1X: `{cota_1x_A}` | 12: `{cota_12_A}` | X2: `{cota_x2_A}`")
                    st.write(f"Cota 1 Piața B: `{cota_1_B}`")
                with c4:
                    st.markdown("**⚽ Linii Goluri & Istoric**")
                    st.write(f"Linie Gol FT: `{linie_gol_ft}` | Sugestie: `{row[16]}`")
                    st.write(f"Meciuri Jucate: **{home_played}** Gazde / **{away_played}** Oaspeți")
                
                st.markdown("<hr style='margin:12px 0px; border-top:1px dashed #bbb;'/>", unsafe_allow_html=True)
                
        except Exception as e:
            continue

# Mesaje de stare în subsolul paginii
st.sidebar.markdown("---")
st.sidebar.metric(label="Total meciuri în CSV", value=total_meciuri_fisier)
st.sidebar.metric(label="Meciuri afișate", value=meciuri_valide)

if meciuri_valide == 0:
    st.info(f"Sistemul funcționează corect (Meciuri totale găsite: {total_meciuri_fisier}), dar niciunul nu respectă filtrele selectate. Încearcă să debifezi căsuța 'Activează filtrele stricte' din meniul din stânga.")
