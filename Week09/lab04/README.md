# Lab04 — Blue-Green Routing

`POST /orders` nhận JSON có trường `account_id` là chuỗi. Gateway kiểm tra cohort `beta` hoặc `internal` trước, rồi kiểm tra allow-list `acct_42` và `acct_99`. Với các account còn lại, gateway lấy MD5 của account ID, đổi sang số nguyên và lấy phần dư chia 100. Bucket nhỏ hơn `V2_PERCENT` được chuyển sang v2.

## Chạy trên Windows CMD

```cmd
cd /d D:\HK1_2627_INT3505E_2\Week09\lab04
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install Flask
set PYTHONDONTWRITEBYTECODE=1
set "V2_PERCENT="
python app.py
```

Nếu một lab khác đang dùng cổng 5000, dừng lab đó trước. Mở cửa sổ CMD thứ hai và chạy:

```cmd
curl.exe -i -H "Content-Type: application/json" -d "{\"account_id\":\"acct_1\"}" http://127.0.0.1:5000/orders
curl.exe -i -H "Content-Type: application/json" -d "{\"account_id\":\"acct_72\"}" http://127.0.0.1:5000/orders
curl.exe -i -H "Content-Type: application/json" -H "X-Cohort: beta" -d "{\"account_id\":\"acct_1\"}" http://127.0.0.1:5000/orders
curl.exe -i -H "Content-Type: application/json" -d "{\"account_id\":\"acct_42\"}" http://127.0.0.1:5000/orders
curl.exe -i -H "Content-Type: application/json" -d "{}" http://127.0.0.1:5000/orders
```

| Yêu cầu | HTTP ở 5% | X-Order-Handler | JSON mong đợi |
| --- | --- | --- | --- |
| acct_1, bucket 53 | 200 | v1 | `{"account_id":"acct_1","status":"accepted"}` |
| acct_72, bucket 3 | 201 | v2 | `{"account_id":"acct_72","status":"created"}` |
| acct_1 với cohort beta | 201 | v2 | `{"account_id":"acct_1","status":"created"}` |
| acct_42 thuộc allow-list | 201 | v2 | `{"account_id":"acct_42","status":"created"}` |
| Thiếu account_id | 400 | Vắng mặt | `{"error":"account_id must be a non-empty string"}` |

## Đổi mức rollout

Dừng server bằng Ctrl+C, rồi khởi động lại với mức mong muốn.

```cmd
set "V2_PERCENT=0"
python app.py
```

Với 0%, hai lệnh theo bucket trả 200, hai lệnh ưu tiên vẫn trả 201. Dừng server và chạy:

```cmd
set "V2_PERCENT=100"
python app.py
```

Với 100%, cả bốn lệnh hợp lệ trả 201. Lệnh thiếu account vẫn trả 400 ở cả hai mức. Dùng `set "V2_PERCENT="` để quay về mặc định 5%.

## Kiểm thử tự động

```cmd
.venv\Scripts\python.exe -B -m unittest -v
```
