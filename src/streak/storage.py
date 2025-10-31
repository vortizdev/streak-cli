import json
from pathlib import Path
from typing import Any

def load_data(file_path: Path) -> list[dict[str, Any]]:
    """Load data from a JSON file. If the file does not exist, create it with an empty list."""
    if not file_path.exists():
        file_path.write_text("[]", encoding="utf-8")
        return []
    text = file_path.read_text(encoding="utf-8")
    return json.loads(text or "[]")

def save_data(data: list[dict[str, Any]], file_path: Path) -> None:
    """Save data to a JSON file."""
    text = json.dumps(data, indent=2)
    file_path.write_text(text, encoding="utf-8")