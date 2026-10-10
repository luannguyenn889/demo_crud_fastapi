from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import SERVICE_NAME
from app.database.connection import get_db
from app.models.entities import DangKy, DeTai, SinhVien
from app.schemas.entities import DangKyInput, DangKyOut, DeTaiInput, DeTaiOut, SinhVienInput, SinhVienOut
from app.services import catalog, registration

# Khởi tạo APIRouter với tiền tố chung là /api/v1
api = APIRouter(prefix="/api/v1")


# =====================================================================
# SINHVIEN SERVICE ENDPOINTS (Quản lý sinh viên)
# =====================================================================

@api.get("/sinhviens", response_model=list[SinhVienOut], tags=["SinhVien Service"])
def sinhviens(q: str | None = None, db: Session = Depends(get_db)):
    """Lấy danh sách tất cả sinh viên (có hỗ trợ tìm kiếm theo từ khóa 'q')"""
    return catalog.list_sinhvien(db, q)


@api.get("/sinhviens/{key}", response_model=SinhVienOut, tags=["SinhVien Service"])
def sinhvien(key: str, db: Session = Depends(get_db)):
    """Lấy thông tin chi tiết của một sinh viên theo mã số sinh viên"""
    item = db.get(SinhVien, key)
    if not item:
        raise HTTPException(404, "Không tìm thấy sinh viên")
    return item


@api.post("/sinhviens", response_model=SinhVienOut, status_code=201, tags=["SinhVien Service"])
def create_sinhvien(data: SinhVienInput, db: Session = Depends(get_db)):
    """Thêm mới một sinh viên vào hệ thống (Mã sinh viên không được trùng)"""
    return catalog.save_sinhvien(db, data.model_dump())


@api.put("/sinhviens/{key}", response_model=SinhVienOut, tags=["SinhVien Service"])
def update_sinhvien(key: str, data: SinhVienInput, db: Session = Depends(get_db)):
    """Cập nhật thông tin sinh viên theo mã số sinh viên"""
    if data.ma_sinh_vien != key:
        raise HTTPException(422, "Mã trong URL và dữ liệu phải trùng nhau")
    return catalog.save_sinhvien(db, data.model_dump(), key)


@api.delete("/sinhviens/{key}", status_code=204, tags=["SinhVien Service"])
def delete_sinhvien(key: str, db: Session = Depends(get_db)):
    """
    Xóa sinh viên khỏi hệ thống.
    Nếu sinh viên đã có bản ghi đăng ký đề tài (ràng buộc khóa ngoại RESTRICT), sẽ báo lỗi 409.
    """
    item = db.get(SinhVien, key)
    if not item:
        raise HTTPException(404, "Không tìm thấy sinh viên")
    try:
        db.delete(item)
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(409, "Sinh viên đang có đăng ký") from exc
    return Response(status_code=204)


# =====================================================================
# DETAI SERVICE ENDPOINTS (Quản lý đề tài tốt nghiệp)
# =====================================================================

@api.get("/detais", response_model=list[DeTaiOut], tags=["DeTai Service"])
def detais(q: str | None = None, db: Session = Depends(get_db)):
    """Lấy danh sách tất cả các đề tài tốt nghiệp (có hỗ trợ tìm kiếm theo từ khóa 'q')"""
    return catalog.list_detai(db, q)


@api.get("/detais/{key}", response_model=DeTaiOut, tags=["DeTai Service"])
def detai(key: str, db: Session = Depends(get_db)):
    """Lấy thông tin chi tiết một đề tài theo mã đề tài"""
    item = db.get(DeTai, key)
    if not item:
        raise HTTPException(404, "Không tìm thấy đề tài")
    return item


@api.post("/detais", response_model=DeTaiOut, status_code=201, tags=["DeTai Service"])
def create_detai(data: DeTaiInput, db: Session = Depends(get_db)):
    """Thêm mới một đề tài tốt nghiệp vào hệ thống"""
    return catalog.save_detai(db, data.model_dump())


