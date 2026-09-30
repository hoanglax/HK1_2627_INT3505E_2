from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

class ProblemError(Exception):
    def __init__(self, status, title, detail=None, type="about:blank"):
        self.status = status
        self.title = title
        self.detail = detail
        self.type = type

@app.errorhandler(ProblemError)
def handle_problem_error(e):
    data = {
        "type": e.type,
        "title": e.title,
        "status": e.status,
        "detail": e.detail,
        "instance": request.path
    }
    return jsonify(data), e.status, {"Content-Type": "application/problem+json"}

@app.errorhandler(HTTPException)
def handle_http_error(e):
    data = {
        "type": "about:blank",
        "title": e.name,
        "status": e.code,
        "detail": e.description,
        "instance": request.path
    }
    return jsonify(data), e.code, {"Content-Type": "application/problem+json"}

@app.errorhandler(Exception)
def handle_system_error(e):
    print("Lỗi Server:", e)
    data = {
        "type": "about:blank",
        "title": "Internal Server Error",
        "status": 500,
        "detail": "Đã xảy ra lỗi hệ thống.",
        "instance": request.path
    }
    return jsonify(data), 500, {"Content-Type": "application/problem+json"}


@app.route("/resources/<int:id>")
def get_resource(id):
    if id != 1:
        raise ProblemError(
            status=404,
            title="Resource Not Found",
            detail=f"Không tìm thấy resource với id = {id}"
        )
    return jsonify({"id": 1, "name": "Item 1"})

@app.route("/test-500")
def test_500():
    return 1 / 0


if __name__ == "__main__":
    app.run(debug=True)