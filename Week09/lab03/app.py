from datetime import datetime, timezone
from os import environ

from flask import Flask

from sunset import deprecate_at

app = Flask(__name__)
SUNSET_DATE = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)


@app.get("/api/v1/users")
@deprecate_at(SUNSET_DATE, replacement="/api/v2/users")
def users_v1():
    return {"users": [{"id": 1, "full_name": "Văn Nguyễn"}]}


@app.get("/api/v2/users")
def users_v2():
    return {"users": [{"id": 1, "first_name": "Văn", "last_name": "Nguyễn"}]}


if __name__ == "__main__":
    demo_now = environ.get("SUNSET_DEMO_NOW")
    if demo_now:
        try:
            demo_time = datetime.fromisoformat(demo_now)
            if demo_time.utcoffset() is None:
                raise ValueError("timezone required")
        except ValueError:
            raise SystemExit("SUNSET_DEMO_NOW must be ISO 8601 with a timezone")
        app.config["SUNSET_DEMO_NOW"] = demo_time.astimezone(timezone.utc)
    app.run(port=5000)
