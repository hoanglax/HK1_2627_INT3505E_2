from os import environ

from flask import Flask, request

from gateway import select_handler

app = Flask(__name__)
V2_PERCENT = 5
app.config["V2_PERCENT"] = V2_PERCENT


@app.post("/orders")
def create_order():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"error": "Expected a JSON object"}, 400

    account_id = data.get("account_id")
    if not isinstance(account_id, str) or not account_id.strip():
        return {"error": "account_id must be a non-empty string"}, 400

    account_id = account_id.strip()
    handler = select_handler(
        request.headers.get("X-Cohort"), account_id, app.config["V2_PERCENT"]
    )
    return handler(account_id)


if __name__ == "__main__":
    try:
        percent = int(environ.get("V2_PERCENT", V2_PERCENT))
        if not 0 <= percent <= 100:
            raise ValueError
    except ValueError:
        raise SystemExit("V2_PERCENT must be an integer between 0 and 100")

    app.config["V2_PERCENT"] = percent
    app.run(port=5000)
