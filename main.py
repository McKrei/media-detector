from src.google_client import search_google


def main():
    query = "Сергунин Евгений"
    results = search_google(query, max_results=10, lang="ru")

    for idx, result in enumerate(results, start=1):
        print(f"{idx}. {result['title']}\n{result['link']}\n{result['snippet']}\n")


if __name__ == "__main__":
    main()
