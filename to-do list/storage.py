import os
import json
from pathlib import Path
import platform

def get_data_file():
    system = platform.system()
    if system == "Windows":
        base_dir = Path(os.getenv("APPDATA")) / "ToDoList"
    else:
        base_dir = Path.home() / ".todolist"

    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / "tasks.json"

DATA_FILE = get_data_file()

def load_tasks():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)
