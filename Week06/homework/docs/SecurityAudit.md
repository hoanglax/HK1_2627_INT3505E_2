# Security Audit – Đánh giá bảo mật API Mạng xã hội

## 1. Các vị trí có nguy cơ làm lộ thông tin

| STT | Vị trí có nguy cơ | Rủi ro | Biện pháp phòng tránh |
|---|---|---|---|
| 1 | Log của API đăng nhập | Email và mật khẩu có thể bị lộ nếu hệ thống ghi lại toàn bộ nội dung request. | Không ghi log mật khẩu hoặc toàn bộ nội dung request đăng nhập. |
| 2 | Access Token trong log hệ thống | Kẻ tấn công có thể lấy JWT từ log và sử dụng để giả mạo người dùng. | Che hoặc loại bỏ thông tin trong header Authorization trước khi ghi log. |
| 3 | Nơi lưu trữ Refresh Token | Nếu Refresh Token bị đánh cắp, kẻ tấn công có thể sử dụng nó để xin Access Token mới. | Lưu trữ Refresh Token an toàn, chỉ lưu giá trị băm ở phía server khi phù hợp, hỗ trợ thu hồi và thay mới token. |
| 4 | Tham số trên URL | Token hoặc dữ liệu nhạy cảm trong URL có thể xuất hiện trong lịch sử trình duyệt, log server hoặc HTTP Referer. | Không truyền token qua URL. Sử dụng HTTP Header hoặc request body phù hợp. |
| 5 | localStorage trên trình duyệt | Nếu ứng dụng bị tấn công XSS, mã độc JavaScript có thể đọc và đánh cắp token. | Ưu tiên cookie có thuộc tính HttpOnly, Secure, SameSite khi phù hợp; đồng thời triển khai biện pháp phòng chống XSS. |
| 6 | Thông báo lỗi đăng nhập | Thông báo quá chi tiết có thể giúp kẻ tấn công xác định email nào đã đăng ký tài khoản. | Sử dụng thông báo lỗi chung như "Email hoặc mật khẩu không chính xác". |
| 7 | Dữ liệu bài viết và phản hồi API | Bài viết riêng tư hoặc thông tin cá nhân có thể bị lộ nếu thiếu kiểm tra quyền truy cập. | Kiểm tra scope và quyền truy cập đối với từng bài viết trước khi trả dữ liệu. |
| 8 | Công cụ debug và giám sát hệ thống | Báo cáo lỗi, hệ thống phân tích hoặc công cụ giám sát có thể thu thập token, mật khẩu và dữ liệu cá nhân. | Loại bỏ hoặc che dữ liệu nhạy cảm trước khi gửi log và giới hạn quyền truy cập các công cụ giám sát. |

## 2. Các biện pháp bảo mật bổ sung

- Sử dụng HTTPS cho toàn bộ quá trình giao tiếp giữa client và server.
- Giới hạn số lần gửi request đến `/auth/login` và `/auth/refresh` để hạn chế brute-force và lạm dụng API.
- Sử dụng thuật toán băm mật khẩu an toàn như Argon2id hoặc bcrypt.
- Kiểm tra chữ ký JWT và các claim quan trọng như `exp` (thời hạn), `iss` (bên phát hành), `aud` (đối tượng nhận).
- Thiết lập thời hạn ngắn cho Access Token.
- Thay mới và thu hồi Refresh Token khi được sử dụng hoặc khi phát hiện bị xâm phạm.
- Không trả về stack trace hoặc thông tin chi tiết về cơ sở dữ liệu trong thông báo lỗi API.
- Kiểm tra quyền truy cập ở cấp độ từng đối tượng để phòng chống lỗ hổng BOLA.

## 3. Kết luận

Các rủi ro bảo mật chính của API mạng xã hội bao gồm:

- Rò rỉ thông tin đăng nhập.
- Đánh cắp Access Token và Refresh Token.
- Cơ chế xác thực không đủ an toàn.
- Truy cập trái phép vào bài viết riêng tư của người dùng khác.

Hệ thống cần bảo vệ thông tin nhạy cảm trong toàn bộ quá trình xác thực, quản lý token, ghi log và kiểm tra quyền truy cập tài nguyên.