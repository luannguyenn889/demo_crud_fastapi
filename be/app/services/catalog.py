from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.entities import DeTai, SinhVien


def list_sinhvien(db: Session, q: str | None):
    stmt = select(SinhVien).order_by(SinhVien.ma_sinh_vien)
    if q:
        stmt = stmt.where(SinhVien.ma_sinh_vien.contains(q) | SinhVien.ho_ten.contains(q))
    return db.scalars(stmt).all()


def save_sinhvien(db: Session, data: dict, key: str | None = None):
    obj = db.get(SinhVien, key or data["ma_sinh_vien"])
    if key and not obj:
        raise HTTPException(404, "Không tìm thấy sinh viên")
    if not key:
        if obj:
            raise HTTPException(409, "Mã sinh viên đã tồn tại")
        obj = SinhVien(**data)
        db.add(obj)
    else:
        for k, v in data.items():
            if k != "ma_sinh_vien": setattr(obj, k, v)
    return commit(db, obj)


def list_detai(db: Session, q: str | None):
    stmt = select(DeTai).order_by(DeTai.ma_de_tai)
    if q: stmt = stmt.where(DeTai.ma_de_tai.contains(q) | DeTai.ten_de_tai.contains(q))
    return db.scalars(stmt).all()


def save_detai(db: Session, data: dict, key: str | None = None):
    obj = db.get(DeTai, key or data["ma_de_tai"])
    if key and not obj: raise HTTPException(404, "Không tìm thấy đề tài")
    if not key:
        if obj: raise HTTPException(409, "Mã đề tài đã tồn tại")
        obj = DeTai(**data); db.add(obj)
    else:
        for k, v in data.items():
            if k != "ma_de_tai": setattr(obj, k, v)
    return commit(db, obj)


def commit(db: Session, obj):
    try:
        db.commit(); db.refresh(obj); return obj
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(409, "Dữ liệu trùng hoặc đang được sử dụng") from exc
