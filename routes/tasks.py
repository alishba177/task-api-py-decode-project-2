from flask import Blueprint, request, jsonify

from data.store import get_all_tasks, get_task_by_id, create_task
from middleware.validate import validate_new_task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# GET /tasks — retrieve all tasks
# Safe & idempotent: does not change server state.
@tasks_bp.get("/")
def list_tasks():
    tasks = get_all_tasks()
    return jsonify({"count": len(tasks), "tasks": tasks}), 200


# GET /tasks/<id> — retrieve a single task by id
@tasks_bp.get("/<task_id>")
def get_task(task_id):
    if not task_id.isdigit():
        return jsonify({"error": "Bad Request", "message": "Task id must be a number."}), 400

    task = get_task_by_id(int(task_id))

    if task is None:
        return jsonify({"error": "Not Found", "message": f"No task found with id {task_id}."}), 404

    return jsonify(task), 200


# POST /tasks — create a new task
# Unsafe & non-idempotent: calling this twice creates two tasks.
@tasks_bp.post("/")
def add_task():
    body = request.get_json(silent=True)
    error, validated = validate_new_task(body)

    if error:
        return jsonify(error), 400

    new_task = create_task(validated["title"], validated["completed"])

    # 201 Created + Location header, per REST convention.
    response = jsonify(new_task)
    response.status_code = 201
    response.headers["Location"] = f"/tasks/{new_task['id']}"
    return response
