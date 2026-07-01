def generate_bilet_sigur(df):
    """
    BILET SIGUR
    - Probabilitate mare
    - Risc mic
    - AX/AY > 8
    - Cote mici 1.10 – 1.40
    """
    sigur = []

    for _, row in df.iterrows():
        if (
            row["col50"] > 8 and
            row["col51"] > 8 and
            row["col19"] < 0.40 and
            row["col15"] > 0.35 and
            row["col16"] > 0.40
        ):
            sigur.append({
                "league": row["col1"],
                "home": row["col3"],
                "away": row["col4"],
                "prediction": "O1.5 FT"
            })

    return sigur[:10]   # 10 selecții


def generate_bilet_combo(df):
    """
    BILET COMBO
    - Probabilitate medie
    - Risc mediu
    - Cote 1.40 – 2.20
    """
    combo = []

    for _, row in df.iterrows():
        if (
            row["col19"] >= 0.40 and row["col19"] <= 0.75 and
            row["col15"] > 0.25 and
            row["col17"] > 0.20
        ):
            # Alegere inteligentă
            if row["col15"] > 0.35:
                pick = "GG"
            else:
                pick = "O1.5 FT"

            combo.append({
                "league": row["col1"],
                "home": row["col3"],
                "away": row["col4"],
                "prediction": pick
            })

    return combo[:6]   # 6 selecții


def generate_bilet_bomba(df):
    """
    BILET BOMBĂ
    - Probabilitate mică
    - Risc mare
    - Cote 2.20 – 6.00
    """
    bomba = []

    for _, row in df.iterrows():
        if (
            row["col19"] > 0.75 and
            row["col15"] > 0.20
        ):
            # Alegere agresivă
            if row["col17"] > 0.25:
                pick = "GG"
            else:
                pick = "O2.5 FT"

            bomba.append({
                "league": row["col1"],
                "home": row["col3"],
                "away": row["col4"],
                "prediction": pick
            })

    return bomba[:6]   # 6 selecții


def generate_predictions(df):
    """
    Biletul Miliardar (standard)
    """
    tickets = []

    for _, row in df.iterrows():
        if row["col8"] == "0-0" and row["col11"] > 0.18:
            pick = "O0.5 HT"
        elif row["col9"] + row["col11"] > 0.45:
            pick = "O1.5 FT"
        elif row["col15"] > 0.30 and row["col17"] > 0.20:
            pick = "GG"
        elif row["col12"] == "X2" or row["col56"] == "X2":
            pick = "X2"
        elif row["col12"] == "1X" or row["col56"] == "1X":
            pick = "1X"
        else:
            pick = "O1.5 FT"

        tickets.append({
            "league": row["col1"],
            "home": row["col3"],
            "away": row["col4"],
            "prediction": pick
        })

    return tickets[:8]
