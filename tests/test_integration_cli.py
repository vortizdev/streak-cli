import subprocess, sys, json, os
from pathlib import Path

def project_root() -> Path:
    return Path(__file__).parent.parent

def test_add_and_list_integration(tmp_path):
    env = os.environ.copy()
    env["STREAK DATA"] = str(tmp_path / "data.json")
    
    root = project_root()
    
    cmd_add = [sys.executable, "-m", "src.streak", "add", "Test Habit"]
    proc_add = subprocess.run(cmd_add, cwd=str(root), env=env, capture_output=True, text=True)
    assert proc_add.returncode == 0, f"add failed: {proc_add.stderr or proc_add.stdout}"
    
    cmd_list = [sys.executable, "-m", "src.streak", "list"]
    proc_list = subprocess.run(cmd_list, cwd=str(root), env=env,
                            capture_output=True, text=True)
    assert proc_list.returncode == 0, f"list failed: {proc_list.stderr or proc_list.stdout}"
    
    assert "Test Habit" in (proc_list.stdout or ""), f"unexpected output: \n{proc_list.stdout}\n{proc_list.stderr}"