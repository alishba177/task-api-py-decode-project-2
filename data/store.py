# In-memory "database".
# Project 2 is API-only — no real database is required yet (that comes later).
# This just needs to behave like persistent storage for the lifetime of the server.

_tasks = [
    {"id": 1, "title": "Design API endpoints", "completed": True},
    {"id": 2, "title": "Add input validation", "completed": False},
    {"id": 3, "title": "Handle error responses", "completed": False},
]

_next_id = 4


def get_all_tasks():
    return _tasks


def get_task_by_id(task_id):
    return next((t for t in _tasks if t["id"] == task_id), None)


def create_task(title, completed=False):
    global _next_id
    new_task = {"id": _next_id, "title": title, "completed": completed}
    _tasks.append(new_task)
    _next_id += 1
    return new_task
