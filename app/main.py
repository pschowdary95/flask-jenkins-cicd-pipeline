
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory database
tasks = {}
next_id = 1


# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project": "Flask Jenkins CI/CD Pipeline",
        "message": "Welcome! Application is running successfully.",
        "status": "success",
        "endpoints": [
            "/",
            "/health",
            "/tasks"
        ]
    }), 200


# Health check route
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "message": "Application is running successfully"
    }), 200


# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({
        "total_tasks": len(tasks),
        "tasks": list(tasks.values())
    }), 200


# Create a new task
@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id

    data = request.get_json(silent=True)

    if not data or not isinstance(data, dict):
        return jsonify({
            "error": "Valid JSON data is required"
        }), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "A valid title is required"
        }), 400

    task = {
        "id": next_id,
        "title": title.strip(),
        "done": False
    }

    tasks[next_id] = task
    next_id += 1

    return jsonify({
        "message": "Task created successfully",
        "task": task
    }), 201


# Get a particular task
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = tasks.get(task_id)

    if task is None:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify(task), 200


# Mark task as completed
@app.route("/tasks/<int:task_id>/complete", methods=["PATCH"])
def complete_task(task_id):
    task = tasks.get(task_id)

    if task is None:
        return jsonify({
            "error": "Task not found"
        }), 404

    task["done"] = True

    return jsonify({
        "message": "Task completed successfully",
        "task": task
    }), 200


# Delete a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({
            "error": "Task not found"
        }), 404

    del tasks[task_id]

    return jsonify({
        "message": "Task deleted successfully"
    }), 200


# Run Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
