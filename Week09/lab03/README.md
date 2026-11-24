# Lab03 — Sunset Middleware

Decorator `@deprecate_at` áp dụng cho `GET /api/v1/users`. Trước **2026-12-31 23:59:59 UTC**, v1 vẫn trả dữ liệu. Từ đúng mốc sunset, v1 trả `410 Gone` và chỉ đường sang `GET /api/v2/users`. Mỗi lần gọi v1 đều ghi log ở mức WARNING.

## Cài đặt trên Windows CMD

```cmd
cd /d D:\HK1_2627_INT3505E_2\Week09\lab03
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install Flask
set PYTHONDONTWRITEBYTECODE=1
```

## Demo trước và sau sunset

Chạy trong cửa sổ CMD đã kích hoạt môi trường ảo. Dừng lab khác nếu đang dùng cổng 5000.

```cmd
set "SUNSET_DEMO_NOW=2026-12-31T23:59:58+00:00"
python app.py
```

Trong cửa sổ CMD thứ hai, chạy:

```cmd
curl.exe -i http://127.0.0.1:5000/api/v1/users
curl.exe -i http://127.0.0.1:5000/api/v2/users
```

Hai lệnh đều trả `200 OK`. V1 trả `full_name` và các header sau:

```http
Sunset: Thu, 31 Dec 2026 23:59:59 GMT
Deprecation: true
Link: </api/v2/users>; rel="successor-version"
```

Dừng server bằng Ctrl+C và khởi động lại trong cửa sổ thứ nhất:

```cmd
set "SUNSET_DEMO_NOW=2027-01-01T00:00:00+00:00"
python app.py
```

Chạy lại hai lệnh curl. V1 trả `410 Gone`, vẫn có ba header trên và trả JSON sau. V2 vẫn trả `200 OK` với `first_name` và `last_name`.

```json
{"error":"Endpoint has been retired","sunset":"2026-12-31T23:59:59+00:00","replacement":"/api/v2/users"}
```

Dùng `set "SUNSET_DEMO_NOW="` trước khi khởi động để trở về thời gian UTC thực.

## Kiểm thử tự động

```cmd
.venv\Scripts\python.exe -B -m unittest -v
```