@api.put("/detais/{key}", response_model=DeTaiOut, tags=["DeTai Service"])
def update_detai(key: str, data: DeTaiInput, db: Session = Depends(get_db)):
    """Cập nhật thông tin đề tài tốt nghiệp theo mã đề tài"""
    if data.ma_de_tai != key:
        raise HTTPException(422, "Mã trong URL và dữ liệu phải trùng nhau")
    return catalog.save_detai(db, data.model_dump(), key)


@api.delete("/detais/{key}", status_code=204, tags=["DeTai Service"])
def delete_detai(key: str, db: Session = Depends(get_db)):
    """
    Xóa đề tài tốt nghiệp khỏi hệ thống.
    Nếu đề tài đang có sinh viên đăng ký, sẽ báo lỗi 409 không thể xóa.
    """
    item = db.get(DeTai, key)
    if not item:
        raise HTTPException(404, "Không tìm thấy đề tài")
    try:
        db.delete(item)
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(409, "Đề tài đang có đăng ký") from exc
    return Response(status_code=204)


# =====================================================================
# DANGKY SERVICE ENDPOINTS (Quản lý đăng ký đề tài)
# =====================================================================

@api.get("/dang-ky", response_model=list[DangKyOut], tags=["DangKy Service"])
def dangky(
    ma_sinh_vien: str | None = None,
    ma_de_tai: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Lấy danh sách các lượt đăng ký đề tài.
    Có thể lọc theo 'ma_sinh_vien' hoặc 'ma_de_tai', sắp xếp giảm dần theo mã đăng ký (mới nhất lên đầu).
    """
    stmt = select(DangKy).order_by(DangKy.ma_dang_ky.desc())
    if ma_sinh_vien:
        stmt = stmt.where(DangKy.ma_sinh_vien == ma_sinh_vien)
    if ma_de_tai:
        stmt = stmt.where(DangKy.ma_de_tai == ma_de_tai)
    return list(db.scalars(stmt).all())


@api.post("/dang-ky", response_model=DangKyOut, status_code=201, tags=["DangKy Service"])
def create_dangky(data: DangKyInput, db: Session = Depends(get_db)):
    """
    Tạo mới một yêu cầu đăng ký đề tài cho sinh viên.
    Kiểm tra tồn tại, trạng thái đề tài, giới hạn số lượng và trạng thái của sinh viên.
    """
    return registration.create_registration(db, data.ma_sinh_vien, data.ma_de_tai)


@api.delete("/dang-ky/{key}", status_code=204, tags=["DangKy Service"])
def cancel_dangky(key: int, db: Session = Depends(get_db)):
    """
    Hủy đăng ký đề tài (Soft-delete: chuyển trạng thái sang 'DA_HUY').
    Sau khi hủy, sinh viên có thể đăng ký đề tài khác.
    """
    item = db.get(DangKy, key)
    if not item:
        raise HTTPException(404, "Không tìm thấy đăng ký")
    item.trang_thai = "DA_HUY"
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(409, "Không thể hủy đăng ký") from exc
    return Response(status_code=204)


# =====================================================================
# BỘ LỌC ENDPOINT THEO DỊCH VỤ (Kiến trúc SOA / Microservices)
# Khi chạy từng service độc lập trên từng port (8001, 8002, 8003):
# Chỉ giữ lại các endpoint thuộc về Service đó, ẩn các endpoint khác.
# =====================================================================
if SERVICE_NAME == "sinhvien":
    api.routes[:] = [r for r in api.routes if "SinhVien Service" in getattr(r, "tags", [])]
elif SERVICE_NAME == "detai":
    api.routes[:] = [r for r in api.routes if "DeTai Service" in getattr(r, "tags", [])]
elif SERVICE_NAME == "dangky":
    api.routes[:] = [r for r in api.routes if "DangKy Service" in getattr(r, "tags", [])]

