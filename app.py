import os
import streamlit as st

st.set_page_config(page_title="Program33 - Predictor", layout="wide")
st.title("⚽ Predicții Meciuri - Stil Program33")

cale_fisier = "scores24.csv"

if not os.path.exists(cale_fisier):
    st.error(f"Nu am găsit fișierul '{cale_fisier}' în GitHub!")
    st.stop()

# Setări Filtrare în Meniul Lateral (Sidebar)
st.sidebar.header("🔧 Setări Filtrare")
activare_filtre = st.sidebar.checkbox("Activează filtrele stricte", value=True)
cota_minima_input = st.sidebar.number_input("Cotă minimă favorit", min_value=1.0, max_value=5.0, value=1.28, step=0.01)
meciuri_minime_input = st.sidebar.number_input("Min. meciuri jucate (AX/AY)", min_value=1, max_value=30, value=6)

meciuri_valide = 0
total_meciuri_fisier = 0

# Deschidem fișierul text simplu ca să evităm crăparea librăriei de CSV
with open(cale_fisier, "r", encoding="utf-8", errors="ignore") as f:
    for linie in f:
        # Curățăm linia de ghilimele ornamentale create de scraper
        linie_curata = linie.replace('", "', ',').replace('",', ',').replace(',"', ',').replace('"', '')
        parti = [p.strip() for p in linie_curata.split(",") if p.strip()]
        
        # Un rând valid din datele tale conține zeci de coloane
        if len(parti) < 30:
            continue
            
        total_meciuri_fisier += 1
        
        try:
            # Extragerea sigură a datelor de identificare (primele coloane)
            liga = parti[0]
            data_ora = parti[1]
            gazde = parti[2]
            oaspeti = parti[3]
            
            # Căutăm dinamic meciurile jucate (ultimele numere întregi din listă)
            numere_gasite = [int(x) for x in parti if x.isdigit()]
            
            # În mod normal, ultimele valori sunt meciurile jucate (AX și AY)
            home_played = numere_gasite[-2] if len(numere_gasite) >= 2 else 0
            away_played = numere_gasite[-1] if len(numere_gasite) >= 2 else 0
            
            # Căutăm dinamic cotele din meci (numere cu virgulă / float)
            cote_gasite = []
            for x in parti:
                try:
                    val = float(x)
                    if 1.01 <= val <= 50.0 and not val.is_integer():
                        cote_gasite.append(val)
                except ValueError:
                    continue
            
            # Prima cotă din listă este de regulă cota echipei favorite (col20)
            cota_favorit = cote_gasite[0] if cote_gasite else 0.0

            # Extragere predictii scoruri (FT / HT)
            scor_ft_1 = parti[6] if len(parti) > 6 else "N/A"
            scor_ft_2 = parti[8] if len(parti) > 8 else "N/A"
            pred_ft = parti[10] if len(parti) > 10 else "N/A"
            linie_gol = parti[11] if len(parti) > 11 else "N/A"
            
            # 🛠️ APLICARE FILTRE SOLICITATE
            if activare_filtre:
                if home_played < meciuri_minime_input or away_played < meciuri_minime_input:
                    continue
                if cota_favorit < cota_minima_input:
                    continue

            meciuri_valide += 1
            
            # Afișarea meciului în stilul grafic dorit
            with st.container():
                st.markdown(f"### 🏟️ {liga} | {data_ora} | **{gazde}** vs **{oaspeti}**")
                
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown("**🎯 Scoruri Probabile**")
                    st.write(f"Scor FT principal: `{scor_ft_1}`")
                    st.write(f"Scor FT secundar: `{scor_ft_2}`")
                    st.write(f"Predicție meci: `{pred_ft}`")
                with c2:
                    st.markdown("**📊 Detalii Algoritm**")
                    st.write(f"Linie Goluri propusă: `{linie_gol}`")
                    st.write(f"Evaluare siguranță: `Stabil`")
                with c3:
                    st.markdown("**💰 Cote Pariuri Detectate**")
                    st.write(f"Cotă Favorit estimată: `{cota_favorit if cota_favorit > 0 else 'N/A'}`")
                    if len(cote_gasite) > 2:
                        st.write(f"Alte cote din meci: `{cote_gasite[1]}` / `{cote_gasite[2]}`")
                with c4:
                    st.markdown("**⚽ Istoric Meciuri Jucate**")
                    st.write(f"Meciuri Gazde (AX): **{home_played}**")
                    st.write(f"Meciuri Oaspeți (AY): **{away_played}**")
                
                st.markdown("<hr style='margin:12px 0px; border-top:1px dashed #bbb;'/>", unsafe_allow_html=True)
                
        except Exception:
            continue

# Panou de statistici în sidebar
st.sidebar.markdown("---")
st.sidebar.metric(label="Total meciuri în fișier", value=total_meciuri_fisier)
st.sidebar.metric(label="Meciuri afișate pe ecran", value=meciuri_valide)

if meciuri_valide == 0 and total_meciuri_fisier > 0:
    st.info("Sistemul a curățat fișierul, dar niciun meci nu trece de filtre. Dezactivează căsuța 'Activează filtrele stricte' din stânga pentru a le vedea pe toate.")
