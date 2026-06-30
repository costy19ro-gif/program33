# program33.py
import streamlit as st
import json
import math
from datetime import datetime

st.set_page_config(page_title="🎯 BetMachine Pro - Program33 Rapid", page_icon="🎯", layout="wide")

# ─────────────────────────────────────────────
# 1. Citire scores24.json
# ─────────────────────────────────────────────
@st.cache_data
def load_scores24():
    with open("scores24.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ─────────────────────────────────────────────
# 2. Motor Poisson + piețe extinse
# ─────────────────────────────────────────────
def poisson_prob(lam, k):
    if lam <= 0:
        return 0.0
    return (lam**k * math.exp(-lam)) / math.factorial(k)

def calculeaza_piete():
    # λ full match (simplu, neutru)
    lam_h = 1.3
    lam_a = 1.1

    # λ prima repriză (aprox. 55% din total)
    lam_h_h1 = lam_h * 0.55
    lam_a_h1 = lam_a * 0.55

    p1 = px = p2 = 0.0
    p_gg = 0.0
    p_o15 = 0.0
    p_o25 = 0.0
    p_h_scores = 0.0
    p_a_scores = 0.0

    for i in range(7):
        for j in range(7):
            p = poisson_prob(lam_h, i) * poisson_prob(lam_a, j)
            # 1X2
            if i > j:
                p1 += p
            elif i == j:
                px += p
            else:
                p2 += p
            # GG
            if i > 0 and j > 0:
                p_gg += p
            # Over 1.5
            if i + j > 1:
                p_o15 += p
            # Over 2.5
            if i + j > 2:
                p_o25 += p
            # Marchează gazdele
            if i > 0:
                p_h_scores += p
            # Marchează oaspeții
            if j > 0:
                p_a_scores += p

    # Gol în prima repriză (oricare echipă)
    p_h1_goal = 1.0 - (
        poisson_prob(lam_h_h1, 0) * poisson_prob(lam_a_h1, 0)
    )

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
        "p_o15": round(p_o15, 3),
        "p_o25": round(p_o25, 3),
        "p_h_scores": round(p_h_scores, 3),
        "p_a_scores": round(p_a_scores, 3),
        "p_h1_goal": round(p_h1_goal, 3),
        "lam_h": round(lam_h, 2),
        "lam_a": round(lam_a, 2),
    }

def prob_to_cota(prob, marja=0.07):
    if prob <= 0.01:
        return 50.0
    return round(1 / (prob * (1 + marja)), 2)

# ─────────────────────────────────────────────
# 3. Pregătire meciuri + piețe (predictie pură)
# ─────────────────────────────────────────────
def pregateste_meciuri(raw):
    meciuri = []
    for m in raw:
        p = calculeaza_piete()

        c_1 = prob_to_cota(p["p1"])
        c_x = prob_to_cota(p["px"])
        c_2 = prob_to_cota(p["p2"])
        c_1x = prob_to_cota(p["p1"] + p["px"])
        c_x2 = prob_to_cota(p["px"] + p["p2"])
        c_gg = prob_to_cota(p["p_gg"])
        c_o15 = prob_to_cota(p["p_o15"])
        c_o25 = prob_to_cota(p["p_o25"])
        c_h1_goal = prob_to_cota(p["p_h1_goal"])
        c_h_scores = prob_to_cota(p["p_h_scores"])
        c_a_scores = prob_to_cota(p["p_a_scores"])
        c_gg_o25 = prob_to_cota(p["p_gg"] * p["p_o25"])
        c_1_gg = prob_to_cota(p["p1"] * p["p_gg"])

        meciuri.append({
            "id": m.get("id"),
            "league": m.get("league", "Unknown"),
            "home": m.get("home"),
            "away": m.get("away"),
            "score": m.get("score", "N/A"),
            "p": p,
            "c": {
                "H1_goal": c_h1_goal,
                "O1_5": c_o15,
                "O2_5": c_o25,
                "1X": c_1x,
                "X2": c_x2,
                "1": c_1,
                "X": c_x,
                "2": c_2,
                "GG": c_gg,
                "GG_O2_5": c_gg_o25,
                "1_GG": c_1_gg,
                "H_scores": c_h_scores,
                "A_scores": c_a_scores,
            }
        })
    return meciuri

