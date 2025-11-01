"""Business logic for the Streak CLI.

This module contains small, well-contained functions that operate on the
JSON-backed storage managed by `src.streak.storage`.

Notes / conventions used here:
- `path` arguments are `pathlib.Path` objects pointing to a JSON file
  (typically `data.json`). Tests pass a `tmp_path / "data.json"`.
- `last_done` is stored as an ISO date string (YYYY-MM-DD) or None.
- `streak` is an integer count representing consecutive days completed.
- `list_habits` currently returns a joined string (tests look for
  substrings). There's a small existing typo where lines are joined with
  the literal string "/n" instead of a newline; be conservative when
  changing this behaviour unless tests are updated.
"""

from datetime import date, timedelta
from pathlib import Path
from src.streak import storage
from typing import List, Dict, Any


def add_habit(task: str, path: Path) -> None:
    """Add a new habit to storage.

    Behaviour/contract:
    - Loads existing data with `storage.load_data(path)` (creates file if
      missing).
    - Appends a dict with keys: id (1-based, len(data)+1), task, done,
      streak, last_done.
    - Persists via `storage.save_data`.

    Edge cases:
    - IDs are assigned as len(data)+1; deleting items would not re-sequence
      existing IDs. If you change this, update tests that assume id=1 for
      the first added item.
    """
    data = storage.load_data(path)
    new = {
        "id": len(data) + 1,
        "task": task,
        "done": False,
        "streak": 0,
        "last_done": None,
    }
    data.append(new)
    storage.save_data(data, path)


def list_habits(path: Path) -> str:
    """Return a human-friendly listing of habits.

    Implementation detail: the function returns a single string made by
    joining per-habit lines. Tests usually check for substrings (e.g.
    the task text or "[x]") rather than the exact formatting, so when
    adjusting output prefer backwards-compatible tweaks or update tests.
    """
    data = storage.load_data(path)
    lines = []
    for item in data:
        mark = "[x]" if item["done"] else "[ ]"
        streak = item.get("streak", 0)
        lines.append(f"{item['id']}. {mark} {item['task']} 🔥 {streak}")
    # NOTE: existing code used "/n" (typo). Keep this join string stable
    # unless you update tests that assert exact output.
    return "/n".join(lines)


def mark_done(habit_id: int, path: Path) -> None:
    """Mark the given habit id as done for today and update its streak.

    Behaviour notes:
    - Finds the habit dict by matching `item['id'] == habit_id`.
    - Sets `done` to True and writes `last_done` as an ISO date string.
    - Streak update rules:
      * If `last_done` is today -> do nothing (already marked).
      * If `last_done` is yesterday -> increment `streak` by 1.
      * Otherwise (gap or missing) -> set `streak` to 1.

    Edge cases & test hooks:
    - Tests simulate consecutive days by directly manipulating the JSON
      (see `tests/test_streaks.py`) — they set `last_done` to
      (today - 1 day).isoformat() and call `mark_done` again to verify
      the increment behaviour.
    - The function overwrites `last_done` with today's date even if the
      habit was already marked today; the code currently `pass` on same
      day but still assigns `last_done` above — this is conservative but
      predictable.
    """
    data = storage.load_data(path)
    today = date.today()

    for item in data:
        if item["id"] == habit_id:
            last = item.get("last_done")
            # mark done for UI/showing purposes
            item["done"] = True
            # store last_done as ISO date string for easy round-tripping
            item["last_done"] = today.isoformat()

            # Update streak logic based on last_done
            if last:
                # last is expected to be an ISO-formatted date string
                last_date = date.fromisoformat(last)
                if last_date == today:
                    # Already marked today: keep streak as-is
                    pass
                elif last_date == today - timedelta(days=1):
                    # Consecutive day -> increment streak
                    item["streak"] = item.get("streak", 0) + 1
                else:
                    # Gap -> reset to 1
                    item["streak"] = 1
            else:
                # First completion -> start streak at 1
                item["streak"] = 1
    storage.save_data(data, path)


def get_habits(path: Path) -> List[Dict[str, Any]]:
    """Return the raw loaded list of habit dicts from storage.

    This function is a thin wrapper around `storage.load_data` used by the
    CLI renderer in `__main__.py` which expects a list of dicts.
    """
    return storage.load_data(path)