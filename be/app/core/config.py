import os
from pathlib import Path

from dotenv import load_dotenv

# Đọc cấu hình từ file .env nằm ở thư mục gốc của backend (be/.env)
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# Chuỗi kết nối tới cơ sở dữ liệu MySQL (sử dụng PyMySQL làm driver kết nối, bảng mã utf8mb4)
DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+pymysql://root:password@127.0.0.1:3306/demo_quan_ly_do_an?charset=utf8mb4"
)

# URL gọi nội bộ giữa các service (phục vụ mô hình kiến trúc SOA / Microservices)
# - DangKy Service gọi sang SinhVien Service để xác thực sinh viên có tồn tại hay không
SINHVIEN_SERVICE_URL = os.getenv("SINHVIEN_SERVICE_URL", "http://127.0.0.1:8001/api/v1")

# - DangKy Service gọi sang DeTai Service để kiểm tra trạng thái mở/đóng và số lượng đề tài
DETAI_SERVICE_URL = os.getenv("DETAI_SERVICE_URL", "http://127.0.0.1:8002/api/v1")

# Tên dịch vụ hiện tại: 'all' (chạy chung), 'sinhvien', 'detai', hoặc 'dangky'
# Giúp ứng dụng xác định cần bật những API route nào khi khởi chạy riêng lẻ
SERVICE_NAME = os.getenv("SERVICE_NAME", "all")

# Danh sách các domain frontend được phép truy cập API (CORS)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:4200,http://127.0.0.1:4200").split(",")

