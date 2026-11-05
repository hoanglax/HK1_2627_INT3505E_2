def test_create_product(client):
    response = client.post(
        "/api/v1/products/",
        json={
            "sku": "TEST00123",
            "name": "Test Product abc",
            "price_cents": 123456,
            "qty_in_stock": 67
        }
    )

    assert response.status_code == 201