from src.google_client import search_google
from src.scoring import filter_relevant_results, calculate_media_score
from src.report import build_report_html
from src.telegram_client import send_message
from src.storage import load_last_score, save_score


TARGETS = [
    # {
    #     "name": "Evgenii Sergunin",
    #     "query": "Евгений Сергунин Валерьевич",
    #     "extra_keywords": [],
    #     "lang": "ru",
    #     "max_results": 30,
    # },
    {
        "name": "Чуян Андрей",
        "query": "Чуян Андрей",
        "extra_keywords": ["IT", "инфраструктура", "DevOps", "инженер", "IT-волна", "Debug Skills", "Debug Camp"],
        "lang": "ru",
        "max_results": 30,
    }
]


def run_for_target(target: dict) -> None:
    name = target["name"]
    query = target["query"]
    extra_keywords = target.get("extra_keywords", [])
    lang = target.get("lang", "ru")
    max_results = target.get("max_results", 30)

    results = search_google(query=query, max_results=max_results, lang=lang)

    relevant = filter_relevant_results(
        results=results,
        full_name=query,
        extra_keywords=extra_keywords,
    )

    score = calculate_media_score(
        total_results=len(results),
        relevant_results=len(relevant),
    )

    last_score = load_last_score(name)
    report_text = build_report_html(
        target_name=name,
        score=score,
        relevant_results=relevant,
        total_results=len(results),
    )

    if last_score is not None:
        delta = score - last_score
        report_text += (
            f"\nИзменение относительно последнего значения: "
            f"{delta:+d} (было {last_score})."
        )

    send_message(report_text)
    save_score(name, score)


def main() -> None:
    for target in TARGETS:
        run_for_target(target)


if __name__ == "__main__":
    main()
