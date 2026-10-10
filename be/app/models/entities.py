from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Computed,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


# =====================================================================
# Bảng SINHVIEN: Quản lý hồ sơ thông tin sinh viên
# =====================================================================
class SinhVien(Base):
    __tablename__ = "SINHVIEN"

    # Mã sinh viên là khóa chính (ví dụ: SV001, SV002)
    ma_sinh_vien: Mapped[str] = mapped_column(String(20), primary_key=True)
    # Họ tên sinh viên (bắt buộc nhập)
    ho_ten: Mapped[str] = mapped_column(String(100), nullable=False)
    # Email của sinh viên (không được trùng lặp giữa các sinh viên)
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    # Lớp sinh hoạt (ví dụ: CNTT-K20)
    lop: Mapped[str | None] = mapped_column(String(50))
    # Ngành học (ví dụ: Công nghệ thông tin)
    nganh: Mapped[str | None] = mapped_column(String(100))
    # Số điện thoại liên hệ
    so_dien_thoai: Mapped[str | None] = mapped_column(String(20))


# =====================================================================
# Bảng DETAI: Quản lý danh mục các đề tài tốt nghiệp
# =====================================================================
class DeTai(Base):
    __tablename__ = "DETAI"
    # Ràng buộc số lượng sinh viên tối đa của đề tài phải lớn hơn 0
    __table_args__ = (CheckConstraint("so_luong_toi_da > 0", name="chk_detai_so_luong"),)

    # Mã đề tài là khóa chính (ví dụ: DT001, DT002)
    ma_de_tai: Mapped[str] = mapped_column(String(20), primary_key=True)
    # Tên đề tài (bắt buộc nhập)
    ten_de_tai: Mapped[str] = mapped_column(String(200), nullable=False)
    # Mô tả chi tiết yêu cầu, phạm vi của đề tài
    mo_ta: Mapped[str | None] = mapped_column(Text)
    # Giảng viên hướng dẫn thực hiện đề tài
    giang_vien_huong_dan: Mapped[str | None] = mapped_column(String(100))
    # Số lượng sinh viên tối đa được phép đăng ký vào đề tài này (mặc định là 1)
    so_luong_toi_da: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    # Trạng thái mở hoặc đóng nhận đăng ký: 'MO_DANG_KY' hoặc 'DA_DONG'
    trang_thai: Mapped[str] = mapped_column(
        Enum("MO_DANG_KY", "DA_DONG"), nullable=False, default="MO_DANG_KY"
    )


# =====================================================================
# Bảng DANGKY: Quản lý lịch sử và trạng thái đăng ký đề tài của sinh viên
# =====================================================================
class DangKy(Base):
    __tablename__ = "DANGKY"
    __table_args__ = (
        # 1. Ràng buộc: Mỗi sinh viên không thể đăng ký trùng cùng một đề tài nhiều lần
        UniqueConstraint("ma_sinh_vien", "ma_de_tai", name="uq_dangky_sinhvien_detai"),
        # 2. Ràng buộc: Mỗi sinh viên tại một thời điểm chỉ có tối đa 1 đề tài ở trạng thái hiệu lực (DA_DANG_KY)
        UniqueConstraint("ma_sinh_vien_dang_ky", name="uq_dangky_sinhvien_dang_ky"),
    )

    # Khóa chính tự động tăng
    ma_dang_ky: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # Mã sinh viên tham chiếu khóa ngoại tới bảng SINHVIEN (chặn xóa/sửa nếu đang có đăng ký)
    ma_sinh_vien: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("SINHVIEN.ma_sinh_vien", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
    )

    # Mã đề tài tham chiếu khóa ngoại tới bảng DETAI (cascade khi cập nhật mã đề tài)
    ma_de_tai: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("DETAI.ma_de_tai", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    # Thời điểm đăng ký (mặc định lấy thời gian hiện tại của database)
    ngay_dang_ky: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )

    # Trạng thái đăng ký: 'DA_DANG_KY' (đang hiệu lực) hoặc 'DA_HUY' (đã hủy)
    trang_thai: Mapped[str] = mapped_column(
        Enum("DA_DANG_KY", "DA_HUY"), nullable=False, default="DA_DANG_KY"
    )

    # Cột tính toán tự động (Generated Column):
    # - Nếu trạng thái là 'DA_DANG_KY' => nhận giá trị ma_sinh_vien
    # - Nếu trạng thái là 'DA_HUY'     => nhận giá trị NULL
    # Kết hợp với UniqueConstraint ở trên để đảm bảo sinh viên chỉ có 1 đề tài hoạt động cùng lúc
    ma_sinh_vien_dang_ky: Mapped[str | None] = mapped_column(
        String(20),
        Computed(
            "CASE WHEN trang_thai = 'DA_DANG_KY' THEN ma_sinh_vien ELSE NULL END",
            persisted=True,
        ),
    )

