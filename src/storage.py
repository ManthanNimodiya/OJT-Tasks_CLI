import json
import os
from typing import List, Dict
from .models import Task

class Storage:
    """
    Handles the persistence of tasks to a JSON file.

    Attributes:
        file_path (str): The absolute path to the JSON file used for storage.
    """
    def __init__(self, file_path: str):
        """
        Initializes the Storage instance.

        Args:
            file_path (str): The path to the JSON file.
        """
        self.file_path = file_path

    def load_tasks(self) -> List[Task]:
        """
        Loads tasks from the JSON file.

        Returns:
            List[Task]: A list of Task objects loaded from the file.
                        Returns an empty list if the file does not exist or is invalid.
        """
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, IOError):
            return []

    def save_tasks(self, tasks: List[Task]):
        """
        Saves a list of tasks to the JSON file.

        Args:
            tasks (List[Task]): The list of Task objects to save.
        """
        data = [task.to_dict() for task in tasks]
        dirname = os.path.dirname(self.file_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        temp_file_path = f"{self.file_path}.tmp"
        with open(temp_file_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        # Atomic replace
        os.replace(temp_file_path, self.file_path)
