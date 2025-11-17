import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from src.manager import TaskManager
from src.storage import Storage

print("Starting manual verification...")

try:
    test_file = "manual_test_tasks.json"
    if os.path.exists(test_file):
        os.remove(test_file)
    
    storage = Storage(test_file)
    manager = TaskManager(storage)
    
    print("Adding task...")
    task = manager.add_task("Test Task", recurrence="daily")
    print(f"Task added: {task.id}")
    
    print("Completing task...")
    manager.complete_task(task.id)
    print("Task completed.")
    
    print("Checking tasks...")
    tasks = manager.list_tasks()
    for t in tasks:
        print(f"Task: {t.id} - {t.title} - {t.status} - {t.recurrence}")
        
    print("Updating task...")
    manager.update_task(task.id, status="pending")
    print("Task updated.")
    
    print("Done.")
    
    if os.path.exists(test_file):
        os.remove(test_file)

except Exception as e:
    print(f"Error: {e}")
