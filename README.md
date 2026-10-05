# Quản lý đồ án tốt nghiệp

Ứng dụng quản lý sinh viên, đề tài tốt nghiệp và đăng ký đề tài. Frontend Angular gọi REST API của ba tiến trình FastAPI. Các dịch vụ dùng chung MySQL trong phạm vi bài thực hành.

## Kiến trúc SOA

```mermaid
flowchart LR
    User[Người dùng] --> FE[Angular Web<br/>localhost:4200]
    FE --> SA[StudentApi Service]
    FE --> TA[TopicApi Service]
    FE --> RA[RegistrationApi Service]
    SA -->|HTTP REST :8001| SS[SinhVien Service<br/>FastAPI]
    TA -->|HTTP REST :8002| TS[DeTai Service<br/>FastAPI]
    RA -->|HTTP REST :8003| RS[DangKy Service<br/>FastAPI]
    RS -->|HTTP kiểm tra sinh viên| SS
    RS -->|HTTP kiểm tra đề tài| TS
    SS --> DB[(MySQL · demo_quan_ly_do_an<br/>SINHVIEN · DETAI · DANGKY)]
```

`StudentApi`, `TopicApi` và `RegistrationApi` là Angular services quản lý HTTP client tương ứng. `App` giữ trạng thái màn hình và điều phối thao tác từ các component. Backend hiện chạy ba tiến trình độc lập theo biến `SERVICE_NAME`; các tiến trình dùng chung database `demo_quan_ly_do_an`. `DangKy Service` gọi HTTP đến hai dịch vụ còn lại để xác minh dữ liệu trước khi ghi đăng ký.

## Yêu cầu

- MySQL 8.x
- Python 3.10 trở lên và `pip`
- Node.js tương thích với Angular 21 và npm

## 1. Tạo database

Mở `database.sql` trong MySQL Workbench và chạy script. Script tạo database `demo_quan_ly_do_an`, ba bảng cùng dữ liệu sinh viên/đề tài mẫu. Script không xóa database hiện có.

`cryptography` trong backend requirements cần thiết để PyMySQL xác thực với MySQL 8 khi tài khoản dùng `caching_sha2_password`.

Backend tự đọc cấu hình từ `be/.env`. Hãy tạo file này một lần với tài khoản MySQL của bạn; ví dụ:

```powershell
DATABASE_URL=mysql+pymysql://your_user:your_password@127.0.0.1:3306/demo_quan_ly_do_an?charset=utf8mb4
```

Thay user/password bằng thông tin thật. `be/.env` đã được thêm vào `.gitignore`; không commit file chứa mật khẩu. Nếu mật khẩu có ký tự đặc biệt như `@`, `#` hoặc `%`, hãy URL-encode các ký tự đó. Có thể đặt `DATABASE_URL` trong môi trường PowerShell thay cho `.env`; biến môi trường sẽ được ưu tiên.

## 2. Cài và chạy backend

Từ thư mục dự án:

```powershell
cd be
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

> **Mẹo chạy nhanh trên Windows:** Bạn có thể nhấp đúp chuột vào file `start_backend.bat` ở thư mục gốc để tự động mở và chạy cả 3 service cùng lúc trên 3 cửa sổ riêng biệt. Khi muốn tắt, nhấp đúp file `stop_backend.bat`.

Hoặc mở **ba cửa sổ PowerShell riêng**, chuyển từng cửa sổ vào `be`, kích hoạt `.venv`, rồi đặt `SERVICE_NAME` và chạy service tương ứng. Cả ba tiến trình cùng đọc `DATABASE_URL` từ `.env`:

```powershell
$env:SERVICE_NAME = "sinhvien"
python -m uvicorn app.main:app --reload --port 8001
```

```powershell
$env:SERVICE_NAME = "detai"
python -m uvicorn app.main:app --reload --port 8002
```

```powershell
$env:SERVICE_NAME = "dangky"
python -m uvicorn app.main:app --reload --port 8003
```

Luôn chạy bằng `python -m uvicorn` trong virtualenv đang kích hoạt. Tránh gọi `uvicorn` trực tiếp nếu launcher còn trỏ tới đường dẫn Python cũ. Nếu Python báo chưa có module Uvicorn, cài dependencies bằng `python -m pip install -r requirements.txt` rồi chạy lại.

Giữ cả ba tiến trình chạy. Mặc định `DangKy Service` gọi dịch vụ sinh viên tại `http://127.0.0.1:8001/api/v1` và dịch vụ đề tài tại `http://127.0.0.1:8002/api/v1`. Nếu đổi cổng, đặt thêm `SINHVIEN_SERVICE_URL` và `DETAI_SERVICE_URL` trong cửa sổ chạy DangKy Service.

