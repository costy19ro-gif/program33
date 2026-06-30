import streamlit as st
import requests
from datetime import datetime, timedelta
import math

st.set_page_config(page_title="BetMachine Pro - Program 33", page_icon="🎯", layout="wide")

# ══════════════════════════════════════════════════════════
#  CONFIGURARE API — DOAR FOOTBALL-DATA.ORG
# ══════════════════════════════════════════════════════════
API_TOKEN   = "5c62dc102c364274ac4fc0ec7f33010a"
FD_BASE     = "https://api.football-data.org/v4"
FD_HEADERS  = {"X-Auth-Token": API_TOKEN}

# ══════════════════════════════════════════════════════════
#  FUNCȚII API — FOOTBALL-DATA.ORG
# ══════════════════════════════════════════════════════════
@st.cache_data(ttl=1800)
def get_fd_matches(comp_code):
    azi  = datetime.now().strftime("%Y-%m-%d")
    viit = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    try:
        url = f"{FD_BASE}/competitions/{comp_code}/matches"
        r   = requests.get(url, headers=FD_HEADERS,
                           params={"status": "SCHEDULED", "dateFrom": azi, "dateTo": viit},
                           timeout=8)
        if r.status_code == 200:
            return r.json().get("matches", [])
        return []
    except:
        return []

@st.cache_data(ttl=3600)
def get_fd_standings(comp_code):
    try:
        r = requests.get(f"{FD_BASE}/competitions/{comp_code}/standings",
                         headers=FD_HEADERS, timeout=8)
        if r.status_code == 200:
            return r.json().get("standings", [])
        return []
    except:
        return []

# ══════════════════════════════════════════════════════════
#  MOTOR POISSON / DIXON-COLES
# ══════════════════════════════════════════════════════════
def poisson_prob(lam, k):
    if lam <= 0: return 0.0
    return (lam**k * math.exp(-lam)) / math.factorial(k)

def calculeaza_prob(atac_h, def_h, atac_a, def_a, media=1.2):
    lam_h = max(atac_h * def_a * media * 1.10, 0.3)
    lam_a = max(atac_a * def_h * media * 0.90, 0.3)

    p1 = px = p2 = 0.0
    p_gg = 0.0
    p_o25 = 0.0

    for i in range(7):
        for j in range(7):
            p = poisson_prob(lam_h, i) * poisson_prob(lam_a, j)
            if i > j:   p1 += p
            elif i == j: px += p
            else:        p2 += p
            if i > 0 and j > 0: p_gg += p
            if i + j > 2:       p_o25 += p

    total = p1 + px + p2
    if total == 0: p1, px, p2 = 0.38, 0.28, 0.34
    else:          p1, px, p2 = p1/total, px/total, p2/total

    return {
        "p1": round(p1, 3), "px": round(px, 3), "p2": round(p2, 3),
        "p_gg": round(p_gg, 3), "p_o25": round(p_o25, 3),
        "lam_h": round(lam_h, 2), "lam_a": round(lam_a, 2)
    }

def prob_to_cota(prob, marja=0.07):
    if prob <= 0.01: return 50.0
    return round(1 / (prob * (1 + marja)), 2)

def forta_din_standing_fd(rows, team_id):
    for row in rows:
        if row.get("team", {}).get("id") == team_id:
            played = max(row.get("playedGames", 1), 1)
            gf = row.get("goalsFor", 2)
            ga = row.get("goalsAgainst", 2)
            return gf / played, ga / played
    return 1.2, 1.2

# ══════════════════════════════════════════════════════════
#  PROCESARE MECIURI FOOTBALL-DATA.ORG
# ══════════════════════════════════════════════════════════
def proceseaza_meciuri_fd(matches, standings_rows):
    meciuri = []
    for m in matches:
        home_id = m["homeTeam"]["id"]
        away_id = m["awayTeam"]["id"]
        home    = m["homeTeam"]["name"]
        away    = m["awayTeam"]["name"]
        comp    = m.get("competition", {}).get("name", "")
        dt_str  = m["utcDate"]

        try:
            dt = datetime.strptime(dt_str[:16], "%Y-%m-%dT%H:%M")
        except:
            continue

        ah, dh = forta_din_standing_fd(standings_rows, home_id)
        aa, da = forta_din_standing_fd(standings_rows, away_id)
        prob   = calculeaza_prob(ah, dh, aa, da)

        meciuri.append({
            "sursa": "FD",
            "comp":  comp,
            "data":  dt.strftime("%d.%m"),
            "ora":   dt.strftime("%H:%M"),
            "home":  home,
            "away":  away,
            "prob":  prob,
            "grup":  ""
        })
    return meciuri

