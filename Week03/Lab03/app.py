from flask import Flask, request, jsonify
import base64
import json

mock_orders = [
    {"id": 1, "code": "A001", "customer_id": 101, "status": "pending", "total": 100.0, "created_at": "2024-06-01 10:00:00"},
    {"id": 2, "code": "A002", "customer_id": 102, "status": "completed", "total": 150.0, "created_at": "2024-06-02 11:30:00"},
    {"id": 3, "code": "A003", "customer_id": 101, "status": "pending", "total": 200.0, "created_at": "2024-06-03 09:15:00"},
    {"id": 4, "code": "A004", "customer_id": 103, "status": "cancelled", "total": 75.0, "created_at": "2024-06-03 14:20:00"},
    {"id": 5, "code": "A005", "customer_id": 102, "status": "pending", "total": 300.0, "created_at": "2024-06-04 16:45:00"},
    {"id": 6, "code": "A006", "customer_id": 101, "status": "completed", "total": 250.0, "created_at": "2024-06-05 12:10:00"},
    {"id": 7, "code": "A007", "customer_id": 104, "status": "pending", "total": 180.0, "created_at": "2024-06-06 08:50:00"},
    {"id": 8, "code": "A008", "customer_id": 102, "status": "completed", "total": 220.0, "created_at": "2024-06-07 13:30:00"},
    {"id": 9, "code": "A009", "customer_id": 103, "status": "cancelled", "total": 90.0, "created_at": "2024-06-08 15:40:00"},
    {"id": 10, "code": "A010", "customer_id": 101, "status": "pending", "total": 400.0, "created_at": "2024-06-09 17:25:00"},
    {"id": 11, "code": "A011", "customer_id": 102, "status": "completed", "total": 350.0, "created_at": "2024-06-10 10:15:00"},
    {"id": 12, "code": "A012", "customer_id": 101, "status": "pending", "total": 120.0, "created_at": "2024-06-11 11:45:00"},
    {"id": 13, "code": "A013", "customer_id": 103, "status": "cancelled", "total": 60.0, "created_at": "2024-06-12 14:55:00"},
    {"id": 14, "code": "A014", "customer_id": 102, "status": "pending", "total": 280.0, "created_at": "2024-06-13 16:05:00"},
    {"id": 15, "code": "A015", "customer_id": 101, "status": "completed", "total": 320.0, "created_at": "2024-06-14 09:35:00"},
    {"id": 16, "code": "A016", "customer_id": 102, "status": "pending", "total": 150.0, "created_at": "2024-06-15 12:20:00"},
    {"id": 17, "code": "A017", "customer_id": 101, "status": "completed", "total": 200.0, "created_at": "2024-06-16 13:50:00"},
    {"id": 18, "code": "A018", "customer_id": 103, "status": "cancelled", "total": 80.0, "created_at": "2024-06-17 15:10:00"},
    {"id": 19, "code": "A019", "customer_id": 102, "status": "pending", "total": 270.0, "created_at": "2024-06-18 17:30:00"},
    {"id": 20, "code": "A020", "customer_id": 101, "status": "completed", "total": 300.0, "created_at": "2024-06-19 10:40:00"}
]

app = Flask(__name__)


@app.get("/orders")
def get_orders():
    status = request.args.get("status", default=None, type=str)
    customer_id = request.args.get("customer_id", default=None, type=int)
    total_min = request.args.get("total_min", default=None, type=float)
    total_max = request.args.get("total_max", default=None, type=float)
    sort = request.args.get("sort", default="-created_at,id", type=str)
    cursor = request.args.get("cursor", default=None, type=str)
    limit = request.args.get("limit", default=10, type=int)
    fields = request.args.get("fields", default=None, type=str)

    if limit < 1 or limit > 20:
        return jsonify({"error": "Limit must be between 1 and 20"}), 400

    # decode cursor
    decoded_cursor = None
    if cursor:
        try:
            decoded_cursor = json.loads(base64.b64decode(cursor).decode('utf-8'))
        except Exception:
            return jsonify({"error": "Invalid cursor"}), 400

    # filter
    filtered_orders = mock_orders.copy()
    if status:
        filtered_orders = [order for order in filtered_orders if order["status"] == status]
    if customer_id is not None:
        filtered_orders = [order for order in filtered_orders if order["customer_id"] == customer_id]
    # Tự làm thêm
    if total_min is not None:
        filtered_orders = [order for order in filtered_orders if order["total"] >= total_min]
    if total_max is not None:
        filtered_orders = [order for order in filtered_orders if order["total"] <= total_max]

    # sort
    is_descending = sort.startswith("-")
    filtered_orders.sort(
        key = lambda o: (o['created_at'], -o['id']) if is_descending else (o['created_at'], o['id']),
        reverse=is_descending
    )

    # cursor seek
    if decoded_cursor:
        last_created_at = decoded_cursor.get("created_at")
        last_id = decoded_cursor.get("id")

        seek_orders = []

        for order in filtered_orders:
            if is_descending:
                if order["created_at"] < last_created_at or (order["created_at"] == last_created_at and order["id"] < last_id):
                    seek_orders.append(order)
            else:
                if order["created_at"] > last_created_at or (order["created_at"] == last_created_at and order["id"] > last_id):
                    seek_orders.append(order)
        filtered_orders = seek_orders

    # limit 
    page_orders = filtered_orders[:limit + 1]
    has_more = len(page_orders) > limit
    if has_more:
        page_orders = page_orders[:limit]
        last_item = page_orders[-1]
        next_cursor = base64.b64encode(json.dumps({"created_at": last_item["created_at"], "id": last_item["id"]}).encode('utf-8')).decode('utf-8')
    else:
        next_cursor = None

    # sparse fields
    final_orders = []
    if fields:
        fields_list = [f.strip() for f in fields.split(",")]
        for order in page_orders:
            filtered_item = {k: v for k, v in order.items() if k in fields_list}
            final_orders.append(filtered_item)
    else:
        final_orders = page_orders

    # json response
    return jsonify({
        "data": final_orders,
        "pagination": {
            "limit": limit,
            "next_cursor": next_cursor,
            "has_more": has_more
        }
    }), 200


if __name__ == "__main__":
    app.run(debug=True)