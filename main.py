from src.google_client import search_google
from src.scoring import filter_relevant_results, calculate_media_score


def main():
    # query = "Сергунин Евгений"
    query = "Чуян Андрей"
    google_results = search_google(query, max_results=10, lang="ru")

    # for idx, result in enumerate(results, start=1):
    #     print(f"{idx}. {result['title']}\n{result['link']}\n{result['snippet']}\n")

    relevant_results = filter_relevant_results(
        google_results,
        full_name=query,
        # extra_keywords=["python", "vk", "разработчик", "developer", "Data Science"],
        extra_keywords=["IT", "инфраструктура", "DevOps", "инженер", "IT-волна", "Debug Skills", "Debug Camp"],
    )

    score = calculate_media_score(
        total_results=len(google_results),
        relevant_results=len(relevant_results),
    )

    print(f"Total results: {len(google_results)}")
    print(f"Relevant results: {len(relevant_results)}")
    print(f"Media score: {score}/100")


if __name__ == "__main__":
    main()
