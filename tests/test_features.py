import unittest
import os
from src.manager import TaskManager
from src.storage import Storage

class TestFeatures(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_features.json"
        self.storage = Storage(self.test_file)
        self.manager = TaskManager(self.storage)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_update_task(self):
        task = self.manager.add_task("Original Title", priority="Low")
        updated_task = self.manager.update_task(task.id, title="New Title", priority="High")
        
        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.priority, "High")
        self.assertEqual(self.manager.tasks[0].title, "New Title")

    def test_recurrence_creation(self):
        task = self.manager.add_task("Daily Task", recurrence="daily")
        self.manager.complete_task(task.id)
        
        # Should have 2 tasks: one done, one pending
        self.assertEqual(len(self.manager.tasks), 2)
        self.assertEqual(self.manager.tasks[0].status, "done")
        self.assertEqual(self.manager.tasks[1].status, "pending")
        self.assertEqual(self.manager.tasks[1].title, "Daily Task")
        self.assertEqual(self.manager.tasks[1].recurrence, "daily")

    def test_relist_tracking(self):
        task = self.manager.add_task("Task to Relist")
        self.manager.complete_task(task.id)
        self.assertEqual(self.manager.tasks[0].status, "done")
        
        # Relist (Done -> Pending)
        self.manager.update_task(task.id, status="pending")
        self.assertEqual(self.manager.tasks[0].status, "pending")
        self.assertEqual(self.manager.tasks[0].relist_count, 1)
        
        # Complete and Relist again
        self.manager.complete_task(task.id)
        self.manager.update_task(task.id, status="pending")
        self.assertEqual(self.manager.tasks[0].relist_count, 2)

if __name__ == "__main__":
    unittest.main()
