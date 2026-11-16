# Lab 4 — Phân tích kết quả

| Kịch bản | Users | Spawn rate | Duration | p95 (ms) | Failure rate | RPS |
|---|---:|---:|---:|---:|---:|---:|
| A | 10 | 2 | 30s | 21 | 0% | 4.75 |
| B | 50 | 5 | 60s | 24 | 0% | 23.39 |
| C | 200 | 50 | 30s | 72 | 0% | 97.98 |

1. Kịch bản có p95 cao nhất là gì? Dùng số liệu quan sát để giải thích.
Kịch bản C có p95 cao nhất, đạt 72 ms, so với 21 ms ở kịch bản A và 24 ms ở kịch bản B.

Khi tăng số người dùng ảo từ 10 lên 200, p95 tăng khoảng 3,43 lần. Kết quả này cho thấy thời gian phản hồi ở nhóm request chậm có xu hướng tăng khi tải lớn hơn. Nguyên nhân có thể liên quan đến xử lý tài nguyên và khả năng xử lý đồng thời của Flask/SQLite.

2. Endpoint nào tăng failure rate? Phân biệt lỗi HTTP thực và lỗi đánh dấu trong Locust.
Trong cả ba kịch bản A, B và C, failure rate ghi nhận đều bằng 0%. Vì vậy, không có endpoint nào được quan sát thấy tăng failure rate.

Phân biệt hai loại lỗi:

Lỗi HTTP: Server trả về mã lỗi như HTTP 500 hoặc HTTP 503 do gặp sự cố xử lý. Những lỗi này phản ánh phản hồi thực tế của server.

Lỗi đánh dấu trong Locust: Khi sử dụng catch_response=True, có thể gọi response.failure() để đánh dấu một request thất bại theo tiêu chí kiểm thử, ngay cả khi server không trả về HTTP 500.

3. Với SLO giả định p95 < 300 ms, kịch bản nào đạt? Nêu giới hạn của phép đo.
Cả ba kịch bản đều đạt SLO giả định về thời gian phản hồi:

|Kịch bản|p95|Kết quả|
|A|21 ms|Đạt|
|B|24 ms|Đạt|
|C|72 ms|Đạt|

Tất cả giá trị p95 đều nhỏ hơn 300 ms.

Phép đo có những giới hạn:
- Thời gian chạy tương đối ngắn, chỉ từ 30 đến 60 giây.
- Hệ thống sử dụng Flask development server và SQLite trên máy cá nhân.
- Chưa đánh giá tải kéo dài, mức sử dụng CPU, RAM và I/O.
- Số lượng người dùng ảo không tương đương trực tiếp với số người dùng thực tế.
- Dữ liệu và cách phân phối request trong thử nghiệm có thể khác môi trường production.

4. Nếu connection pool bị giới hạn ở 5, bạn sẽ kiểm chứng ảnh hưởng như thế nào?
Để kiểm chứng ảnh hưởng của việc giới hạn connection pool xuống 5 kết nối, có thể thực hiện thử nghiệm đối chứng:

- Giữ nguyên ứng dụng, dữ liệu thử nghiệm và cấu hình Locust.

- Chạy lại các kịch bản A, B, C với cấu hình connection pool hiện tại để lấy số liệu đối chứng.

- Cấu hình connection pool của SQLAlchemy với pool_size=5 và kiểm soát số kết nối vượt mức bằng max_overflow=0, nếu loại pool đang sử dụng hỗ trợ các tham số này.

- Chạy lại các kịch bản với cùng Users, Spawn rate và Duration.

- So sánh p95, RPS, failure rate và kiểm tra log để phát hiện thời gian chờ kết nối hoặc lỗi timeout.

Nếu pool trở thành điểm nghẽn, có thể quan sát thấy p95 tăng, RPS bị giới hạn hoặc xuất hiện lỗi timeout khi nhiều request cần truy cập database đồng thời.

> Không điền số liệu giả định vào bảng. Không khẳng định hiệu năng production
> từ SQLite + Flask development server trên máy cá nhân.
