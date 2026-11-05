from sqlalchemy import event
from src.extensions import db


def test_get_order_with_products(client, app):
    product_ids = []

    for i in range(3):
        response = client.post(
            "/api/v1/products/",
            json={
                "sku": f"ORD00{i + 1}",
                "name": f"Product {i + 1}",
                "price_cents": 100000,
                "qty_in_stock": 10
            }
        )
        assert response.status_code == 201
        product_ids.append(response.get_json()["id"])

    order_response = client.post(
        "/api/v1/orders/",
        json={
            "items": [
                {"product_id": product_id, "quantity": 2}
                for product_id in product_ids
            ]
        }
    )

    assert order_response.status_code == 201
    order_id = order_response.get_json()["id"]

    queries = []

    def count_queries(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            queries.append(statement)

    with app.app_context():
        event.listen(db.engine, "before_cursor_execute", count_queries)

        try:
            response = client.get(f"/api/v1/orders/{order_id}")
        finally:
            event.remove(db.engine, "before_cursor_execute", count_queries)

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["items"]) == 3
    assert all(item["product"] is not None for item in data["items"])
    assert len(queries) <= 3