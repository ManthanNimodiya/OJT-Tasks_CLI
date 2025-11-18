import unittest
import os
import json
from src.manager import TaskManager
from src.storage import Storage
from src.models import Task 

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_tasks.json"
        self.storage = Storage(self.test_file)
        self.manager = TaskManager(self.storage)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_task(self):
        task = self.manager.add_task("Test Task", priority="High")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.priority, "High")
        self.assertEqual(len(self.manager.tasks), 1)

    def test_delete_task(self):
        task = self.manager.add_task("To Delete")
        self.assertTrue(self.manager.delete_task(task.id))
        self.assertEqual(len(self.manager.tasks), 0)

    def test_complete_task(self):
        task = self.manager.add_task("To Complete")
        self.assertTrue(self.manager.complete_task(task.id))
        self.assertEqual(self.manager.tasks[0].status, "done")

    def test_list_tasks_filter(self):
        self.manager.add_task("Task 1", project="A")
        self.manager.add_task("Task 2", project="B")
        
        tasks_a = self.manager.list_tasks(project="A")
        self.assertEqual(len(tasks_a), 1)
        self.assertEqual(tasks_a[0].title, "Task 1")

    def test_add_task_with_due_date(self):
        task = self.manager.add_task("Due Task", due_date="2023-12-31")
        self.assertEqual(task.due_date, "2023-12-31")
        
        # Verify persistence
        new_manager = TaskManager(Storage(self.test_file))
        loaded_task = new_manager.tasks[0]
        self.assertEqual(loaded_task.due_date, "2023-12-31")

if __name__ == "__main__":
    unittest.main()
