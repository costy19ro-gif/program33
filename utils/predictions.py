def generate_bilet_sigur(df):
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
    return sigur[:10]


def generate_bilet_combo(df):
    combo = []
    for _, row in df.iterrows():
        if (
            row["col19"] >= 0.40 and row["col19"] <= 0.75 and
            row["col15"] > 0.25 and
            row["col17"] > 0.20
        ):
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
    return combo[:6]


def generate_bilet_bomba(df):
    bomba = []
    for _, row in df.iterrows():
        if (
            row["col19"] > 0.75 and
            row["col15"] > 0.20
        ):
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
    return bomba[:6]


def generate_predictions(df):
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
