from streak import commands
from datetime import date, timedelta
from pathlib import Path

def test_first_completion_sets_streak(tmp_path):
    path = tmp_path / "data.json"
    commands.add_habit("Read", path)
    commands.mark_done(1, path)
    data = commands.get_habits(path)
    assert data[0]["streak"] == 1
    
def test_consequtive_days_increase_streak(tmp_path):
    path = tmp_path / "data.json"
    commands.add_habit("Run", path)
    
    #First day
    commands.mark_done(1, path)
    #Simulate yesterdays completion
    from src.streak import storage
    stored = storage.load_data(path)
    stored[0]["last_done"] = (date.today() - timedelta(days=1)).isoformat()
    storage.save_data(stored, path)
    
    commands.mark_done(1, path)
    data = commands.get_habits(path)
    assert data[0]["streak"] == 2
    