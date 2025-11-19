import json
import os
from typing import Optional

STORAGE_PATH = os.getenv("MEDIA_STORAGE_PATH", "media_history.json")


def _load_all() -> dict:
    if not os.path.exists(STORAGE_PATH):
        return {}
    try:
        with open(STORAGE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_all(data: dict) -> None:
    with open(STORAGE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_last_score(target_name: str) -> Optional[int]:
    data = _load_all()
    entry = data.get(target_name)
    if not entry:
        return None
    return entry.get("last_score")


def save_score(target_name: str, score: int) -> None:
    data = _load_all()
    data[target_name] = {
        "last_score": score,
    }
    _save_all(data)
