# Hướng Dẫn Cài Đặt và Sử Dụng FastAPI

Tài liệu hướng dẫn chi tiết các bước thiết lập môi trường, cài đặt thư viện và phát triển ứng dụng web/API với **FastAPI**.

---

## 1. Yêu Cầu Hệ Thống

- **Python**: Phiên bản 3.8 trở lên (khuyên dùng Python 3.10+).
- Trình quản lý gói `pip`.

Kiểm tra phiên bản Python trên máy:
```bash
python --version
```

---

## 2. Thiết Lập Môi Trường Ảo (Virtual Environment)

Nên sử dụng môi trường ảo để cô lập các thư viện của dự án, tránh xung đột với hệ thống.

### Bước 2.1: Tạo môi trường ảo
Mở terminal tại thư mục dự án (`fastapi-demo`) và chạy:

```bash
python -m venv .venv
```

### Bước 2.2: Kích hoạt môi trường ảo

- **Windows (PowerShell)**:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  *(Nếu gặp lỗi script execution policy, chạy lệnh: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

- **Windows (Command Prompt / cmd.exe)**:
  ```cmd
  .venv\Scripts\activate.bat
  ```

- **Linux / macOS**:
  ```bash
  source .venv/bin/activate
  ```

> **Dấu hiệu nhận biết**: Sau khi kích hoạt thành công, dòng lệnh sẽ có tiền tố `(.venv)` ở đầu.

---

## 3. Cài Đặt FastAPI

Khuyên dùng gói cài đặt đầy đủ `fastapi[standard]` bao gồm FastAPI CLI, Uvicorn, Pydantic và các công cụ tiêu chuẩn khác:

```bash
pip install "fastapi[standard]"
```

*(Tùy chọn) Kiểm tra cài đặt:*
```bash
pip show fastapi
```

---

## 4. Cấu Trúc Dự Án Mẫu (Chuẩn Layered Architecture)

Cấu trúc dự án theo mô hình phân tầng (Clean / Layered Architecture) dành cho các ứng dụng thực tế và dự án lớn:

```text
backend/
│
├── app/
│   ├── __init__.py             # Đánh dấu app là một Python package chính
│   ├── main.py                 # Khởi tạo ứng dụng FastAPI và gom các routers
│   │
│   ├── core/                   # Cấu hình chung và bảo mật
│   │   ├── __init__.py
│   │   ├── config.py           # Quản lý Settings, biến môi trường (.env)
│   │   ├── security.py         # Xử lý JWT token, hash mật khẩu
│   │   └── exceptions.py       # Custom exception handlers
│   │
│   ├── database/               # Quản lý kết nối cơ sở dữ liệu
│   │   ├── __init__.py
│   │   ├── connection.py       # Khởi tạo Database Engine
│   │   └── session.py          # Quản lý DB Session (get_db dependency)
│   │
│   ├── models/                 # ORM Models (SQLAlchemy đại diện các bảng DB)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   │
│   ├── schemas/                # Pydantic Models (Validation Request / Response)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   │
│   ├── repositories/           # Tầng truy xuất dữ liệu (Data Access / CRUD)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   │
│   ├── services/               # Tầng nghiệp vụ (Business Logic)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   │
│   └── routers/                # Tầng điều hướng API (API Endpoints / Controllers)
│       ├── __init__.py
│       ├── auth.py
│       ├── users.py
│       └── products.py
│
├── tests/                      # Kiểm thử tự động (Unit test, Integration test)
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_users.py
│   └── test_products.py
│
├── .env                        # Chứa biến môi trường bảo mật
├── .gitignore                  # Bỏ qua các file không cần commit lên Git
├── requirements.txt            # Danh sách thư viện phụ thuộc
├── Dockerfile                  # Cấu hình đóng gói container cho ứng dụng
└── docker-compose.yml          # Điều phối các dịch vụ (App, PostgreSQL, Redis...)
```

### ⚠️ Lưu Ý Quan Trọng Về File `__init__.py`

- **Tại sao cần có `__init__.py`?**
  - Trong Python, sự hiện diện của file `__init__.py` biến một thư mục thông thường thành một **Python Package**.
  - Nếu thiếu `app/__init__.py`, Python và công cụ `fastapi dev` sẽ không thể xác định `app` làm package gốc, dẫn đến lỗi:
    `ModuleNotFoundError: No module named 'app'`
  - Tương tự, các thư mục con như `models/`, `routers/` cần có `__init__.py` để có thể thực hiện lệnh `from app.models.user import User`.

### 💡 Cách Tạo File `__init__.py`

#### 1. Tạo cho một package đơn lẻ (ví dụ tạo cho `app/models/`):

- **Windows (PowerShell)**:
  ```powershell
  New-Item -ItemType File -Path "app/models/__init__.py" -Force
  ```
  *(Hoặc lệnh rút gọn: `ni app/models/__init__.py -Force`)*

- **Windows (Command Prompt - cmd.exe)**:
  ```cmd
  type nul > app\models\__init__.py
  ```

- **Linux / macOS / Git Bash**:
  ```bash
  touch app/models/__init__.py
  ```

#### 2. Tạo tự động hàng loạt cho toàn bộ packages trong dự án:

Bạn có thể chạy 1 dòng lệnh duy nhất tại thư mục gốc của dự án:

- **Windows (PowerShell)**:
  ```powershell
  "app", "app/core", "app/database", "app/models", "app/schemas", "app/repositories", "app/services", "app/routers", "tests" | ForEach-Object { if (-not (Test-Path "$_\__init__.py")) { New-Item -ItemType File -Path "$_\__init__.py" -Force } }
  ```

- **Linux / macOS / Git Bash**:
  ```bash
  find app tests -type d -exec touch {}/__init__.py \;
  ```

---

### Luồng xử lý dữ liệu (Data Flow):
> **Client Request** ➔ **Routers** (nhận request & validate bằng *Schemas*) ➔ **Services** (xử lý logic nghiệp vụ) ➔ **Repositories** (truy vấn DB qua *Models*) ➔ **Database**

---

## 5. Viết Code Ứng Dụng Đầu Tiên

Tạo file `app/main.py` với nội dung:

```python
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="FastAPI Demo",
    description="Ứng dụng mẫu sử dụng FastAPI",
    version="1.0.0"
)

# Endpoint gốc
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Path parameter và Query parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "query": q}

# Model dữ liệu gửi lên (Request Body)
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

# POST endpoint
@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}
```

---

## 6. Chạy Ứng Dụng

### Cách 1: Sử dụng FastAPI CLI (Khuyên dùng với FastAPI mới)

- **Môi trường phát triển (Development - tự động reload khi sửa code)**:
  ```bash
  fastapi dev app/main.py
  ```

- **Môi trường triển khai (Production)**:
  ```bash
  fastapi run app/main.py
  ```

### Cách 2: Sử dụng Uvicorn trực tiếp
```bash
python -m uvicorn app.main:app --reload
```

---

## 7. Kiểm Tra API & Tài Liệu Tự Động (Interactive Docs)

Sau khi server khởi động (mặc định tại cổng `8000`):

1. **Gọi API trực tiếp**:
   - Truy cập trình duyệt: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - Kết quả trả về: `{"message": "Hello World"}`

2. **Swagger UI (Interactive API Docs)**:
   - Truy cập: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Cho phép xem danh sách endpoint, kiểu dữ liệu request/response và bấm **Try it out** để test trực tiếp.

3. **ReDoc (Giao diện tài liệu thay thế)**:
   - Truy cập: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 8. Quản Lý Dependencies (`requirements.txt`)

Để dễ dàng chia sẻ dự án cho máy khác hoặc deploy lên server:

- **Xuất danh sách thư viện hiện tại**:
  ```bash
  pip freeze > requirements.txt
  ```

- **Cài đặt lại dự án trên máy khác**:
  ```bash
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1   # (hoặc lệnh tương ứng theo OS)
  pip install -r requirements.txt
  ```
