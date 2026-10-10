from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import DATABASE_URL


# Lớp Base cơ sở cho các bảng ORM kế thừa (SQLAlchemy 2.0 Declarative Style)
class Base(DeclarativeBase):
    pass


# Khởi tạo engine kết nối tới CSDL MySQL
# pool_pre_ping=True: Tự động kiểm tra kết nối còn sống trước khi truy vấn (tránh lỗi kết nối bị rớt)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Tạo Session factory để khởi tạo các phiên làm việc (session) với CSDL
# autoflush=False: Không tự động đẩy thay đổi xuống DB trước khi truy vấn
# expire_on_commit=False: Giữ nguyên dữ liệu của đối tượng sau khi commit (không cần query lại)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


# Dependency injection trong FastAPI để cấp phát session CSDL cho mỗi request
def get_db():
    """
    Cung cấp một database session cho mỗi HTTP request.
    Sau khi request hoàn tất (thành công hoặc lỗi), đảm bảo session được đóng để tránh rò rỉ kết nối.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