# ══════════════════════════════════════════════════════════
#  ASAMBLARE BILETE
# ══════════════════════════════════════════════════════════
def asambleaza_bilete(selectii):
    bilet_sigur = []
    bilet_combo = []
    bilet_bomba = []
    cota_s = cota_c = cota_b = 1.0

    sortate = sorted(selectii,
                     key=lambda x: max(x["prob"]["p1"], x["prob"]["p2"]),
                     reverse=True)

    for s in sortate:
        p = s["prob"]
        c1   = prob_to_cota(p["p1"])
        cx   = prob_to_cota(p["px"])
        c2   = prob_to_cota(p["p2"])
        c1x  = prob_to_cota(p["p1"] + p["px"])
        cx2  = prob_to_cota(p["px"] + p["p2"])
        cgg  = prob_to_cota(p["p_gg"])
        co25 = prob_to_cota(p["p_o25"])
        prefix = f"({s['data']} {s['ora']}) {s['home']} vs {s['away']}"

        # BILET SIGUR
        if cota_s < 20.0:
            if p["p1"] + p["px"] >= 0.60 and 1.20 <= c1x <= 1.70:
                bilet_sigur.append({"text": f"{prefix} ➜ 1X", "cota": c1x, "comp": s["comp"]})
                cota_s *= c1x
            elif p["px"] + p["p2"] >= 0.60 and 1.20 <= cx2 <= 1.70:
                bilet_sigur.append({"text": f"{prefix} ➜ X2", "cota": cx2, "comp": s["comp"]})
                cota_s *= cx2
            elif p["p_o25"] >= 0.58 and 1.25 <= co25 <= 1.75:
                bilet_sigur.append({"text": f"{prefix} ➜ Peste 2.5 goluri", "cota": co25, "comp": s["comp"]})
                cota_s *= co25
            elif p["p1"] >= 0.52 and 1.25 <= c1 <= 1.80:
                bilet_sigur.append({"text": f"{prefix} ➜ 1 (Victorie gazdă)", "cota": c1, "comp": s["comp"]})
                cota_s *= c1

        # BILET COMBO
        if len(bilet_combo) < 4 and cota_c < 15.0:
            if p["p1"] >= 0.44 and 1.55 <= c1 <= 3.20:
                bilet_combo.append({"text": f"{prefix} ➜ 1", "cota": c1, "comp": s["comp"]})
                cota_c *= c1
            elif p["p2"] >= 0.44 and 1.55 <= c2 <= 3.20:
                bilet_combo.append({"text": f"{prefix} ➜ 2", "cota": c2, "comp": s["comp"]})
                cota_c *= c2
            elif p["p_gg"] >= 0.50 and 1.55 <= cgg <= 2.50:
                bilet_combo.append({"text": f"{prefix} ➜ GG", "cota": cgg, "comp": s["comp"]})
                cota_c *= cgg

        # BILET BOMBĂ
        if len(bilet_bomba) < 3:
            if c2 >= 3.00 and p["p2"] >= 0.30:
                bilet_bomba.append({"text": f"{prefix} ➜ 2 (Surpriză oaspeți)", "cota": c2, "comp": s["comp"]})
                cota_b *= c2
            elif c1 >= 3.00 and p["p1"] >= 0.30:
                bilet_bomba.append({"text": f"{prefix} ➜ 1 (Surpriză gazdă)", "cota": c1, "comp": s["comp"]})
                cota_b *= c1
            elif cgg >= 3.00 and p["p_gg"] >= 0.38:
                bilet_bomba.append({"text": f"{prefix} ➜ GG cotă mare", "cota": cgg, "comp": s["comp"]})
                cota_b *= cgg

    return {
        "sigur": {"selectii": bilet_sigur, "cota": round(cota_s, 2)},
        "combo": {"selectii": bilet_combo, "cota": round(cota_c, 2)},
        "bomba": {"selectii": bilet_bomba, "cota": round(cota_b, 2)},
    }

# ══════════════════════════════════════════════════════════
#  INTERFAȚĂ STREAMLIT — FĂRĂ CAMPIONAT MONDIAL
# ══════════════════════════════════════════════════════════
st.title("🎯 BetMachine Pro - Program 33 — Fără Campionatul Mondial")
st.markdown(f"📅 **{datetime.now().strftime('%d.%m.%Y %H:%M')}** | ⚽ Ligi active football-data.org")

