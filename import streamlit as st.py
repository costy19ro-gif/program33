# ─────────────────────────────────────────────
# 5. BILETE SIGUR / COMBO / BOMBĂ – generate automat
# ─────────────────────────────────────────────

st.markdown("---")
st.markdown("## 🎫 Bilete generate automat din predictii")

# Funcție utilă pentru calcul cotă totală
def cota_totala(lista_cote):
    total = 1.0
    for c in lista_cote:
        total *= c
    return round(total, 2)

# ─────────────────────────────────────────────
# BILET SIGUR
# ─────────────────────────────────────────────
if st.button("🎯 Generează Bilet SIGUR"):
    sigur = []
    for m in meciuri:
        c = m["c"]

        # cele mai sigure piețe (în ordinea corectă)
        sigur.append((f"{m['home']} vs {m['away']}", "1X", c["1X"]))
        sigur.append((f"{m['home']} vs {m['away']}", "H1 gol", c["H1_goal"]))
        sigur.append((f"{m['home']} vs {m['away']}", "HG", c["H_scores"]))

        if len(sigur) >= 10:
            break

    total = cota_totala([x[2] for x in sigur])

    st.subheader(f"🎯 Bilet SIGUR – Cotă totală: {total}")
    for meci, piata, cota in sigur:
        st.write(f"✔️ {meci} ➜ {piata} @ {cota}")

# ─────────────────────────────────────────────
# BILET COMBO
# ─────────────────────────────────────────────
if st.button("🔥 Generează Bilet COMBO"):
    combo = []
    for m in meciuri:
        c = m["c"]

        combo.append((f"{m['home']} vs {m['away']}", "GG", c["GG"]))
        combo.append((f"{m['home']} vs {m['away']}", "+2.5", c["O2_5"]))

        if len(combo) >= 6:
            break

    total = cota_totala([x[2] for x in combo])

    st.subheader(f"🔥 Bilet COMBO – Cotă totală: {total}")
    for meci, piata, cota in combo:
        st.write(f"⭐ {meci} ➜ {piata} @ {cota}")

# ─────────────────────────────────────────────
# BILET BOMBĂ
# ─────────────────────────────────────────────
if st.button("💣 Generează Bilet BOMBĂ"):
    bomba = []
    for m in meciuri:
        c = m["c"]

        bomba.append((f"{m['home']} vs {m['away']}", "GG + 2.5", c["GG_O2_5"]))
        bomba.append((f"{m['home']} vs {m['away']}", "1 & GG", c["1_GG"]))
        bomba.append((f"{m['home']} vs {m['away']}", "X", c["X"]))

        if len(bomba) >= 6:
            break

    total = cota_totala([x[2] for x in bomba])

    st.subheader(f"💣 Bilet BOMBĂ – Cotă totală: {total}")
    for meci, piata, cota in bomba:
        st.write(f"💥 {meci} ➜ {piata} @ {cota}")

