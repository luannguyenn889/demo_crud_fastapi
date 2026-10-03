from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SinhVienInput(BaseModel):
    ma_sinh_vien: str = Field(min_length=1, max_length=20)
    ho_ten: str = Field(min_length=1, max_length=100)
    email: str | None = Field(default=None, max_length=255)
    lop: str | None = Field(default=None, max_length=50)
    nganh: str | None = Field(default=None, max_length=100)
    so_dien_thoai: str | None = Field(default=None, max_length=20)


class SinhVienOut(ORMModel):
    ma_sinh_vien: str
    ho_ten: str
    email: str | None
    lop: str | None
    nganh: str | None
    so_dien_thoai: str | None


class DeTaiInput(BaseModel):
    ma_de_tai: str = Field(min_length=1, max_length=20)
    ten_de_tai: str = Field(min_length=1, max_length=200)
    mo_ta: str | None = None
    giang_vien_huong_dan: str | None = Field(default=None, max_length=100)
    so_luong_toi_da: int = Field(default=1, ge=1)
    trang_thai: str = "MO_DANG_KY"


class DeTaiOut(ORMModel):
    ma_de_tai: str
    ten_de_tai: str
    mo_ta: str | None
    giang_vien_huong_dan: str | None
    so_luong_toi_da: int
    trang_thai: str


class DangKyInput(BaseModel):
    ma_sinh_vien: str = Field(min_length=1, max_length=20)
    ma_de_tai: str = Field(min_length=1, max_length=20)


class DangKyOut(ORMModel):
    ma_dang_ky: int
    ma_sinh_vien: str
    ma_de_tai: str
    ngay_dang_ky: datetime
    trang_thai: str
