import re

from flask import Blueprint, request

from blueprints.user_data import create_user, get_user

bp = Blueprint("v2", __name__, url_prefix="/api/v2/users")


@bp.route("/<int:uid>")
def get(uid):
    user = get_user(uid)
    if user is None:
        return {"error": "nf"}, 404

    return {"id": uid, **user}


@bp.route("/", methods=["POST"])
def create():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"error": "invalid JSON"}, 400

    for field in ("first_name", "last_name", "email"):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            return {"error": "Missing or invalid fields"}, 400
        data[field] = value.strip()

    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", data["email"]):
        return {"error": "Invalid email"}, 400

    uid, user = create_user(data)
    return {"id": uid, **user}, 201
