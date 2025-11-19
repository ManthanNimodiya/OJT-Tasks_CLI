from typing import List, Optional
import datetime
from .models import Task
from .storage import Storage
import csv

class TaskManager:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.tasks = self.storage.load_tasks()

    def export_tasks_to_csv(self, filename: str):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Title", "Status", "Priority", "Project", "Recurrence", "Relist Count", "Created At", "Completed At", "Due Date"])
            for task in self.tasks:
                writer.writerow([
                    task.id,
                    task.title,
                    task.status,
                    task.priority,
                    task.project if task.project else "",
                    task.recurrence if task.recurrence else "",
                    task.relist_count,
                    task.created_at,
                    task.completed_at if task.completed_at else "",
                    task.due_date if task.due_date else ""
                ])

    def add_task(self, title: str, project: Optional[str] = None, priority: str = "Medium", recurrence: Optional[str] = None, due_date: Optional[str] = None) -> Task:
        new_id = 1
        if self.tasks:
            new_id = max(t.id for t in self.tasks) + 1
        
        task = Task(id=new_id, title=title, project=project, priority=priority, recurrence=recurrence, due_date=due_date)
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)
        return task

    def list_tasks(self, project: Optional[str] = None, priority: Optional[str] = None) -> List[Task]:
        filtered_tasks = self.tasks
        if project:
            filtered_tasks = [t for t in filtered_tasks if t.project == project]
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority]
        return filtered_tasks

    def update_task(self, task_id: int, title: Optional[str] = None, project: Optional[str] = None, priority: Optional[str] = None, recurrence: Optional[str] = None, status: Optional[str] = None, due_date: Optional[str] = None) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                if title:
                    task.title = title
                if project:
                    task.project = project
                if priority:
                    task.priority = priority
                if recurrence:
                    task.recurrence = recurrence
                if status:
                    # Relist tracking: if changing from done to pending
                    if task.status == "done" and status == "pending":
                        task.relist_count += 1
                        task.completed_at = None
                    task.status = status
                if due_date:
                    task.due_date = due_date
                
                self.storage.save_tasks(self.tasks)
                return task
        return None

    def delete_task(self, task_id: int) -> bool:
        initial_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) < initial_count:
            self.storage.save_tasks(self.tasks)
            return True
        return False

    def complete_task(self, task_id: int) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                task.status = "done"
                task.completed_at = datetime.datetime.now().isoformat()
                
                # Handle recurrence
                if task.recurrence:
                    self.add_task(
                        title=task.title,
                        project=task.project,
                        priority=task.priority,
                        recurrence=task.recurrence,
                        due_date=task.due_date
                    )
                
                self.storage.save_tasks(self.tasks)
                return True
        return False
