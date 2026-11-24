# Lab02 — Header Versioning

Một endpoint `GET /users/{id}` chọn phiên bản theo header `X-API-Version`. Decorator `@api_version` giữ metadata của hàm bằng `functools.wraps` và mặc định chọn `2` khi thiếu header.

## Chạy trong Windows CMD

```cmd
cd /d D:\HK1_2627_INT3505E_2\Week09\lab02
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install Flask
set PYTHONDONTWRITEBYTECODE=1
python app.py
```

Dừng lab01 nếu nó đang dùng cổng 5000. Trong cửa sổ CMD thứ hai, chạy:

```cmd
curl.exe -i -H "X-API-Version: 1" http://127.0.0.1:5000/users/1
curl.exe -i -H "X-API-Version: 2" http://127.0.0.1:5000/users/1
curl.exe -i -H "X-API-Version: 2024-06-20" http://127.0.0.1:5000/users/1
curl.exe -i http://127.0.0.1:5000/users/1
curl.exe -i -H "X-API-Version: 3" http://127.0.0.1:5000/users/1
curl.exe -i -H "X-API-Version: 1" http://127.0.0.1:5000/users/999
```

| Yêu cầu | HTTP | `X-API-Version-Served` | JSON mong đợi |
| --- | --- | --- | --- |
| Version `1` | 200 | `1` | `{"id":1,"full_name":"Văn Nguyễn"}` |
| Version `2` | 200 | `2` | `{"id":1,"first_name":"Văn","last_name":"Nguyễn","email":"a@vnu.vn"}` |
| Version `2024-06-20` | 200 | `2024-06-20` | Cùng nội dung version `2` |
| Thiếu header | 200 | `2` | Cùng nội dung version `2` |
| Version `3` | 400 | Vắng mặt | `{"error":"Unsupported API version"}` |
| User `999` với version `1` | 404 | `1` | `{"error":"User not found"}` |

Các phản hồi của endpoint có `Vary: X-API-Version` để cache phân biệt các phiên bản.

## Kiểm thử tự động

```cmd
.venv\Scripts\python.exe -B -m unittest -v
```
