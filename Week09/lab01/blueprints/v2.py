from flask import Blueprint
from blueprints.user_data import get_user

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

