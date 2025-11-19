import itertools


def normalize(text: str) -> str:
    return text.lower().strip()


def prepare_name_variants(full_name: str) -> list[str]:
    """
    Из строки пользователя делаем список слов.
    Генерируем ВСЕ возможные порядки,
    чтобы искать непрерывные фразы в любом порядке.
    """
    parts = [normalize(p) for p in full_name.split() if p.strip()]

    if not parts:
        return []

    variants = []
    # permutations - все перестановки. Пример для 3 слов: ABC, ACB, BAC, BCA, CAB, CBA
    for perm in itertools.permutations(parts):
        variants.append(" ".join(perm))

    return variants


def filter_relevant_results(
    results, full_name: str, extra_keywords: list[str] | None = None
) -> list[dict]:
    """
    Логика максимально простая и строгая:
    1) В тексте должна встречаться ОДНА из перестановок имени подряд.
    2) В том же тексте должно быть хотя бы одно extra_keyword.
    """
    name_variants = prepare_name_variants(full_name)
    if extra_keywords is None:
        extra_keywords = []

    # Предварительная нормализация ключевых слов
    extra_keywords = [normalize(k) for k in extra_keywords]

    relevant = []

    for item in results:
        title = normalize(item.get("title", ""))
        snippet = normalize(item.get("snippet", ""))
        text = f"{title} {snippet}"

        # 1 — Матч имени в любом порядке, но одной фразой
        if not any(variant in text for variant in name_variants):
            continue

        # 2 — Должно быть хоть одно ключевое слово
        if extra_keywords and not any(kw in text for kw in extra_keywords):
            continue

        relevant.append(item)

    return relevant


def calculate_media_score(total_results: int, relevant_results: int) -> int:
    """
    Линейная модель: доля релевантных -> 0..100.
    """
    if total_results == 0:
        return 0

    score = int((relevant_results / total_results) * 100)

    if score < 0:
        return 0
    if score > 100:
        return 100

    return score
