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
Limit nằm trong khoảng [1..20], danh sách mặc định là mới nhất trước.

- Khi chọn đúng khoảng limit
![alt text](image-3.png)

- Khi chọn ngoài khoảng hợp lệ
![alt text](image-4.png)

### Sparse Fieldsets 
- Giữ đúng 2 trường id, total (limit default = 10)
![alt text](image-5.png)

### Kết hợp 4 trường
![alt text](image-6.png)

### Cursor hỏng - 400 
![alt text](image-7.png)