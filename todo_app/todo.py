import json
import os
import argparse

FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        content = f.read().strip()
        if not content:          # file exists but is empty
            return []
        return json.loads(content)

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(title):
    tasks = load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": new_id, "title": title, "done": False})
    save_tasks(tasks)
    print(f"✓ Added: [{new_id}] {title}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet. Add one with: python todo.py add \"Task name\"")
        return
    for t in tasks:
        status = "✓" if t["done"] else "○"
        print(f"  {status} [{t['id']}] {t['title']}")


def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            print(f"✓ Marked done: {t['title']}")
            return
    print(f"No task with id {task_id}")


def delete_task(task_id):
    tasks = load_tasks()
    updated = [t for t in tasks if t["id"] != task_id]
    if len(updated) == len(tasks):
        print(f"No task with id {task_id}")
        return
    save_tasks(updated)
    print(f"✓ Deleted task {task_id}")


def main():
    parser = argparse.ArgumentParser(description="CLI To-Do List")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title")

    subparsers.add_parser("list", help="List all tasks")

    done_parser = subparsers.add_parser("done", help="Mark a task as complete")
    done_parser.add_argument("id", type=int, help="Task ID")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()