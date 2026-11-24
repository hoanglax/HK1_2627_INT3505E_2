from datetime import datetime, timezone
from email.utils import format_datetime

from flask import Blueprint

from blueprints.user_data import get_user

bp = Blueprint("v1", __name__, url_prefix="/api/v1/users")
SUNSET_DATE = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)


@bp.after_request
def add_deprecation_headers(response):
    response.headers["Sunset"] = format_datetime(SUNSET_DATE, usegmt=True)
    response.headers["Deprecation"] = "true"
    return response


@bp.route("/<int:uid>")
def get(uid):
    user = get_user(uid)
    if user is None:
        return {"error": "nf"}, 404

    return {
        "id": uid,
        "full_name": f"{user['first_name']} {user['last_name']}",
        "email": user["email"],
    }
