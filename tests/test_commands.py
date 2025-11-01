from streak import commands
from pathlib import Path

def test_add_and_list(tmp_path):
    path = tmp_path / "data.json"
    commands.add_habit("Read book", path)
    result = commands.list_habits(path)
    assert "Read book" in result
    
def test_mark_done(tmp_path):
    path = tmp_path / "data.json"
    commands.add_habit("Workout", path)
    commands.mark_done(1, path)
    result = commands.list_habits(path)
    assert "[x]" in result
    