# ─────────────────────────────────────────────
# 4. UI Streamlit – tabel + carduri
# ─────────────────────────────────────────────
st.title("🎯 BetMachine Pro - Program33 Rapid (taca‑paca, predictie pură)")
st.caption(f"Data: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

try:
    raw = load_scores24()
except FileNotFoundError:
    st.error("Nu am găsit scores24.json în repo. Generează-l și urcă-l în GitHub.")
    st.stop()

meciuri_all = pregateste_meciuri(raw)

st.success(f"Meciuri încărcate din scores24.json: {len(meciuri_all)}")

# SELECTĂM DIRECT PRIMELE 21 MECIURI – PREDICTIE PURĂ
meciuri = meciuri_all[:21]

st.markdown("## 🧱 Tabel TACA‑PACA (21 meciuri × piețe)")

tabel_data = []
for m in meciuri:
    row = {
        "Liga": m["league"],
        "Meci": f"{m['home']} vs {m['away']}",
        "H1 gol": m["c"]["H1_goal"],
        "+1.5": m["c"]["O1_5"],
        "+2.5": m["c"]["O2_5"],
        "1X": m["c"]["1X"],
        "X2": m["c"]["X2"],
        "1": m["c"]["1"],
        "X": m["c"]["X"],
        "2": m["c"]["2"],
        "GG": m["c"]["GG"],
        "GG+2.5": m["c"]["GG_O2_5"],
        "1&GG": m["c"]["1_GG"],
        "HG": m["c"]["H_scores"],
        "HO": m["c"]["A_scores"],
    }
    tabel_data.append(row)

st.dataframe(tabel_data, use_container_width=True)

st.markdown("---")
st.markdown("## 🧩 Carduri pe meci (piețe detaliate)")

for m in meciuri:
    with st.expander(f"{m['league']} | {m['home']} vs {m['away']} | scor: {m['score']}"):
        p = m["p"]
        c = m["c"]

        st.caption(f"λ gazde: {p['lam_h']} | λ oaspeți: {p['lam_a']}")

        col_h1, col_o, col_1x2 = st.columns(3)

        with col_h1:
            st.markdown("### ⏱ Prima repriză")
            st.metric("Gol în H1", c["H1_goal"], f"{int(p['p_h1_goal']*100)}%")
            st.metric("+1.5 goluri", c["O1_5"], f"{int(p['p_o15']*100)}%")
            st.metric("+2.5 goluri", c["O2_5"], f"{int(p['p_o25']*100)}%")

        with col_o:
            st.markdown("### 🎯 Goluri & GG")
            st.metric("GG", c["GG"], f"{int(p['p_gg']*100)}%")
            st.metric("GG + 2.5", c["GG_O2_5"])
            st.metric("1 & GG", c["1_GG"])
            st.metric("Marchează gazdele", c["H_scores"], f"{int(p['p_h_scores']*100)}%")
            st.metric("Marchează oaspeții", c["A_scores"], f"{int(p['p_a_scores']*100)}%")

        with col_1x2:
            st.markdown("### 🧱 1X2")
            st.metric("1X", c["1X"], f"{int((p['p1']+p['px'])*100)}%")
            st.metric("X2", c["X2"], f"{int((p['px']+p['p2'])*100)}%")
            st.metric("1", c["1"], f"{int(p['p1']*100)}%")
            st.metric("X", c["X"], f"{int(p['px']*100)}%")
            st.metric("2", c["2"], f"{int(p['p2']*100)}%")
