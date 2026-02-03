#!/usr/bin/env python3
"""Simple task manager"""
import sys
import json
import os
from datetime import datetime

TASKS_FILE = os.path.expanduser("~/clawd/data/tasks.json")

def load_tasks():
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    if os.path.exists(TASKS_FILE):
        return json.load(open(TASKS_FILE))
    return []

def save_tasks(tasks):
    json.dump(tasks, open(TASKS_FILE, 'w'), indent=2)

def add_task(description, priority="normal"):
    tasks = load_tasks()
    tasks.append({
        "id": len(tasks) + 1,
        "description": description,
        "priority": priority,
        "done": False,
        "created": datetime.now().isoformat()
    })
    save_tasks(tasks)
    print(f"✓ Added task #{len(tasks)}: {description}")

def list_tasks(show_done=False):
    tasks = load_tasks()
    for t in tasks:
        if not t["done"] or show_done:
            status = "✓" if t["done"] else "○"
            prio = "!" if t["priority"] == "high" else ""
            print(f"  {status} [{t['id']}] {prio}{t['description']}")

def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            print(f"✓ Completed: {t['description']}")
            return
    print(f"Task {task_id} not found")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: tasks.py add <description> [high|normal]")
        print("       tasks.py list [--all]")
        print("       tasks.py done <id>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) >= 3:
        prio = sys.argv[-1] if sys.argv[-1] in ["high", "normal"] else "normal"
        desc = " ".join(sys.argv[2:-1] if prio != "normal" else sys.argv[2:])
        add_task(desc, prio)
    elif cmd == "list":
        list_tasks("--all" in sys.argv)
    elif cmd == "done" and len(sys.argv) >= 3:
        complete_task(int(sys.argv[2]))
