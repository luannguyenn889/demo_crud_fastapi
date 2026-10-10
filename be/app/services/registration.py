import httpx
from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import DETAI_SERVICE_URL, SINHVIEN_SERVICE_URL
from app.models.entities import DangKy


def verify(url: str, resource: str, key: str) -> dict:
    """
    Gọi HTTP GET sang service khác để xác thực thông tin tài nguyên (Kiến trúc SOA / Microservices).
    - url: URL gốc của service cần gọi (ví dụ: http://127.0.0.1:8001/api/v1)
    - resource: Tên tài nguyên (ví dụ: 'sinhviens' hoặc 'detais')
    - key: Mã định danh của tài nguyên (ví dụ: 'SV001', 'DT001')
    """
    try:
        # Gửi HTTP request nội bộ với thời gian timeout là 3 giây
        response = httpx.get(f"{url}/{resource}/{key}", timeout=3.0)
    except httpx.RequestError as exc:
        # Lỗi mạng hoặc service đích chưa được khởi động
        raise HTTPException(503, f"Dịch vụ {resource} hiện không khả dụng") from exc

    if response.status_code == 404:
        # Không tìm thấy đối tượng tương ứng ở service đích
        raise HTTPException(404, f"Không tìm thấy {resource}")

    if response.is_error:
        # Service đích trả về mã lỗi 4xx hoặc 5xx
        raise HTTPException(502, f"Dịch vụ {resource} phản hồi lỗi")

    return response.json()


def create_registration(db: Session, student_key: str, topic_key: str) -> DangKy:
    """
    Nghiệp vụ đăng ký đề tài tốt nghiệp cho sinh viên.
    Thực hiện theo quy trình kiểm tra nghiệp vụ tuần tự:
      1. Xác thực sinh viên có tồn tại qua SinhVien Service.
      2. Xác thực đề tài có tồn tại qua DeTai Service.
      3. Đảm bảo đề tài đang ở trạng thái 'MO_DANG_KY'.
      4. Đảm bảo sinh viên hiện chưa giữ một đề tài nào khác đang có hiệu lực.
      5. Đảm bảo sinh viên chưa từng đăng ký đề tài này.
      6. Đảm bảo đề tài chưa vượt quá số lượng sinh viên tối đa cho phép.
    """
    # Bước 1: Kiểm tra sinh viên có tồn tại hay không (gọi sang SinhVien Service)
    verify(SINHVIEN_SERVICE_URL, "sinhviens", student_key)

    # Bước 2: Kiểm tra đề tài có tồn tại hay không (gọi sang DeTai Service)
    topic = verify(DETAI_SERVICE_URL, "detais", topic_key)

    # Bước 3: Kiểm tra trạng thái đề tài có đang mở đăng ký hay không
    if topic["trang_thai"] != "MO_DANG_KY":
        raise HTTPException(409, "Đề tài đã đóng đăng ký")

    # Bước 4: Kiểm tra sinh viên đã có đề tài nào đang có hiệu lực (DA_DANG_KY) chưa
    active_registration = db.scalar(
        select(DangKy).where(
            DangKy.ma_sinh_vien == student_key,
            DangKy.trang_thai == "DA_DANG_KY",
        )
    )
    if active_registration:
        raise HTTPException(409, "Sinh viên cần hủy đăng ký hiện tại trước khi đăng ký đề tài khác")

    # Bước 5: Kiểm tra xem sinh viên đã có bản ghi đăng ký nào với đề tài này chưa
    existing = db.scalar(
        select(DangKy).where(
            DangKy.ma_sinh_vien == student_key,
            DangKy.ma_de_tai == topic_key,
        )
    )
    if existing:
        raise HTTPException(409, "Sinh viên đã có đăng ký với đề tài này")

    # Bước 6: Đếm số lượng sinh viên đã đăng ký thành công đề tài này
    count = db.scalar(
        select(func.count())
        .select_from(DangKy)
        .where(DangKy.ma_de_tai == topic_key, DangKy.trang_thai == "DA_DANG_KY")
    )
    if count >= topic["so_luong_toi_da"]:
        raise HTTPException(409, "Đề tài đã đủ số lượng sinh viên")

    # Khởi tạo bản ghi đăng ký mới và lưu vào cơ sở dữ liệu
    record = DangKy(ma_sinh_vien=student_key, ma_de_tai=topic_key)
    db.add(record)
    try:
        db.commit()
        db.refresh(record)
        return record
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(409, "Đăng ký bị trùng hoặc dữ liệu tham chiếu không hợp lệ") from exc

