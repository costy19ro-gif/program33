import pandas as pd

def load_data():
    df = pd.read_csv("scores24.csv")
    return df

def filter_matches(df):
    # Regula AX/AY > 6
    df = df[(df["col50"] > 6) & (df["col51"] > 6)]

    # Regula probabilități HT/FT
    df = df[
        (df["col9"] + df["col11"] > 0.40) &     # prob_ht_1 + prob_ht_x
        (df["col15"] > 0.25) &                  # Poisson 1
        (df["col16"] > 0.35) &                  # Poisson X
        (df["col17"] > 0.20) &                  # Poisson 2
        (df["col19"] > 0.75)                    # risk mare
    ]

    return df

def generate_predictions(df):
    tickets = []

    for _, row in df.iterrows():

        league = row["col1"]
        home = row["col3"]
        away = row["col4"]

        # Regula O0.5 HT
        if row["col8"] == "0-0" and row["col11"] > 0.18:
            pick = "O0.5 HT"

        # Regula O1.5 FT
        elif row["col9"] + row["col11"] > 0.45:
            pick = "O1.5 FT"

        # Regula GG
        elif row["col15"] > 0.30 and row["col17"] > 0.20:
            pick = "GG"

        # Regula X2
        elif row["col12"] == "X2" or row["col56"] == "X2":
            pick = "X2"

        # Regula 1X
        elif row["col12"] == "1X" or row["col56"] == "1X":
            pick = "1X"

        else:
            pick = "O1.5 FT"

        tickets.append({
            "league": league,
            "home": home,
            "away": away,
            "prediction": pick
        })

    return tickets

def generate_bilet_miliardar():
    df = load_data()
    df = filter_matches(df)
    tickets = generate_predictions(df)

    # Selectăm cele mai bune 8 meciuri
    final_ticket = tickets[:8]

    print("\n=== BILETUL MILIARDAR ===\n")
    for t in final_ticket:
        print(f"{t['league']} | {t['home']} - {t['away']} → {t['prediction']}")

    print("\n==========================\n")

if __name__ == "__main__":
    generate_bilet_miliardar()
