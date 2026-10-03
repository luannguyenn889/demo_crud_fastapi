import httpx
from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import DETAI_SERVICE_URL, SINHVIEN_SERVICE_URL
from app.models.entities import DangKy


def verify(url: str, resource: str, key: str):
    try:
        response = httpx.get(f"{url}/{resource}/{key}", timeout=3.0)
    except httpx.RequestError as exc:
        raise HTTPException(503, f"Dịch vụ {resource} hiện không khả dụng") from exc
    if response.status_code == 404:
        raise HTTPException(404, f"Không tìm thấy {resource}")
    if response.is_error:
        raise HTTPException(502, f"Dịch vụ {resource} phản hồi lỗi")
    return response.json()


def create_registration(db: Session, student_key: str, topic_key: str):
    verify(SINHVIEN_SERVICE_URL, "sinhviens", student_key)
    topic = verify(DETAI_SERVICE_URL, "detais", topic_key)
    if topic["trang_thai"] != "MO_DANG_KY":
        raise HTTPException(409, "Đề tài đã đóng đăng ký")
    existing = db.scalar(select(DangKy).where(DangKy.ma_sinh_vien == student_key, DangKy.ma_de_tai == topic_key))
    if existing: raise HTTPException(409, "Sinh viên đã có đăng ký với đề tài này")
    count = db.scalar(select(func.count()).select_from(DangKy).where(DangKy.ma_de_tai == topic_key, DangKy.trang_thai == "DA_DANG_KY"))
    if count >= topic["so_luong_toi_da"]: raise HTTPException(409, "Đề tài đã đủ số lượng sinh viên")
    record = DangKy(ma_sinh_vien=student_key, ma_de_tai=topic_key)
    db.add(record)
    try:
        db.commit(); db.refresh(record); return record
    except IntegrityError as exc:
        db.rollback(); raise HTTPException(409, "Đăng ký bị trùng hoặc dữ liệu tham chiếu không hợp lệ") from exc
