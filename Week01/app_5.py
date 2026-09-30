from flask import Flask, jsonify

ORDERS = {
    "1": {"status": "pending"},
    "2": {"status": "shipped"},
    "3": {"status": "delivered"},
}

app = Flask(__name__)

@app.route("/order/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = ORDERS.get(order_id)
    # 404 - Not found
    if order is None:
        return {"error": "not found"}, 404

    # 409 - business rule - đang giao thì không được xóa
    if order["status"] in ("shipped", "delivered"):
        return {"error": "cannot complete"}, 409

    ORDERS.pop(order_id, None)

    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)