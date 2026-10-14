import os
import uuid
from datetime import date, datetime, timezone
from functools import wraps

import hmac
import yaml
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

API_TOKEN = os.environ.get("TASKS_API_TOKEN", "demo-token")

with open("openapi.yaml", "r", encoding="utf-8") as file:
    OPENAPI_SPEC = yaml.safe_load(file)

# Demo storage: data disappears when the server restarts.
tasks = {}


def error(message, status):
    return jsonify({"error": message}), status



def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        authorization = request.headers.get("Authorization", "")
        parts = authorization.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return error("Missing or invalid Bearer token", 401)

        token = parts[1]

        if not hmac.compare_digest(token, API_TOKEN):
            return error("Invalid Bearer token", 401)

        return func(*args, **kwargs)

    return wrapper



def valid_date(value):
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def validate_fields(data, creating=False):
    if not isinstance(data, dict):
        return "Request body must be a JSON object"

    allowed = {"title", "status", "priority", "dueDate", "assigneeId"}
    unknown = set(data) - allowed
    if unknown:
        return f"Unknown fields: {', '.join(sorted(unknown))}"

    if creating and not data.get("title", "").strip():
        return "title is required and must not be empty"

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return "title must be a non-empty string"

    if "status" in data:
        if data["status"] not in {"todo", "in_progress", "done"}:
            return "Invalid status"

    if "priority" in data:
        if data["priority"] not in {"low", "medium", "high"}:
            return "Invalid priority"

    if "dueDate" in data and not valid_date(data["dueDate"]):
        return "dueDate must be YYYY-MM-DD or null"

    if "assigneeId" in data:
        value = data["assigneeId"]
        if value is not None and not isinstance(value, str):
            return "assigneeId must be a string or null"

    return None


@app.get("/openapi.json")
def openapi_json():
    return jsonify(OPENAPI_SPEC)


swagger = get_swaggerui_blueprint(
    "/docs",
    "/openapi.json",
    config={"app_name": "Tasks API"},
)
app.register_blueprint(swagger, url_prefix="/docs")


@app.get("/tasks")
@require_auth
def list_tasks():
    result = list(tasks.values())

    status = request.args.get("status")
    priority = request.args.get("priority")

    if status:
        result = [t for t in result if t["status"] == status]
    if priority:
        result = [t for t in result if t["priority"] == priority]

    return jsonify(result), 200


@app.post("/tasks")
@require_auth
def create_task():
    data = request.get_json(silent=True)
    if data is None:
        return error("A JSON request body is required", 400)

    problem = validate_fields(data, creating=True)
    if problem:
        return error(problem, 400)

    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "title": data["title"].strip(),
        "status": data.get("status", "todo"),
        "priority": data.get("priority", "medium"),
        "dueDate": data.get("dueDate"),
        "assigneeId": data.get("assigneeId"),
    }

    tasks[task_id] = task
    return jsonify(task), 201


@app.get("/tasks/<task_id>")
@require_auth
def get_task(task_id):
    try:
        task_id = str(uuid.UUID(task_id))
    except ValueError:
        return error("taskId must be a valid UUID", 400)

    task = tasks.get(task_id)
    if task is None:
        return error("Task not found", 404)

    return jsonify(task), 200


@app.patch("/tasks/<task_id>")
@require_auth
def patch_task(task_id):
    try:
        task_id = str(uuid.UUID(task_id))
    except ValueError:
        return error("taskId must be a valid UUID", 400)

    task = tasks.get(task_id)
    if task is None:
        return error("Task not found", 404)

    data = request.get_json(silent=True)
    if data is None:
        return error("A JSON request body is required", 400)

    problem = validate_fields(data)
    if problem:
        return error(problem, 400)

    if not data:
        return error("At least one field must be provided", 400)

    updated = task.copy()
    for key, value in data.items():
        updated[key] = value.strip() if key == "title" else value

    tasks[task_id] = updated
    return jsonify(updated), 200


@app.delete("/tasks/<task_id>")
@require_auth
def delete_task(task_id):
    try:
        task_id = str(uuid.UUID(task_id))
    except ValueError:
        return error("taskId must be a valid UUID", 400)

    if task_id not in tasks:
        return error("Task not found", 404)

    del tasks[task_id]
    return "", 204


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)