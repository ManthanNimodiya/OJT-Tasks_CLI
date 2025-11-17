import json
import os
from typing import List, Dict
from .models import Task

class Storage:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_tasks(self) -> List[Task]:
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, IOError):
            return []

    def save_tasks(self, tasks: List[Task]):
        data = [task.to_dict() for task in tasks]
        dirname = os.path.dirname(self.file_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)
