# Kế hoạch triển khai: Hệ thống quản lý đồ án tốt nghiệp

## 1. Mục tiêu

Xây dựng ứng dụng web để khoa quản lý sinh viên, đề tài tốt nghiệp và việc sinh viên đăng ký đề tài. Hệ thống áp dụng kiến trúc hướng dịch vụ (SOA): các dịch vụ nghiệp vụ độc lập cung cấp REST API qua HTTP; giao diện web gọi các API này.

Trong phạm vi bài thực hành, ưu tiên một bản chạy được ở môi trường phát triển, có CRUD cho ba nhóm dữ liệu, quy tắc đăng ký rõ ràng, tài liệu API và hướng dẫn chạy. Chưa đặt mục tiêu triển khai quy mô lớn hay xác thực/phân quyền đầy đủ nếu đề bài không yêu cầu.

## 2. Khảo sát hiện trạng và giả định

- Backend có khung thư mục FastAPI theo lớp tại `be/app`: `routers`, `services`, `repositories`, `models`, `schemas`, `database`, `core`.
- Frontend là ứng dụng Angular tại `fe`; cần bổ sung màn hình và tích hợp REST API.
- Hiện chưa có mã nghiệp vụ, cấu hình cơ sở dữ liệu, migration hay đặc tả cột cho các bảng.
- Trước khi cài đặt, đối chiếu CSDL được cung cấp để chốt tên cột, kiểu dữ liệu, khóa chính/ngoại và ràng buộc. Không tự ý thay đổi schema nguồn.
- Nếu chưa có đặc tả bổ sung, dùng mô hình logic tối thiểu dưới đây làm giả định để thống nhất thiết kế; tên cột có thể ánh xạ sang tên thật trong CSDL.

## 3. Mô hình dữ liệu dự kiến

### SINHVIEN

- `ma_sinh_vien`: khóa chính, mã định danh duy nhất.
- `ho_ten`: bắt buộc.
- `email`: duy nhất nếu CSDL có trường này.
- Các thuộc tính bổ sung như lớp, ngành, số điện thoại: lấy theo schema được cung cấp.

### DETAI

- `ma_de_tai`: khóa chính.
- `ten_de_tai`: bắt buộc.
- `mo_ta`: nội dung mô tả, có thể rỗng.
- Các thuộc tính như giảng viên hướng dẫn, số lượng tối đa, trạng thái: lấy theo schema thực tế.

### DANGKY

- Khóa chính theo schema (hoặc khóa ghép được xác nhận).
- Khóa ngoại `ma_sinh_vien` tham chiếu `SINHVIEN`.
- Khóa ngoại `ma_de_tai` tham chiếu `DETAI`.
- Thuộc tính như ngày đăng ký/trạng thái nếu có trong CSDL.
- Bổ sung ràng buộc duy nhất phù hợp quy định, tối thiểu chống tạo bản ghi đăng ký trùng cho cùng sinh viên và đề tài. Quy tắc một đề tài cho mỗi sinh viên hoặc giới hạn số sinh viên/đề tài phải được xác nhận từ yêu cầu nghiệp vụ.

## 4. Kiến trúc và ranh giới dịch vụ

### Phương án cho bài thực hành

Tổ chức ba dịch vụ nghiệp vụ độc lập theo tài nguyên, mỗi dịch vụ có router, service, repository, schema/model riêng và giao tiếp bằng HTTP/REST:

1. **SinhVien Service**: quản lý và tra cứu sinh viên.
2. **DeTai Service**: quản lý và tra cứu đề tài.
3. **DangKy Service**: tạo, xem, hủy/cập nhật đăng ký; kiểm tra điều kiện bằng cách gọi SinhVien Service và DeTai Service.

Có thể đặt các dịch vụ trong cùng repository để dễ thực hành, nhưng chạy trên các tiến trình/cổng riêng để thể hiện rõ giao tiếp SOA. Ví dụ cổng cấu hình qua biến môi trường: sinh viên `8001`, đề tài `8002`, đăng ký `8003`. Angular gọi các endpoint qua cấu hình môi trường hoặc một gateway/proxy phát triển.

Mỗi dịch vụ sở hữu dữ liệu và schema của mình. Với CSDL bài tập dùng chung được cung cấp, có thể cùng kết nối một máy chủ CSDL nhưng phân định rõ quyền sở hữu bảng: SINHVIEN, DETAI, DANGKY tương ứng. Không truy cập trực tiếp repository/bảng của dịch vụ khác trong luồng nghiệp vụ; dùng API nội bộ. Nếu môi trường bài tập bắt buộc một ứng dụng FastAPI duy nhất, giữ nguyên ranh giới module và URL theo dịch vụ, đồng thời ghi đây là cách mô phỏng SOA trong một tiến trình.

### Luồng đăng ký đề tài