toate_selectiile = []
status_col1, status_col2 = st.columns(2)

# ── Sursa: football-data.org ─────────────────────────────
with st.spinner("⏳ Se descarcă meciurile din football-data.org..."):
    LIGI_FD = ["BSA", "ELC", "PL", "PD", "SA"]  # Premier League, La Liga, Serie A etc.
    meciuri_fd_total = []
    for cod in LIGI_FD:
        matches = get_fd_matches(cod)
        if matches:
            standings_raw = get_fd_standings(cod)
            rows = []
            for sg in standings_raw:
                rows.extend(sg.get("table", []))
            meciuri_fd_total.extend(proceseaza_meciuri_fd(matches, rows))

with status_col1:
    if meciuri_fd_total:
        st.success(f"✅ football-data.org: **{len(meciuri_fd_total)} meciuri** găsite")
        toate_selectiile.extend(meciuri_fd_total)
    else:
        st.warning("⚠️ football-data.org: niciun meci programat în ligile active")

if not toate_selectiile:
    st.error("❌ Nu s-au găsit meciuri din nicio sursă!")
    st.stop()

st.success(f"### Total meciuri analizate: **{len(toate_selectiile)}**")
st.markdown("---")

# ── Generare bilete ──────────────────────────────────────
bilete = asambleaza_bilete(toate_selectiile)

st.subheader("🎫 Biletele Generate de Algoritmul Poisson/Dixon-Coles")
col1, col2, col3 = st.columns(3)

# BILET SIGUR
with col1:
    cs = bilete["sigur"]["cota"]
    atins = cs >= 20.0
    st.metric("Cotă Totală", cs, f"{'Obiectiv atins!' if atins else 'Sub 20.00'}")
    st.markdown("**Selecții:**")
    if bilete["sigur"]["selectii"]:
        for ev in bilete["sigur"]["selectii"]:
            st.markdown(f"✔️ `{ev['cota']}` {ev['text']}")
            st.caption(f"🏆 {ev['comp']}")
    else:
        st.error("Nu s-au găsit selecții sigure.")

# BILET COMBO
with col2:
    cc = bilete["combo"]["cota"]
    st.metric("Cotă Totală", cc, "3-4 selecții echilibrate")
    st.markdown("**Selecții:**")
    if bilete["combo"]["selectii"]:
        for ev in bilete["combo"]["selectii"]:
            st.markdown(f"✔️ `{ev['cota']}` {ev['text']}")
            st.caption(f"🏆 {ev['comp']}")
    else:
        st.error("Nu s-au găsit selecții combo.")

# BILET BOMBĂ
with col3:
    cb = bilete["bomba"]["cota"]
    st.metric("Cotă Totală", cb, "Fiecare selecție ≥ 3.00")
    st.markdown("**Selecții:**")
    if bilete["bomba"]["selectii"]:
        for ev in bilete["bomba"]["selectii"]:
            st.markdown(f"✔️ `{ev['cota']}` {ev['text']}")
            st.caption(f"🏆 {ev['comp']}")
    else:
        st.error("Nu s-au găsit selecții cu cotă ≥ 3.00")

# Tabel meciuri analizate
st.markdown("---")
st.subheader("📋 Toate Meciurile Analizate")

for s in toate_selectiile:
    p = s["prob"]
    with st.expander(
        f"⚽ [{s['data']} {s['ora']}] {s['home']} vs {s['away']} | {s['comp']}"
    ):
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("1",    prob_to_cota(p["p1"]),  f"{int(p['p1']*100)}%")
        c2.metric("X",    prob_to_cota(p["px"]),  f"{int(p['px']*100)}%")
        c3.metric("2",    prob_to_cota(p["p2"]),  f"{int(p['p2']*100)}%")
        c4.metric("GG",   prob_to_cota(p["p_gg"]),f"{int(p['p_gg']*100)}%")
        c5.metric("O2.5", prob_to_cota(p["p_o25"]),f"{int(p['p_o25']*100)}%")
        st.caption(
            f"λ Gazdă: {p['lam_h']} goluri | "
            f"λ Oaspeți: {p['lam_a']} goluri | "
            f"Sursă: {s['sursa']}"
        )

st.caption("⚠️ BetMachine Pro - Program 33 folosește modele statistice Poisson. Jucați responsabil. 18+")
