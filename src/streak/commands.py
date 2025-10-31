from pathlib import Path
from src.streak import storage

def add_habit(task: str, path: Path) -> None:
    data = storage.load_data(path)
    new = {"id": len(data)+1, "task": task, "done": False}
    data.append(new)
    storage.save_data(data, path)

def list_habits(path: Path) -> str:
    data = storage.load_data(path)
    lines = []
    for item in data:
        mark = "[x]" if item["done"] else "[ ]"
        lines.append(f"{item['id']}. {mark} {item['task']}")
    return "/n".join(lines)

def mark_done(habit_id: int, path: Path) -> None:
    data = storage.load_data(path)
    for item in data:
        if item["id"] == habit_id:
            item["done"] = True
    storage.save_data(data, path)