import datetime
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    status: str = "pending"
    priority: str = "Medium"
    project: Optional[str] = None
    recurrence: Optional[str] = None
    relist_count: int = 0
    created_at: str = "" 
    completed_at: Optional[str] = None
    due_date: Optional[str] = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.datetime.now().isoformat()

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
