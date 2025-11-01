import json 
from streak import storage

def test_save_and_load(tmp_path):
    file_path = tmp_path / "data.json"
    data = [{"id": 1, "task": "Read", "done": False}]
    storage.save_data(data, file_path)
    loaded = storage.load_data(file_path)
    assert loaded == data
    
def test_load_creates_empty_file(tmp_path):
    file_path = tmp_path / "missing.json"
    data = storage.load_data(file_path)
    assert data == []
    assert file_path.exists()