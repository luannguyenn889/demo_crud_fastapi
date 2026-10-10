from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.entities import DeTai, SinhVien


def list_sinhvien(db: Session, q: str | None = None) -> list[SinhVien]:
    """
    Lấy danh sách sinh viên trong cơ sở dữ liệu.
    - Sắp xếp tăng dần theo mã sinh viên.
    - Hỗ trợ tìm kiếm gần đúng (LIKE) theo mã sinh viên hoặc họ tên nếu có tham số 'q'.
    """
    stmt = select(SinhVien).order_by(SinhVien.ma_sinh_vien)
    if q:
        # Tìm kiếm theo mã hoặc tên sinh viên
        stmt = stmt.where(SinhVien.ma_sinh_vien.contains(q) | SinhVien.ho_ten.contains(q))
    return list(db.scalars(stmt).all())


def save_sinhvien(db: Session, data: dict, key: str | None = None) -> SinhVien:
    """
    Tạo mới hoặc cập nhật thông tin sinh viên.
    - Nếu 'key' là None: Nghiệp vụ TẠO MỚI (kiểm tra trùng mã sinh viên).
    - Nếu 'key' có giá trị: Nghiệp vụ CẬP NHẬT (kiểm tra tồn tại trước khi cập nhật).
    """
    # Tìm sinh viên theo mã (dùng 'key' nếu cập nhật, hoặc lấy từ payload nếu tạo mới)
    obj = db.get(SinhVien, key or data["ma_sinh_vien"])

    if key and not obj:
        # Trường hợp cập nhật nhưng không tìm thấy sinh viên trong CSDL
        raise HTTPException(404, "Không tìm thấy sinh viên")

    if not key:
        # Trường hợp tạo mới: nếu mã sinh viên đã tồn tại thì báo lỗi trùng lặp (409)
        if obj:
            raise HTTPException(409, "Mã sinh viên đã tồn tại")
        obj = SinhVien(**data)
        db.add(obj)
    else:
        # Trường hợp cập nhật: gán các giá trị mới (không đổi khóa chính ma_sinh_vien)
        for field, value in data.items():
            if field != "ma_sinh_vien":
                setattr(obj, field, value)

    return commit(db, obj)


def list_detai(db: Session, q: str | None = None) -> list[DeTai]:
    """
    Lấy danh sách đề tài tốt nghiệp trong cơ sở dữ liệu.
    - Sắp xếp tăng dần theo mã đề tài.
    - Hỗ trợ tìm kiếm theo mã đề tài hoặc tên đề tài nếu có tham số 'q'.
    """
    stmt = select(DeTai).order_by(DeTai.ma_de_tai)
    if q:
        # Tìm kiếm theo mã đề tài hoặc tên đề tài
        stmt = stmt.where(DeTai.ma_de_tai.contains(q) | DeTai.ten_de_tai.contains(q))
    return list(db.scalars(stmt).all())


def save_detai(db: Session, data: dict, key: str | None = None) -> DeTai:
    """
    Tạo mới hoặc cập nhật thông tin đề tài tốt nghiệp.
    - Nếu 'key' là None: Nghiệp vụ TẠO MỚI (kiểm tra trùng mã đề tài).
    - Nếu 'key' có giá trị: Nghiệp vụ CẬP NHẬT (kiểm tra tồn tại trước khi cập nhật).
    """
    # Tìm đề tài theo mã trong CSDL
    obj = db.get(DeTai, key or data["ma_de_tai"])

    if key and not obj:
        # Không tìm thấy đề tài cần cập nhật
        raise HTTPException(404, "Không tìm thấy đề tài")

    if not key:
        # Kiểm tra trùng mã đề tài khi tạo mới
        if obj:
            raise HTTPException(409, "Mã đề tài đã tồn tại")
        obj = DeTai(**data)
        db.add(obj)
    else:
        # Cập nhật các trường thông tin (giữ nguyên mã đề tài)
        for field, value in data.items():
            if field != "ma_de_tai":
                setattr(obj, field, value)

    return commit(db, obj)


def commit(db: Session, obj):
    """
    Hàm phụ trợ thực hiện commit transaction xuống CSDL và làm mới dữ liệu đối tượng.
    Nếu vi phạm ràng buộc toàn vẹn (IntegrityError), thực hiện rollback và ném lỗi 409 Conflict.
    """
    try:
        db.commit()
        db.refresh(obj)
        return obj
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(409, "Dữ liệu trùng hoặc đang được sử dụng") from exc

