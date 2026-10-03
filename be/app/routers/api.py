from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import SERVICE_NAME
from app.database.connection import get_db
from app.models.entities import DangKy, DeTai, SinhVien
from app.schemas.entities import DangKyInput, DangKyOut, DeTaiInput, DeTaiOut, SinhVienInput, SinhVienOut
from app.services import catalog, registration

api = APIRouter(prefix="/api/v1")


@api.get("/sinhviens", response_model=list[SinhVienOut], tags=["SinhVien Service"])
def sinhviens(q: str | None = None, db: Session = Depends(get_db)): return catalog.list_sinhvien(db, q)

@api.get("/sinhviens/{key}", response_model=SinhVienOut, tags=["SinhVien Service"])
def sinhvien(key: str, db: Session = Depends(get_db)):
    item = db.get(SinhVien, key)
    if not item: raise HTTPException(404, "Không tìm thấy sinh viên")
    return item

@api.post("/sinhviens", response_model=SinhVienOut, status_code=201, tags=["SinhVien Service"])
def create_sinhvien(data: SinhVienInput, db: Session = Depends(get_db)): return catalog.save_sinhvien(db, data.model_dump())

@api.put("/sinhviens/{key}", response_model=SinhVienOut, tags=["SinhVien Service"])
def update_sinhvien(key: str, data: SinhVienInput, db: Session = Depends(get_db)):
    if data.ma_sinh_vien != key: raise HTTPException(422, "Mã trong URL và dữ liệu phải trùng nhau")
    return catalog.save_sinhvien(db, data.model_dump(), key)

@api.delete("/sinhviens/{key}", status_code=204, tags=["SinhVien Service"])
def delete_sinhvien(key: str, db: Session = Depends(get_db)):
    item = db.get(SinhVien, key)
    if not item: raise HTTPException(404, "Không tìm thấy sinh viên")
    try: db.delete(item); db.commit()
    except Exception as exc: db.rollback(); raise HTTPException(409, "Sinh viên đang có đăng ký") from exc
    return Response(status_code=204)

@api.get("/detais", response_model=list[DeTaiOut], tags=["DeTai Service"])
def detais(q: str | None = None, db: Session = Depends(get_db)): return catalog.list_detai(db, q)

@api.get("/detais/{key}", response_model=DeTaiOut, tags=["DeTai Service"])
def detai(key: str, db: Session = Depends(get_db)):
    item = db.get(DeTai, key)
    if not item: raise HTTPException(404, "Không tìm thấy đề tài")
    return item

@api.post("/detais", response_model=DeTaiOut, status_code=201, tags=["DeTai Service"])
def create_detai(data: DeTaiInput, db: Session = Depends(get_db)): return catalog.save_detai(db, data.model_dump())

@api.put("/detais/{key}", response_model=DeTaiOut, tags=["DeTai Service"])
def update_detai(key: str, data: DeTaiInput, db: Session = Depends(get_db)):
    if data.ma_de_tai != key: raise HTTPException(422, "Mã trong URL và dữ liệu phải trùng nhau")
    return catalog.save_detai(db, data.model_dump(), key)

@api.delete("/detais/{key}", status_code=204, tags=["DeTai Service"])
def delete_detai(key: str, db: Session = Depends(get_db)):
    item = db.get(DeTai, key)
    if not item: raise HTTPException(404, "Không tìm thấy đề tài")
    try: db.delete(item); db.commit()
    except Exception as exc: db.rollback(); raise HTTPException(409, "Đề tài đang có đăng ký") from exc
    return Response(status_code=204)

@api.get("/dang-ky", response_model=list[DangKyOut], tags=["DangKy Service"])
def dangky(ma_sinh_vien: str | None = None, ma_de_tai: str | None = None, db: Session = Depends(get_db)):
    stmt = select(DangKy).order_by(DangKy.ma_dang_ky.desc())
    if ma_sinh_vien: stmt = stmt.where(DangKy.ma_sinh_vien == ma_sinh_vien)
    if ma_de_tai: stmt = stmt.where(DangKy.ma_de_tai == ma_de_tai)
    return db.scalars(stmt).all()

@api.post("/dang-ky", response_model=DangKyOut, status_code=201, tags=["DangKy Service"])
def create_dangky(data: DangKyInput, db: Session = Depends(get_db)):
    return registration.create_registration(db, data.ma_sinh_vien, data.ma_de_tai)

@api.delete("/dang-ky/{key}", status_code=204, tags=["DangKy Service"])
def cancel_dangky(key: int, db: Session = Depends(get_db)):
    item = db.get(DangKy, key)
    if not item: raise HTTPException(404, "Không tìm thấy đăng ký")
    item.trang_thai = "DA_HUY"
    try: db.commit()
    except IntegrityError as exc: db.rollback(); raise HTTPException(409, "Không thể hủy đăng ký") from exc
    return Response(status_code=204)


if SERVICE_NAME == "sinhvien":
    api.routes[:] = [r for r in api.routes if "SinhVien Service" in getattr(r, "tags", [])]
elif SERVICE_NAME == "detai":
    api.routes[:] = [r for r in api.routes if "DeTai Service" in getattr(r, "tags", [])]
elif SERVICE_NAME == "dangky":
    api.routes[:] = [r for r in api.routes if "DangKy Service" in getattr(r, "tags", [])]
