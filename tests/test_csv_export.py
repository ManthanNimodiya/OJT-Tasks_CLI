import unittest
import os
import csv
from src.manager import TaskManager
from src.storage import Storage
from src.models import Task

class TestCSVExport(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_tasks_export.json"
        self.csv_file = "test_tasks_export.csv"
        self.storage = Storage(self.test_file)
        self.manager = TaskManager(self.storage)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_export_tasks_to_csv(self):
        # Add some tasks
        self.manager.add_task("Task 1", priority="High", project="Project A")
        self.manager.add_task("Task 2", priority="Low", project="Project B")
        
        # Export to CSV
        self.manager.export_tasks_to_csv(self.csv_file)
        
        # Verify CSV content
        self.assertTrue(os.path.exists(self.csv_file))
        
        with open(self.csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            self.assertEqual(len(rows), 2)
            
            self.assertEqual(rows[0]['Title'], "Task 1")
            self.assertEqual(rows[0]['Priority'], "High")
            self.assertEqual(rows[0]['Project'], "Project A")
            
            self.assertEqual(rows[1]['Title'], "Task 2")
            self.assertEqual(rows[1]['Priority'], "Low")
            self.assertEqual(rows[1]['Project'], "Project B")

if __name__ == "__main__":
    unittest.main()
