import unittest
import os
import json
from src.storage import Storage
from src.models import Task

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_storage.json"
        self.storage = Storage(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_tasks(self):
        task = Task(id=1, title="Test Task")
        self.storage.save_tasks([task])
        
        loaded_tasks = self.storage.load_tasks()
        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0].title, "Test Task")

    def test_load_empty_file(self):
        tasks = self.storage.load_tasks()
        self.assertEqual(tasks, [])

if __name__ == '__main__':
    unittest.main()
