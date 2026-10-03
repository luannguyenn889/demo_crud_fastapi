from datetime import datetime

from sqlalchemy import BigInteger, CheckConstraint, Computed, DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class SinhVien(Base):
    __tablename__ = "SINHVIEN"
    ma_sinh_vien: Mapped[str] = mapped_column(String(20), primary_key=True)
    ho_ten: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    lop: Mapped[str | None] = mapped_column(String(50))
    nganh: Mapped[str | None] = mapped_column(String(100))
    so_dien_thoai: Mapped[str | None] = mapped_column(String(20))


class DeTai(Base):
    __tablename__ = "DETAI"
    __table_args__ = (CheckConstraint("so_luong_toi_da > 0", name="chk_detai_so_luong"),)
    ma_de_tai: Mapped[str] = mapped_column(String(20), primary_key=True)
    ten_de_tai: Mapped[str] = mapped_column(String(200), nullable=False)
    mo_ta: Mapped[str | None] = mapped_column(Text)
    giang_vien_huong_dan: Mapped[str | None] = mapped_column(String(100))
    so_luong_toi_da: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    trang_thai: Mapped[str] = mapped_column(Enum("MO_DANG_KY", "DA_DONG"), nullable=False, default="MO_DANG_KY")


class DangKy(Base):
    __tablename__ = "DANGKY"
    __table_args__ = (
        UniqueConstraint("ma_sinh_vien", "ma_de_tai", name="uq_dangky_sinhvien_detai"),
        UniqueConstraint("ma_sinh_vien_dang_ky", name="uq_dangky_sinhvien_dang_ky"),
    )
    ma_dang_ky: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    ma_sinh_vien: Mapped[str] = mapped_column(String(20), ForeignKey("SINHVIEN.ma_sinh_vien", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    ma_de_tai: Mapped[str] = mapped_column(String(20), ForeignKey("DETAI.ma_de_tai", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    ngay_dang_ky: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    trang_thai: Mapped[str] = mapped_column(Enum("DA_DANG_KY", "DA_HUY"), nullable=False, default="DA_DANG_KY")
    ma_sinh_vien_dang_ky: Mapped[str | None] = mapped_column(
        String(20),
        Computed("CASE WHEN trang_thai = 'DA_DANG_KY' THEN ma_sinh_vien ELSE NULL END", persisted=True),
    )
