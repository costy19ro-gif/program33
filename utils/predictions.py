def generate_predictions(df):
    tickets = []

    for _, row in df.iterrows():

        # Reguli de predicție
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

    return tickets
