def build_report_html(
    target_name: str, score: int, relevant_results: list[dict], total_results: int
) -> str:
    """
    Формирует HTML-отчёт для Telegram (parse_mode="HTML").
    """

    rel_count = len(relevant_results)

    parts: list[str] = []

    parts.append(f"<b>Отчёт по медийности: {target_name}</b>")
    parts.append(f"Медиабаллы: <b>{score}</b>/100")
    parts.append("")
    parts.append(
        f"Найдено релевантных совпадений: <b>{rel_count}</b> из <b>{total_results}</b>"
    )
    parts.append("")

    if rel_count > 0:
        parts.append("<b>Лучшие совпадения:</b>")

        for item in relevant_results[:3]:
            title = item.get("title", "") or "(без названия)"
            link = item.get("link", "") or ""

            # буллет + кликабельная ссылка
            if link:
                parts.append(f'• <a href="{link}">{title}</a>')
            else:
                parts.append(f"• {title}")

    else:
        parts.append("Релевантные упоминания не найдены.")

    return "\n".join(parts)
