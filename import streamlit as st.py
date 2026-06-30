import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def load_match(match_id):
    url = f"https://www.flashscore.com/match/{match_id}/"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        home = soup.select_one(".duelParticipant__home .participant__participantName").text.strip()
        away = soup.select_one(".duelParticipant__away .participant__participantName").text.strip()
    except:
        home = away = None

    try:
        score = soup.select_one(".detailScore__matchInfo").text.strip()
    except:
        score = "N/A"

    try:
        league = soup.select_one(".tournamentHeader__country").text.strip()
    except:
        league = "Unknown"

    return {
        "id": match_id,
        "league": league,
        "home": home,
        "away": away,
        "score": score
    }


def scrape_all(ids):
    results = []
    for mid in ids:
        print(f"Scraping {mid} ...")
        data = load_match(mid)
        if data:
            results.append(data)
        time.sleep(1)
    return results


if __name__ == "__main__":
    # pune aici lista ta
    ids = [
        "IwPWq0hD","ILTH4hVI","h6QrNLiK","zqcn2PEq","jZ7fTmb6","r94nV9Tg",
        "S0MygXWj","pGDVMxDc","vu6QTgTN","bmeyGhgl","2H95LEVQ","rVJISK1T",
        "bghf72MP","6a58qaUI","bZ10oLa6","O6LrHl6t","xr2XQUQ7","QV46XZtn",
        "fwgP1tpm","23dXaKEa","xvuImmSG","zP6eOXjo","E7DFiLbn","f3fESCyQ",
        "020aeGJN","YihotzGk","6NqY95d3","82GrfiO8","OEQelMim","zql7v5N0",
        "pvitQ587","xYwSm90E","tnfPTm9r","ETabtRhl","ro9SomVQ","r9iFxqhD",
        "lCcXRRwe","4lfJlYIE","GxXl9is3","QRGBtnbT","Ie8Upmoe","Cb5Mn9Gr",
        "tGEjhVhL","hxc6hvJq","6XrUGr6D","j96xqRF7","IFbO6U7E","CvoegTad",
        "2HieBbUH","tO8gGan2","YBnsOVx0","fgykqHrH","Sn9oOzIi","zNc6mdnI",
        "CtjULjfD","je5Tr9ko","nNIt4sLq","4tQDGivC","xIxsHWi3","ARGygiW9",
        "xtDjhFmA","dGriP1DU","IT9Gkva4","hlkvEFR1","QXsK4ix9","fsqxuix9",
        "lhUFc166","tx2IC6G7","A1NY2zwq","MonTzavh","W6G6uhqp","C4f32xD4",
        "MZBYzB7M","f3Dtspt9","veVgJtl2","t8CA57t0","Ei9kDbr9","4OnVPySE",
        "n57cBxDL","44dy4f5e","xIfq2YZ7","8fE27TBm","lYFI3oBC","vDo8CaAF",
        "6sQJFprB","AkgMUO9L","IFdexmwn","EshrT6wS","zFFN6avq","YmMkWLiJ",
        "xnhbdmEO","8GeyD4Q6","hrr1lyOk","GW3DtPrg","0MlySB0k","Aep5ldum",
        "Q1HBPlxq","j5nBZyP7","ro0iCS6c","A9gW5YT6","GI82JlZi","dbJQ1PuP",
        "46BuSJQh","dt8XTudt","lthIA9r9","ImzY29U1","rPIDsBEM","lW6AHS34",
        "tYqhP2Xr","UN3MMEFl","Maef03qd","jgblkVKP","tOhaom0c","pUpZTUw2"
    ]

    results = scrape_all(ids)

    with open("scores24_ids.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print("GATA! Am salvat scores24_ids.json")
