import datetime
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Task:
    """
    Represents a single task in the task management system.

    Attributes:
        id (int): Unique identifier for the task.
        title (str): The title or description of the task.
        status (str): Current status of the task (default: "pending").
        priority (str): Priority level of the task (default: "Medium").
        project (Optional[str]): The project this task belongs to.
        recurrence (Optional[str]): Recurrence pattern (e.g., "daily", "weekly").
        created_at (str): ISO format timestamp of when the task was created.
        completed_at (Optional[str]): ISO format timestamp of when the task was completed.
        due_date (Optional[str]): Due date for the task in YYYY-MM-DD format.
    """
    id: int
    title: str
    status: str = "pending"
    priority: str = "Medium"
    project: Optional[str] = None
    recurrence: Optional[str] = None
    created_at: str = "" 
    completed_at: Optional[str] = None
    due_date: Optional[str] = None

    def __post_init__(self):
        """
        Post-initialization hook to set the creation timestamp if not provided.
        """
        if not self.created_at:
            self.created_at = datetime.datetime.now().isoformat()

    def to_dict(self):
        """
        Converts the Task instance to a dictionary.

        Returns:
            dict: A dictionary representation of the task.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Task instance from a dictionary.

        Args:
            data (dict): A dictionary containing task data.

        Returns:
            Task: A new Task instance.
        """
        return cls(**data)
