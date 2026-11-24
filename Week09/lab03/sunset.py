from datetime import datetime, timezone
from email.utils import format_datetime
from functools import wraps

from flask import current_app, make_response, request


def deprecate_at(sunset_date, replacement=None):
    if sunset_date.utcoffset() is None:
        raise ValueError("sunset_date must include a timezone")

    sunset_utc = sunset_date.astimezone(timezone.utc)
    sunset_header = format_datetime(sunset_utc, usegmt=True)

    def decorate(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            current_app.logger.warning(
                "Deprecated endpoint called: %s %s", request.method, request.path
            )
            now = current_app.config.get("SUNSET_DEMO_NOW")
            if now is None:
                now = datetime.now(timezone.utc)

            if now >= sunset_utc:
                response = make_response({
                    "error": "Endpoint has been retired",
                    "sunset": sunset_utc.isoformat(),
                    "replacement": replacement,
                }, 410)
            else:
                response = make_response(view(*args, **kwargs))

            response.headers["Sunset"] = sunset_header
            response.headers["Deprecation"] = "true"
            if replacement is not None:
                response.headers["Link"] = f'<{replacement}>; rel="successor-version"'
            return response

        return wrapped

    return decorate
