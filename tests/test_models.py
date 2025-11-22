import unittest
from src.models import Task

class TestTaskModel(unittest.TestCase):
    def test_task_creation(self):
        task = Task(id=1, title="Test Task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.priority, "Medium")

    def test_task_to_dict(self):
        task = Task(id=1, title="Test Task")
        data = task.to_dict()
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], "Test Task")

    def test_task_from_dict(self):
        data = {
            "id": 1,
            "title": "Test Task",
            "status": "pending",
            "priority": "Medium"
        }
        task = Task.from_dict(data)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")

if __name__ == '__main__':
    unittest.main()
