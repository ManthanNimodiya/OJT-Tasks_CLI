from typing import List, Optional
import datetime
from .models import Task
from .storage import Storage
import csv

class TaskManager:
    """
    Manages the lifecycle of tasks, including creation, updates, deletion, and retrieval.
    """
    def __init__(self, storage: Storage):
        """
        Initializes the TaskManager.

        Args:
            storage (Storage): The storage backend to use for persisting tasks.
        """
        self.storage = storage
        self.tasks = self.storage.load_tasks()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieves a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            Optional[Task]: The task if found, else None.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_active_tasks(self) -> List[Task]:
        """
        Retrieves all tasks that are not marked as 'done'.

        Returns:
            List[Task]: A list of active tasks.
        """
        return [task for task in self.tasks if task.status != "done"]

    def export_tasks_to_csv(self, filename: str):
        """
        Exports all tasks to a CSV file.

        Args:
            filename (str): The name of the file to export to.
        """
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Title", "Status", "Priority", "Project", "Recurrence", "Due Date", "Created At", "Completed At"])
            for task in self.tasks:
                writer.writerow([
                    task.id,
                    task.title,
                    task.status,
                    task.priority,
                    task.project if task.project else "",
                    task.recurrence if task.recurrence else "",
                    task.due_date if task.due_date else "",
                    task.created_at,
                    task.completed_at if task.completed_at else ""
                ])

    def add_task(self, title: str, project: Optional[str] = None, priority: str = "Medium", recurrence: Optional[str] = None, due_date: Optional[str] = None, allow_duplicates: bool = False) -> Task:
        """
        Adds a new task.

        Args:
            title (str): The title of the task.
            project (Optional[str]): The project name.
            priority (str): The priority level (default: "Medium").
            recurrence (Optional[str]): Recurrence pattern.
            due_date (Optional[str]): Due date in YYYY-MM-DD format.
            allow_duplicates (bool): Whether to allow duplicate tasks.

        Returns:
            Task: The newly created task.
        """
        # Check for duplicates
        if not allow_duplicates:
            for task in self.tasks:
                if task.title == title and task.status != "done":
                    raise ValueError("Task already exists")

        new_id = 1
        if self.tasks:
            new_id = max(t.id for t in self.tasks) + 1
        
        task = Task(id=new_id, title=title, project=project, priority=priority, recurrence=recurrence, due_date=due_date)
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)
        return task

    def list_tasks(self, project: Optional[str] = None, priority: Optional[str] = None) -> List[Task]:
        """
        Lists tasks, optionally filtering by project or priority.

        Args:
            project (Optional[str]): Filter by project name.
            priority (Optional[str]): Filter by priority level.

        Returns:
            List[Task]: A list of matching tasks.
        """
        filtered_tasks = self.tasks
        if project:
            filtered_tasks = [t for t in filtered_tasks if t.project == project]
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority]
        return filtered_tasks

    def update_task(self, task_id: int, title: Optional[str] = None, project: Optional[str] = None, priority: Optional[str] = None, recurrence: Optional[str] = None, status: Optional[str] = None, due_date: Optional[str] = None) -> Optional[Task]:
        """
        Updates an existing task.

        Args:
            task_id (int): The ID of the task to update.
            title (Optional[str]): New title.
            project (Optional[str]): New project.
            priority (Optional[str]): New priority.
            recurrence (Optional[str]): New recurrence.
            status (Optional[str]): New status.
            due_date (Optional[str]): New due date.

        Returns:
            Optional[Task]: The updated task, or None if not found.
        """
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
                    # if changing from done to pending, clear completed_at
                    if task.status == "done" and status == "pending":
                        task.completed_at = None
                    task.status = status
                if due_date:
                    task.due_date = due_date
                
                self.storage.save_tasks(self.tasks)
                return task
        return None

    def delete_task(self, task_id: int) -> bool:
        """
        Deletes a task by ID.

        Args:
            task_id (int): The ID of the task to delete.

        Returns:
            bool: True if the task was deleted, False if not found.
        """
        initial_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) < initial_count:
            self.storage.save_tasks(self.tasks)
            return True
        return False

    def complete_task(self, task_id: int) -> bool:
        """
        Marks a task as complete. Handles recurrence if applicable.

        Args:
            task_id (int): The ID of the task to complete.

        Returns:
            bool: True if the task was completed, False if not found.
        """
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
