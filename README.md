
# Task CLI

A command-line interface (CLI) tool for managing tasks with support for projects, priorities, and persistence.

## Features
- **Add Tasks**: Create new tasks with optional project and priority.
- **List Tasks**: View all tasks, or filter by project/priority.
- **Complete Tasks**: Mark tasks as done.
- **Delete Tasks**: Remove tasks permanently.
- **Export Tasks**: Export tasks to a CSV file.
- **Persistence**: Tasks are saved to a JSON file.

## Usage


### Add Task
Create a new task.
```bash
# Simple
python3 task.py add "Buy milk"

# With Project and Priority
python3 task.py add "Finish Report" --project Work --priority High

# Recurring Task (Daily, Weekly, etc.)
python3 task.py add "Daily Standup" --recurrence daily

# With Due Date
python3 task.py add "Submit Assignment" --due-date 2023-12-31
```

### List Tasks
View tasks with optional filters.
```bash
# List all
python3 task.py list

# Filter by Project
python3 task.py list --project Work

# Filter by Priority
python3 task.py list --priority High
```

### Update Task
Modify an existing task.
```bash
# Update Title and Priority
python3 task.py update <id> --title "New Title" --priority Low

# Update Recurrence
python3 task.py update <id> --recurrence weekly

# Relist a Task (Move from Done -> Pending)
# This increments the 'Relist' counter
python3 task.py update <id> --status pending

# Update Due Date
python3 task.py update <id> --due-date 2024-01-15
```

### Complete Task
Mark a task as done.
```bash
python3 task.py done <id>
```
*Note: If the task is recurring, a new pending task will be automatically created.*

### Delete Task
Permanently remove a task.
```bash
python3 task.py delete <id>
```


### Export Tasks
Export tasks to a CSV file.
```bash
# Export to default file (tasks.csv)
python3 task.py export

# Export to specific file
python3 task.py export my_tasks.csv
```

## Running Tests
```bash
python -m unittest discover tests
```
