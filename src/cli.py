import argparse
import sys
from .manager import TaskManager
from .storage import Storage

def main(storage_path: str):
    storage = Storage(storage_path)
    manager = TaskManager(storage)

    parser = argparse.ArgumentParser(description="Task CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--project", help="Project name")
    add_parser.add_argument("--priority", choices=["Low", "Medium", "High"], default="Medium", help="Task priority")
    add_parser.add_argument("--recurrence", help="Recurrence pattern (e.g., daily, weekly)")
    add_parser.add_argument("--due-date", help="Due date (YYYY-MM-DD)")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("--title", help="New title")
    update_parser.add_argument("--project", help="New project")
    update_parser.add_argument("--priority", choices=["Low", "Medium", "High"], help="New priority")
    update_parser.add_argument("--recurrence", help="New recurrence")
    update_parser.add_argument("--status", choices=["pending", "done"], help="New status")
    update_parser.add_argument("--due-date", help="New due date (YYYY-MM-DD)")

    # List command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--project", help="Filter by project")
    list_parser.add_argument("--priority", help="Filter by priority")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # Done command
    done_parser = subparsers.add_parser("done", help="Mark task as done")
    done_parser.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.command == "add":
        task = manager.add_task(args.title, args.project, args.priority, args.recurrence, args.due_date)
        print(f"Task added: {task.id} - {task.title}")
    
    elif args.command == "list":
        tasks = manager.list_tasks(args.project, args.priority)
        if not tasks:
            print("No tasks found.")
        else:
            print(f"{'ID':<5} {'Title':<30} {'Project':<15} {'Priority':<10} {'Status':<10} {'Recurrence':<12} {'Due Date':<12} {'Relist':<6}")
            print("-" * 115)
            for task in tasks:
                project = task.project if task.project else ""
                recurrence = task.recurrence if task.recurrence else ""
                due_date = task.due_date if task.due_date else ""
                print(f"{task.id:<5} {task.title[:28]:<30} {project[:13]:<15} {task.priority:<10} {task.status:<10} {recurrence[:10]:<12} {due_date:<12} {task.relist_count:<6}")

    elif args.command == "update":
        task = manager.update_task(
            args.id, 
            title=args.title, 
            project=args.project, 
            priority=args.priority, 
            recurrence=args.recurrence, 
            status=args.status,
            due_date=args.due_date
        )
        if task:
            print(f"Task {task.id} updated.")
        else:
            print(f"Task {args.id} not found.")

    elif args.command == "delete":
        if manager.delete_task(args.id):
            print(f"Task {args.id} deleted.")
        else:
            print(f"Task {args.id} not found.")

    elif args.command == "done":
        if manager.complete_task(args.id):
            print(f"Task {args.id} marked as done.")
        else:
            print(f"Task {args.id} not found.")

    else:
        parser.print_help()
