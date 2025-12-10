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
        Saves a list of tasks to the JSON file atomically.
        
        It writes to a temporary file first, then renames it to the target file.
        This prevents data corruption if the write fails midway.

        Args:
            tasks (List[Task]): The list of Task objects to save.
        """
        data = [task.to_dict() for task in tasks]
        dirname = os.path.dirname(self.file_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        # Atomic write: write to temp file then rename
        import tempfile
        try:
            # Create a temp file in the same directory to ensure atomic rename works across filesystems
            with tempfile.NamedTemporaryFile('w', dir=dirname if dirname else '.', delete=False, encoding='utf-8') as tf:
                json.dump(data, tf, indent=4)
                temp_name = tf.name
            
            # Atomic replacement
            os.replace(temp_name, self.file_path)
        except Exception as e:
            # Clean up temp file if something went wrong before rename
            if 'temp_name' in locals() and os.path.exists(temp_name):
                os.remove(temp_name)
            raise e
