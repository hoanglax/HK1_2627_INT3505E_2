from functools import wraps

from flask import Flask, make_response, request

app = Flask(__name__)

VERSION_HEADER = "X-API-Version"
SERVED_HEADER = "X-API-Version-Served"
SUPPORTED_VERSIONS = {"1", "2", "2024-06-20"}
DEFAULT_VERSION = "2"

USERS = {
    1: {"first_name": "Văn", "last_name": "Nguyễn", "email": "a@vnu.vn"},
    2: {"first_name": "Trang", "last_name": "Trần", "email": "b@vnu.vn"},
}


def api_version(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        version = request.headers.get(VERSION_HEADER, DEFAULT_VERSION)
        if version in SUPPORTED_VERSIONS:
            response = make_response(view(*args, version=version, **kwargs))
            response.headers[SERVED_HEADER] = version
        else:
            response = make_response({"error": "Unsupported API version"}, 400)

        response.vary.add(VERSION_HEADER)
        return response

    return wrapped


@app.get("/users/<int:uid>")
@api_version
def get_user(uid, version):
    user = USERS.get(uid)
    if user is None:
        return {"error": "User not found"}, 404

    if version == "1":
        return {"id": uid, "full_name": f"{user['first_name']} {user['last_name']}"}

    return {"id": uid, **user}


if __name__ == "__main__":
    app.run(port=5000)