Swagger UI và health check:

| Service | Swagger UI | Health |
| --- | --- | --- |
| SinhVien | `http://localhost:8001/docs` | `http://localhost:8001/health` |
| DeTai | `http://localhost:8002/docs` | `http://localhost:8002/health` |
| DangKy | `http://localhost:8003/docs` | `http://localhost:8003/health` |

## 3. Cài và chạy frontend

Mở cửa sổ PowerShell khác:

```powershell
cd fe
npm install
npm start
```

Mở `http://localhost:4200`. Các API URL hiện được đặt trong Angular services:

- Sinh viên: `fe/src/app/services/student-api.ts` → `http://localhost:8001/api/v1/sinhviens`
- Đề tài: `fe/src/app/services/topic-api.ts` → `http://localhost:8002/api/v1/detais`
- Đăng ký: `fe/src/app/services/registration-api.ts` → `http://localhost:8003/api/v1/dang-ky`

Backend mặc định cho phép CORS từ `http://localhost:4200` và `http://127.0.0.1:4200`. Đổi danh sách này bằng biến `CORS_ORIGINS`, các origin phân tách bằng dấu phẩy.

## API và quy tắc nghiệp vụ

- `SinhVien Service`: `GET/POST /api/v1/sinhviens`, `GET/PUT/DELETE /api/v1/sinhviens/{ma_sinh_vien}`.
- `DeTai Service`: `GET/POST /api/v1/detais`, `GET/PUT/DELETE /api/v1/detais/{ma_de_tai}`.
- `DangKy Service`: `GET /api/v1/dang-ky` (lọc bằng `ma_sinh_vien` hoặc `ma_de_tai`), `POST /api/v1/dang-ky`, `DELETE /api/v1/dang-ky/{id}` để hủy.
- Chỉ đề tài `MO_DANG_KY` nhận đăng ký; không cho đăng ký trùng cùng cặp sinh viên/đề tài; giới hạn sức chứa đề tài được kiểm tra trước khi tạo.
- Hủy đăng ký đổi trạng thái thành `DA_HUY` và giữ lại bản ghi. Schema giữ khóa duy nhất theo cặp sinh viên/đề tài, vì vậy cặp đó không thể đăng ký lại sau khi hủy.
- Xóa sinh viên hoặc đề tài đã được đăng ký bị từ chối bởi ràng buộc khóa ngoại.
- CSDL dùng chung giữa ba tiến trình để phù hợp môi trường thực hành; các ranh giới dịch vụ và giao tiếp DangKy → SinhVien/DeTai được thể hiện qua REST API.

### Xử lý lỗi thường gặp

- Nếu API trả `500` và backend báo `cryptography package is required for sha256_password or caching_sha2_password`, cài lại dependency trong đúng virtualenv: `python -m pip install -r requirements.txt`, sau đó khởi động lại các backend.
- Nếu `python -m pip install -r requirements.txt` đã chạy trước khi thêm dependency, chạy lệnh đó lại để cài `cryptography`.
- Nếu MySQL báo sai user/password hoặc không tìm thấy database, đặt `DATABASE_URL` đúng thông tin MySQL trước khi khởi động mỗi service.
