# scraper_scores24_ids.py (rulezi LOCAL, nu în Streamlit Cloud)
import requests
from bs4 import BeautifulSoup
import json
import concurrent.futures

HEADERS = {"User-Agent": "Mozilla/5.0"}

def load_match(match_id):
    url = f"https://www.flashscore.com/match/{match_id}/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, "lxml")

        home = soup.select_one(".duelParticipant__home .participant__participantName")
        away = soup.select_one(".duelParticipant__away .participant__participantName")
        score = soup.select_one(".detailScore__matchInfo")
        league = soup.select_one(".tournamentHeader__country")

        return {
            "id": match_id,
            "league": league.text.strip() if league else "Unknown",
            "home": home.text.strip() if home else None,
            "away": away.text.strip() if away else None,
            "score": score.text.strip() if score else "N/A",
        }
    except:
        return None

def scrape_all(ids):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(load_match, mid): mid for mid in ids}
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            if data:
                results.append(data)
    return results

if __name__ == "__main__":
    # citește ID-urile exportate din Excel
    with open(r"E:\AAA _ matchID\match_ids.txt", "r", encoding="utf-8") as f:
        ids = [line.strip() for line in f if line.strip()]

    results = scrape_all(ids)

    with open("scores24.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print("GATA, am salvat scores24.json (urcă-l în GitHub în același folder cu program33.py)")
