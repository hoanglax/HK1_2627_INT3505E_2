from flask import Blueprint, request
from blueprints.user_data import get_user, create_user

bp = Blueprint("v2", __name__, url_prefix="/users")

@bp.route("/<int:uid>")
def get(uid):
    u = get_user(uid)

    if not u:
        return {"error": "nf"}, 404

    return {
        "first_name": u["first_name"],
        "last_name": u["last_name"],
        "email": u["email"]
    }

@bp.route("/", methods=["POST"])
def create():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "invalid JSON"}, 400

    required_fields = ["first_name", "last_name", "email"]

    for field in required_fields:
        if not isinstance(data.get(field), str):
            return {"error": "Missing or invalid fields"}, 400

        if data[field].strip() == "":
            return {"error": "Missing or invalid fields"}, 400

    uid, u = create_user(data)

    return {
        "id": uid,
        **u
    }, 201