1. Client gửi yêu cầu đăng ký tới DangKy Service.
2. DangKy Service kiểm tra sinh viên và đề tài tồn tại qua API của hai dịch vụ.
3. Service kiểm tra các quy tắc đăng ký đã chốt.
4. Repository ghi đăng ký và trả kết quả.
5. API chuẩn hóa lỗi từ dịch vụ phụ thuộc (timeout/không khả dụng) thành phản hồi có ý nghĩa; không tạo bản ghi khi chưa xác minh điều kiện.

Với nhiều dịch vụ và một CSDL dùng chung, thao tác kiểm tra rồi ghi có thể phát sinh tranh chấp đồng thời. Dùng ràng buộc duy nhất/khóa ngoại ở CSDL làm lớp bảo vệ cuối; giao dịch CSDL trong DangKy Service; xử lý lỗi ràng buộc thành `409 Conflict`. Không triển khai distributed transaction trong phạm vi cơ bản.

## 5. Thiết kế API dự kiến

Dùng JSON, tiền tố phiên bản `/api/v1`, mã HTTP theo ngữ nghĩa và tài liệu OpenAPI. Tên trường cuối cùng phải khớp hợp đồng dữ liệu đã thống nhất.

### SinhVien Service

- `GET /api/v1/sinhviens`: danh sách, hỗ trợ tìm kiếm/phân trang nếu cần.
- `GET /api/v1/sinhviens/{ma_sinh_vien}`: chi tiết.
- `POST /api/v1/sinhviens`: tạo.
- `PUT /api/v1/sinhviens/{ma_sinh_vien}`: cập nhật.
- `DELETE /api/v1/sinhviens/{ma_sinh_vien}`: xóa khi không vi phạm khóa ngoại; nếu đang có đăng ký thì trả `409` hoặc áp dụng chính sách đã chốt.

### DeTai Service

- `GET /api/v1/detais`: danh sách, có thể lọc theo tên/trạng thái.
- `GET /api/v1/detais/{ma_de_tai}`: chi tiết.
- `POST /api/v1/detais`: tạo.
- `PUT /api/v1/detais/{ma_de_tai}`: cập nhật.
- `DELETE /api/v1/detais/{ma_de_tai}`: xóa khi không vi phạm khóa ngoại; chính sách khi đã có đăng ký cần chốt.

### DangKy Service

- `GET /api/v1/dang-ky`: danh sách đăng ký, hỗ trợ lọc theo mã sinh viên/đề tài.
- `GET /api/v1/dang-ky/{id}` hoặc định danh khóa ghép theo schema.
- `POST /api/v1/dang-ky`: tạo đăng ký.
- `DELETE /api/v1/dang-ky/{id}`: hủy đăng ký nếu nghiệp vụ cho phép.
- Endpoint truy vấn đăng ký theo sinh viên hoặc đề tài nếu cần cho giao diện.

### Quy ước chung

- `200` đọc/cập nhật thành công; `201` tạo thành công; `204` xóa thành công; `400/422` dữ liệu không hợp lệ; `404` không tìm thấy; `409` trùng mã/vi phạm quy tắc; `502/503` dịch vụ phụ thuộc lỗi hoặc không sẵn sàng.
- Dùng schema riêng cho request/response, không trả trực tiếp ORM object.
- Trả lỗi nhất quán, không để lộ thông tin kết nối hay stack trace.

## 6. Kế hoạch thực hiện theo giai đoạn

### Giai đoạn 1: Chốt yêu cầu và CSDL

- Mở script/schema CSDL được giao; lập bảng đối chiếu cột, kiểu dữ liệu, nullability, khóa và ràng buộc.
- Chốt quy tắc đăng ký: mỗi sinh viên được chọn bao nhiêu đề tài, giới hạn người/đề tài, trạng thái đăng ký, cách hủy và sửa.
- Chốt cách chạy dịch vụ (nhiều tiến trình hay một tiến trình mô phỏng) và cấu hình DB.
- Đầu ra: mô tả schema, quy tắc nghiệp vụ và danh sách API.

### Giai đoạn 2: Nền tảng backend và kết nối CSDL

- Bổ sung cấu hình từ biến môi trường, URL CSDL và kiểm tra kết nối khi khởi động.
- Chọn ORM/driver theo loại CSDL được cấp; ánh xạ mô hình đúng schema có sẵn, không tạo lại hoặc sửa dữ liệu nguồn ngoài ý muốn.
- Tạo quản lý session/connection, xử lý lỗi chung và health endpoint.
- Nếu cần thay đổi schema, quản lý bằng migration có thể lặp lại; nếu schema cố định, chỉ tạo script kiểm tra/seed dữ liệu mẫu riêng.

### Giai đoạn 3: SinhVien Service và DeTai Service

- Tạo model, schema, repository, service và router theo khung `be/app`.
- Cài đặt CRUD, tìm kiếm tối thiểu, kiểm tra trùng khóa và quy tắc xóa.
- Cấu hình chạy độc lập và OpenAPI cho từng dịch vụ.

### Giai đoạn 4: DangKy Service

