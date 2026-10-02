# Triển khai /orders có cursor pagination

Dữ liệu giả lập (mock_orders) có cấu trúc như sau:
{"id": 1, "code": "A001", "customer_id": 101, "status": "pending", "total": 100.0, "created_at": "2024-06-01 10:00:00"},

Trong đó "status" gồm: pending, completed, cancelled

## Kiểm thử

### Với các status:
- status=completed
![alt text](image.png)

- status=pending
![alt text](image-1.png)

- status=cancelled
![alt text](image-2.png)

### Với limit
