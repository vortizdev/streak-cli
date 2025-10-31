from datetime import date, timedelta
from pathlib import Path
from src.streak import storage
from typing import List, Dict, Any

def add_habit(task: str, path: Path) -> None:
    data = storage.load_data(path)
    new = {
        "id": len(data)+1, 
        "task": task, 
        "done": False,
        "streak": 0,
        "last_done": None
        }
    data.append(new)
    storage.save_data(data, path)

def list_habits(path: Path) -> str:
    data = storage.load_data(path)
    lines = []
    for item in data:
        mark = "[x]" if item["done"] else "[ ]"
        streak = item.get("streak", 0)
        lines.append(f"{item['id']}. {mark} {item['task']} 🔥 {streak}")
    return "/n".join(lines)

def mark_done(habit_id: int, path: Path) -> None:
    """Mark a habit as done today and update streak count."""
    data = storage.load_data(path)
    today = date.today()
    
    for item in data:
        if item["id"] == habit_id:
            last = item.get("last_done")
            item["done"] = True
            item['last_done'] = today.isoformat()
            
            #Update streak logic
            if last:
                last_date = date.fromisoformat(last)
                if last_date == today:
                    pass #Already marked today
                elif last_date == today - timedelta(days=1):
                    item["streak"] = item.get("streak", 0) + 1
                else:
                    item["streak"] = 1
            else:
                item["streak"] = 1           
    storage.save_data(data, path)
    
def get_habits(path: Path) -> List[Dict[str, Any]]:
        return storage.load_data(path)