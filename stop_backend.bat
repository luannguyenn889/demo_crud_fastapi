@echo off
chcp 65001 > nul
echo ========================================================
echo   DANG DUNG CA 3 BACKEND SERVICES (PORTS 8001, 8002, 8003)
echo ========================================================
echo.

for %%P in (8001 8002 8003) do (
    echo Dang tat service dang lang nghe tai port %%P...
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%%P ^| findstr LISTENING 2^>nul') do (
        taskkill /f /pid %%a > nul 2>&1
    )
)

echo.
echo Da dung tat ca cac backend service thanh cong!
echo Cua so nay se tu dong dong sau 3 giay...
timeout /t 3 > nul
