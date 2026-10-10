from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import CORS_ORIGINS, SERVICE_NAME
from app.database.connection import engine
from app.routers.api import api

# =====================================================================
# KHỞI TẠO ỨNG DỤNG FASTAPI
# =====================================================================
app = FastAPI(
    title="Quản lý đồ án tốt nghiệp",
    version="1.0.0",
    description="Hệ thống REST API quản lý sinh viên, đề tài và đăng ký đồ án theo mô hình SOA / Microservices",
)

# Cấu hình CORS Middleware: cho phép ứng dụng Frontend (Angular) gọi API từ các domain khác nhau
app.add_middleware(
    CORSMiddleware,
    allow_origins=[item.strip() for item in CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gắn các route API (prefix /api/v1) vào ứng dụng FastAPI
app.include_router(api)


# =====================================================================
# ENDPOINT KIỂM TRA SỨC KHỎE HỆ THỐNG (HEALTH CHECK)
# =====================================================================
@app.get("/health", tags=["Health"])
def health():
    """
    Kiểm tra tình trạng hoạt động của service và khả năng kết nối tới CSDL MySQL.
    - Trả về status 'ok' nếu kết nối CSDL thành công.
    - Trả về status 'degraded' nếu không thể kết nối tới CSDL.
    """
    try:
        # Thử thực hiện câu lệnh kiểm tra kết nối đơn giản SELECT 1
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "ok",
            "service": SERVICE_NAME,
        }
    except Exception:
        return {
            "status": "degraded",
            "database": "unavailable",
            "service": SERVICE_NAME,
        }

