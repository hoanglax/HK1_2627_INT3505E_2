# Lab01 — URI Path Versioning

Hai Flask Blueprint dùng chung bảng `USERS` trong bộ nhớ. V1 trả về `full_name` và gửi header vòng đời. V2 tách tên thành hai trường và hỗ trợ tạo user. Dữ liệu tạo thêm mất khi khởi động lại ứng dụng.

## Chạy trên Windows CMD

```cmd
cd /d D:\HK1_2627_INT3505E_2\Week09\lab01
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install Flask
set PYTHONDONTWRITEBYTECODE=1
python app.py
```

## Demo từ cửa sổ CMD khác

```cmd
curl.exe -i http://127.0.0.1:5000/api/v1/users/1
curl.exe -i http://127.0.0.1:5000/api/v2/users/1
curl.exe -i http://127.0.0.1:5000/api/v2/users/999
curl.exe -i -H "Content-Type: application/json" -d "{\"first_name\":\"An\",\"last_name\":\"Le\",\"email\":\"an@example.com\"}" http://127.0.0.1:5000/api/v2/users/
curl.exe -i http://127.0.0.1:5000/api/v1/users/3
curl.exe -i -H "Content-Type: application/json" -d "{\"first_name\":\"An\",\"last_name\":\"Le\",\"email\":\"invalid\"}" http://127.0.0.1:5000/api/v2/users/
```

| Lệnh | Kết quả mong đợi |
| --- | --- |
| GET v1 user 1 | `200` với `id`, `full_name`, `email` và hai header `Deprecation: true`, `Sunset: Thu, 31 Dec 2026 23:59:59 GMT` |
| GET v2 user 1 | `200` với `id`, `first_name`, `last_name`, `email` |
| GET v2 user 999 | `404` và `{"error":"nf"}` |
| POST hợp lệ | `201` và thông tin An Le, `id` là `3` nếu đây là lần tạo đầu tiên |
| GET v1 user 3 | `200` với `full_name` là `An Le` sau lần tạo đầu tiên |
| POST email sai | `400` và `{"error":"Invalid email"}` |

## Kiểm thử tự động

Chạy trong thư mục lab01 với môi trường ảo đã tạo.

```cmd
.venv\Scripts\python.exe -B -m unittest -v
```

Đặc tả API nằm trong `openapi.yaml`.
