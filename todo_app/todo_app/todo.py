import os
import json

FILE = 'todos.json'

def load_tasks():
    if not os.path.exists(FILE):
        return[]
    with open ('FILE' , 'r') as f:
        return json.load(f)
    
def save_tasks(tasks):
    with open('FILE' , 'w') as f:
        return json.dumps(tasks , f , indent=2)
    
def add_tasks(title):
    tasks = load_tasks()
    new_id =max((t["id"] for t in tasks) , default=0) + 1
    tasks.append({"id": new_id , "title": title , "done": False})
    save_tasks(tasks)
    print(f"Added task:{new_id} {title}")
    
def list_tasks():
    tasks = load_tasks()
    for task in tasks:
        status = "✓" if task["done"] else "○"
        print(f"[{status}] {task['id']}: {task['title']}")
    else:
        print("No tasks yet. Add one with: python todo.py add \"Task name\"")

def complete_tasks():
    tasks = load_tasks()
    
    if not tasks:
        print("No tasks to complete.")
        return
    for task in tasks:
        if not task["done"]:
            task["done"] = True
            print(f"Completed task: {task['id']} {task['title']}")
    save_tasks(tasks)
    
def delete_tasks(task_id):
    tasks = load_tasks()
    updated = [t for t in tasks if t["id"] != task_id]
    if len(updated) == len(tasks):
        print(f"No task with id {task_id}")
        return
    save_tasks(updated)
    print(f"Deleted task with id {task_id}")
    