- Cài đặt CRUD/query đăng ký.
- Gọi REST API của SinhVien và DeTai Service qua URL cấu hình; đặt timeout và chuẩn hóa lỗi.
- Kiểm tra tồn tại, trùng đăng ký và các giới hạn nghiệp vụ đã chốt.
- Ghi dữ liệu trong transaction, dựa vào khóa ngoại/ràng buộc DB để bảo vệ nhất quán khi có yêu cầu đồng thời.

### Giai đoạn 5: Frontend Angular

- Tạo lớp API client/service riêng cho sinh viên, đề tài, đăng ký; cấu hình base URL qua environment/proxy.
- Xây dựng màn hình danh sách, xem/tìm kiếm, thêm/sửa/xóa sinh viên và đề tài.
- Xây dựng màn hình tạo/xem/hủy đăng ký; cung cấp lựa chọn sinh viên và đề tài từ API.
- Hiển thị trạng thái tải, lỗi mạng/API, lỗi validation và xác nhận trước khi xóa/hủy.
- Làm rõ với người dùng khi DangKy Service không thể truy cập dịch vụ phụ thuộc.

### Giai đoạn 6: Tài liệu, tích hợp và bàn giao

- Viết hướng dẫn cài đặt, cấu hình `.env.example`, lệnh chạy từng dịch vụ và frontend.
- Mô tả sơ đồ kiến trúc, luồng đăng ký, bảng dữ liệu, endpoint, request/response mẫu và mã lỗi.
- Chuẩn bị dữ liệu mẫu có thể lặp lại và hướng dẫn reset môi trường phát triển.
- Kiểm tra thủ công luồng đầu cuối: tạo sinh viên, tạo đề tài, đăng ký, xem đăng ký, từ chối dữ liệu sai/trùng, xử lý khi dịch vụ phụ thuộc dừng.

## 7. Cấu trúc mã dự kiến

```text
be/
  app/
    main.py
    core/                 # settings, lỗi và HTTP client nội bộ
    database/             # engine/session hoặc client DB
    models/               # ánh xạ SINHVIEN, DETAI, DANGKY
    schemas/              # hợp đồng REST
    repositories/         # thao tác dữ liệu
    services/             # nghiệp vụ; DangKy gọi API dịch vụ khác
    routers/              # endpoint theo nhóm tài nguyên
  tests/
  requirements.txt
fe/
  src/app/
    core/                 # cấu hình và API clients
    features/             # sinh viên, đề tài, đăng ký
```

Nếu cần tách thành ba ứng dụng FastAPI chạy độc lập, nhóm module theo service và tạo entrypoint/config cho từng ứng dụng; tránh nhân bản logic kết nối và xử lý lỗi.

## 8. Cấu hình và vận hành phát triển

- Cấu hình tối thiểu: URL kết nối DB; `SINHVIEN_SERVICE_URL`; `DETAI_SERVICE_URL`; cổng từng API; origin frontend được phép qua CORS.
- Không commit mật khẩu/secret. Cung cấp `.env.example` với giá trị minh họa.
- Chạy backend và frontend trên các cổng riêng; ghi rõ thứ tự khởi động và trạng thái phụ thuộc.
- Health endpoint nên báo trạng thái ứng dụng và kết nối DB; DangKy Service có thể cung cấp trạng thái phụ thuộc ở mức tổng quát.

## 9. Tiêu chí hoàn thành

- Ba bảng được ánh xạ đúng CSDL được cung cấp, bảo toàn khóa và ràng buộc.
- Các thao tác CRUD cần thiết hoạt động qua REST API; dữ liệu đầu vào/đầu ra được kiểm tra và tài liệu hóa.
- Tạo đăng ký chỉ thành công khi sinh viên và đề tài hợp lệ, không vi phạm các giới hạn đã thống nhất; dữ liệu trùng bị từ chối ổn định.
- DangKy Service giao tiếp HTTP với hai dịch vụ còn lại, có timeout và phản hồi lỗi phù hợp.
- Frontend có thể quản lý sinh viên, đề tài và đăng ký qua API, hiển thị được thành công/lỗi.
- Người khác có thể dựng môi trường theo README và kiểm tra luồng mẫu bằng giao diện hoặc Swagger UI.

## 10. Rủi ro và quyết định cần xác nhận

- **Schema không đầy đủ trong đề bài tóm tắt:** đối chiếu CSDL thật trước khi đặt tên cột/kiểu và khóa.
- **Quy tắc đăng ký chưa nêu:** cần quyết định giới hạn sinh viên/đề tài và trạng thái trước khi cài logic.
- **Giao tiếp dịch vụ và dùng chung CSDL:** dùng chung một DB phù hợp bài thực hành nhưng giảm độc lập triển khai; nếu yêu cầu SOA nghiêm ngặt, mỗi service sở hữu DB riêng và DangKy giữ mã tham chiếu, không dùng khóa ngoại xuyên DB.
- **Xóa dữ liệu đã liên kết:** xác định chính sách từ chối xóa, lưu trữ mềm hay cascade; mặc định an toàn là từ chối xóa khi còn đăng ký.
- **Dịch vụ phụ thuộc tạm dừng:** đặt timeout, trả lỗi phụ thuộc rõ ràng và không ghi đăng ký dở dang.
