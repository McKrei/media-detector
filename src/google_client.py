import requests
import math
from src.config import SERPER_API_KEY


def search_google(query: str, max_results: int = 30, lang: str = "ru"):
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json",
    }

    # Serper даёт максимум 10 результатов на page
    per_page = 10
    pages_needed = math.ceil(
        max_results / per_page
    )  # ceil - округление вверх. 21 -> 3, 20 -> 2

    all_results = []

    for page in range(1, pages_needed + 1):
        payload = {"q": query, "gl": lang, "hl": lang, "page": page, "num": per_page}

        resp = requests.post(
            "https://google.serper.dev/search",
            json=payload,
            headers=headers,
            timeout=10,
        )

        if resp.status_code != 200:
            raise RuntimeError(f"Serper API error: {resp.status_code} {resp.text}")

        data = resp.json()
        organic = data.get("organic", [])

        for item in organic:
            all_results.append(
                {
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "link": item.get("link", ""),
                }
            )

        # Защитный выход если результатов меньше, чем хотели
        if len(organic) < per_page:
            break

    return all_results[:max_results]
