# program33.py
import streamlit as st
import json
import math
from datetime import datetime

st.set_page_config(page_title="BetMachine Pro - Program33 Rapid", page_icon="🎯", layout="wide")

# ─────────────────────────────────────────────
# 1. Citire scores24.json (generat de scraper)
# ─────────────────────────────────────────────
@st.cache_data
def load_scores24():
    with open("scores24.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ─────────────────────────────────────────────
# 2. Motor Poisson simplu
# ─────────────────────────────────────────────
def poisson_prob(lam, k):
    if lam <= 0:
        return 0.0
    return (lam**k * math.exp(-lam)) / math.factorial(k)

def calculeaza_prob():
    # fără xG, folosim valori neutre
    lam_h = 1.3
    lam_a = 1.1

    p1 = px = p2 = 0.0
    p_gg = 0.0
    p_o25 = 0.0

    for i in range(7):
        for j in range(7):
            p = poisson_prob(lam_h, i) * poisson_prob(lam_a, j)
            if i > j:
                p1 += p
            elif i == j:
                px += p
            else:
                p2 += p
            if i > 0 and j > 0:
                p_gg += p
            if i + j > 2:
                p_o25 += p

    total = p1 + px + p2
    if total == 0:
        p1, px, p2 = 0.38, 0.28, 0.34
    else:
        p1, px, p2 = p1 / total, px / total, p2 / total

    return {
        "p1": round(p1, 3),
        "px": round(px, 3),
        "p2": round(p2, 3),
        "p_gg": round(p_gg, 3),
        "p_o25": round(p_o25, 3),
        "lam_h": round(lam_h, 2),
        "lam_a": round(lam_a, 2),
    }

def prob_to_cota(prob, marja=0.07):
    if prob <= 0.01:
        return 50.0
    return round(1 / (prob * (1 + marja)), 2)

# ─────────────────────────────────────────────
# 3. Asamblare bilete
# ─────────────────────────────────────────────
def asambleaza_bilete(meciuri):
    bilet_sigur = []
    bilet_combo = []
    bilet_bomba = []
    cota_s = cota_c = cota_b = 1.0

    for m in meciuri:
        p = m["prob"]
        c1 = prob_to_cota(p["p1"])
        cx = prob_to_cota(p["px"])
        c2 = prob_to_cota(p["p2"])
        c1x = prob_to_cota(p["p1"] + p["px"])
        cx2 = prob_to_cota(p["px"] + p["p2"])
        cgg = prob_to_cota(p["p_gg"])
        co25 = prob_to_cota(p["p_o25"])

        prefix = f"{m['league']} | {m['home']} vs {m['away']}"

        # SIGUR
        if cota_s < 20.0:
            if p["p1"] + p["px"] >= 0.60 and 1.20 <= c1x <= 1.70:
                bilet_sigur.append({"text": f"{prefix} ➜ 1X", "cota": c1x})
                cota_s *= c1x
            elif p["px"] + p["p2"] >= 0.60 and 1.20 <= cx2 <= 1.70:
                bilet_sigur.append({"text": f"{prefix} ➜ X2", "cota": cx2})
                cota_s *= cx2
            elif p["p_o25"] >= 0.58 and 1.25 <= co25 <= 1.75:
                bilet_sigur.append({"text": f"{prefix} ➜ Peste 2.5", "cota": co25})
                cota_s *= co25
            elif p["p1"] >= 0.52 and 1.25 <= c1 <= 1.80:
                bilet_sigur.append({"text": f"{prefix} ➜ 1", "cota": c1})
                cota_s *= c1

        # COMBO
        if len(bilet_combo) < 4 and cota_c < 15.0:
            if p["p1"] >= 0.44 and 1.55 <= c1 <= 3.20:
                bilet_combo.append({"text": f"{prefix} ➜ 1", "cota": c1})
                cota_c *= c1
            elif p["p2"] >= 0.44 and 1.55 <= c2 <= 3.20:
                bilet_combo.append({"text": f"{prefix} ➜ 2", "cota": c2})
                cota_c *= c2
            elif p["p_gg"] >= 0.50 and 1.55 <= cgg <= 2.50:
                bilet_combo.append({"text": f"{prefix} ➜ GG", "cota": cgg})
                cota_c *= cgg

        # BOMBĂ
        if len(bilet_bomba) < 3:
            if c2 >= 3.00 and p["p2"] >= 0.30:
                bilet_bomba.append({"text": f"{prefix} ➜ 2 (surpriză)", "cota": c2})
                cota_b *= c2
            elif c1 >= 3.00 and p["p1"] >= 0.30:
                bilet_bomba.append({"text": f"{prefix} ➜ 1 (surpriză)", "cota": c1})
                cota_b *= c1
            elif cgg >= 3.00 and p["p_gg"] >= 0.38:
                bilet_bomba.append({"text": f"{prefix} ➜ GG cotă mare", "cota": cgg})
                cota_b *= cgg

    return {
        "sigur": {"selectii": bilet_sigur, "cota": round(cota_s, 2)},
        "combo": {"selectii": bilet_combo, "cota": round(cota_c, 2)},
        "bomba": {"selectii": bilet_bomba, "cota": round(cota_b, 2)},
    }

# ─────────────────────────────────────────────
# 4. UI Streamlit
# ─────────────────────────────────────────────
st.title("🎯 BetMachine Pro - Program33 Rapid (scores24.json)")
st.caption(f"Data: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

try:
    raw = load_scores24()
except FileNotFoundError:
    st.error("Nu am găsit scores24.json în repo. Generează-l cu scraperul și urcă-l în GitHub.")
    st.stop()

meciuri = []
for m in raw:
    prob = calculeaza_prob()
    meciuri.append({
        "id": m.get("id"),
        "league": m.get("league", "Unknown"),
        "home": m.get("home"),
        "away": m.get("away"),
        "score": m.get("score", "N/A"),
        "prob": prob,
    })

st.success(f"Meciuri încărcate din scores24.json: {len(meciuri)}")

bilete = asambleaza_bilete(meciuri)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Bilet SIGUR")
    cs = bilete["sigur"]["cota"]
    st.metric("Cotă totală", cs)
    for ev in bilete["sigur"]["selectii"]:
        st.markdown(f"✔️ `{ev['cota']}` {ev['text']}")
    st.caption(f"5 RON ➜ {round(5 * cs, 2)} RON")

with col2:
    st.subheader("Bilet COMBO")
    cc = bilete["combo"]["cota"]
    st.metric("Cotă totală", cc)
    for ev in bilete["combo"]["selectii"]:
        st.markdown(f"✔️ `{ev['cota']}` {ev['text']}")
    st.caption(f"5 RON ➜ {round(5 * cc, 2)} RON")

with col3:
    st.subheader("Bilet BOMBĂ")
    cb = bilete["bomba"]["cota"]
    st.metric("Cotă totală", cb)
    for ev in bilete["bomba"]["selectii"]:
        st.markdown(f"✔️ `{ev['cota']}` {ev['text']}")
    st.caption(f"2 RON ➜ {round(2 * cb, 2)} RON")

st.markdown("---")
st.subheader("📋 Toate meciurile din scores24.json")

for m in meciuri:
    with st.expander(f"{m['league']} | {m['home']} vs {m['away']} | scor: {m['score']}"):
        p = m["prob"]
        c1 = prob_to_cota(p["p1"])
        cx = prob_to_cota(p["px"])
        c2 = prob_to_cota(p["p2"])
        cgg = prob_to_cota(p["p_gg"])
        co25 = prob_to_cota(p["p_o25"])
        c1_, c2_, c3_, c4_, c5_ = st.columns(5)
        c1_.metric("1", c1, f"{int(p['p1']*100)}%")
        c2_.metric("X", cx, f"{int(p['px']*100)}%")
        c3_.metric("2", c2, f"{int(p['p2']*100)}%")
        c4_.metric("GG", cgg, f"{int(p['p_gg']*100)}%")
        c5_.metric("O2.5", co25, f"{int(p['p_o25']*100)}%")
        st.caption(f"λ gazdă: {p['lam_h']} | λ oaspeți: {p['lam_a']}")
