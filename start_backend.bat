@echo off
chcp 65001 > nul
echo ========================================================
echo   KHOI DONG HE THONG BACKEND (3 SOA SERVICES FASTAPI)
echo ========================================================
echo.

cd /d "%~dp0be"

if not exist ".venv\Scripts\activate.bat" (
    echo [LOI] Khong tim thay moi truong ao .venv trong thu muc be!
    echo Vui long tao virtualenv truoc:
    echo   cd be
    echo   python -m venv .venv
    echo   call .venv\Scripts\activate.bat
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [1/3] Dang khoi dong SinhVien Service (Port 8001)...
start "SinhVien Service (:8001)" cmd /k "cd /d ""%~dp0be"" && call .venv\Scripts\activate.bat && set SERVICE_NAME=sinhvien && title SinhVien Service (:8001) && python -m uvicorn app.main:app --reload --port 8001"

timeout /t 1 /nobreak > nul

echo [2/3] Dang khoi dong DeTai Service (Port 8002)...
start "DeTai Service (:8002)" cmd /k "cd /d ""%~dp0be"" && call .venv\Scripts\activate.bat && set SERVICE_NAME=detai && title DeTai Service (:8002) && python -m uvicorn app.main:app --reload --port 8002"

timeout /t 1 /nobreak > nul

echo [3/3] Dang khoi dong DangKy Service (Port 8003)...
start "DangKy Service (:8003)" cmd /k "cd /d ""%~dp0be"" && call .venv\Scripts\activate.bat && set SERVICE_NAME=dangky && title DangKy Service (:8003) && python -m uvicorn app.main:app --reload --port 8003"

echo.
echo ========================================================
echo   DA KHOI DONG XONG CA 3 DICH VU TREN CAC CUA SO RIENG:
echo   - SinhVien Service : http://localhost:8001/docs
echo   - DeTai Service    : http://localhost:8002/docs
echo   - DangKy Service   : http://localhost:8003/docs
echo ========================================================
echo Cua so nay se tu dong dong sau 5 giay...
timeout /t 5 > nul
