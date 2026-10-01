from flask import Flask, jsonify
from error import ProblemError, register_error_handlers

app = Flask(__name__)

register_error_handlers(app)

USERS = {
    1: {"id": 1, "name": "John"},
    2: {"id": 2, "name": "Alice"},
    3: {"id": 3, "name": "Bob"}
}

@app.get("/users/<int:id>")
def get_user(id):
    if id not in USERS:
        raise ProblemError(
            status=404,
            title="User Not Found",
            type_path="user-not-found",
            resource_id = id
        )
    return jsonify(USERS[id])


@app.get("/test-500")
def trigger_500():
    return 1 / 0  # ZeroDivisionError


if __name__ == "__main__":
    app.run(debug=True)