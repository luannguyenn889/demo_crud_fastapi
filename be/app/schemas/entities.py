from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# =====================================================================
# Lớp cơ sở hỗ trợ đọc dữ liệu trực tiếp từ đối tượng ORM (SQLAlchemy)
# =====================================================================
class ORMModel(BaseModel):
    # from_attributes=True cho phép Pydantic đọc dữ liệu từ thuộc tính của ORM object thay vì dict
    model_config = ConfigDict(from_attributes=True)


# =====================================================================
# SCHEMAS DÀNH CHO SINH VIÊN
# =====================================================================
class SinhVienInput(BaseModel):
    """Schema dữ liệu đầu vào khi tạo mới hoặc cập nhật sinh viên"""
    ma_sinh_vien: str = Field(min_length=1, max_length=20, description="Mã số sinh viên (1-20 ký tự)")
    ho_ten: str = Field(min_length=1, max_length=100, description="Họ và tên sinh viên")
    email: str | None = Field(default=None, max_length=255, description="Địa chỉ email (tùy chọn)")
    lop: str | None = Field(default=None, max_length=50, description="Lớp sinh hoạt (tùy chọn)")
    nganh: str | None = Field(default=None, max_length=100, description="Chuyên ngành đào tạo (tùy chọn)")
    so_dien_thoai: str | None = Field(default=None, max_length=20, description="Số điện thoại liên hệ (tùy chọn)")


class SinhVienOut(ORMModel):
    """Schema định dạng dữ liệu sinh viên trả về cho client"""
    ma_sinh_vien: str
    ho_ten: str
    email: str | None
    lop: str | None
    nganh: str | None
    so_dien_thoai: str | None


# =====================================================================
# SCHEMAS DÀNH CHO ĐỀ TÀI
# =====================================================================
class DeTaiInput(BaseModel):
    """Schema dữ liệu đầu vào khi tạo mới hoặc cập nhật đề tài"""
    ma_de_tai: str = Field(min_length=1, max_length=20, description="Mã định danh đề tài (1-20 ký tự)")
    ten_de_tai: str = Field(min_length=1, max_length=200, description="Tên đề tài tốt nghiệp")
    mo_ta: str | None = Field(default=None, description="Mô tả chi tiết nội dung đề tài")
    giang_vien_huong_dan: str | None = Field(default=None, max_length=100, description="Họ tên giảng viên hướng dẫn")
    so_luong_toi_da: int = Field(default=1, ge=1, description="Số lượng sinh viên tối đa được phép làm đề tài (>= 1)")
    trang_thai: str = Field(default="MO_DANG_KY", description="Trạng thái đăng ký: MO_DANG_KY hoặc DA_DONG")


class DeTaiOut(ORMModel):
    """Schema định dạng dữ liệu đề tài trả về cho client"""
    ma_de_tai: str
    ten_de_tai: str
    mo_ta: str | None
    giang_vien_huong_dan: str | None
    so_luong_toi_da: int
    trang_thai: str


# =====================================================================
# SCHEMAS DÀNH CHO ĐĂNG KÝ ĐỀ TÀI
# =====================================================================
class DangKyInput(BaseModel):
    """Schema dữ liệu yêu cầu đăng ký đề tài gửi từ client"""
    ma_sinh_vien: str = Field(min_length=1, max_length=20, description="Mã sinh viên đăng ký")
    ma_de_tai: str = Field(min_length=1, max_length=20, description="Mã đề tài muốn đăng ký")


class DangKyOut(ORMModel):
    """Schema định dạng dữ liệu kết quả đăng ký trả về cho client"""
    ma_dang_ky: int
    ma_sinh_vien: str
    ma_de_tai: str
    ngay_dang_ky: datetime
    trang_thai: str

