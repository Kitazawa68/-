@echo off
echo Starting Campus Trade Student Side...
echo Please leave this and the new windows open.

set "BASE_DIR=%~dp0"

set GOPROXY=https://goproxy.cn,direct
call npm config set registry https://registry.npmmirror.com

echo ====================================
echo Starting Go Backend in new window...
start "Student Go Backend" /D "%BASE_DIR%campus-trade-go" cmd /K "echo Init Go Backend... && go mod tidy && go run ."

echo ====================================
echo Starting Vue Frontend in new window (Wait for install)...
start "Student Vue Frontend" /D "%BASE_DIR%campus-trade-web" cmd /K "echo Installing frontend deps... && npm install && echo Starting website... && npm run dev"

echo ====================================
echo Start commands sent!
echo If Windows Defender Firewall prompts, please allow.
echo Frontend will be at http://localhost:5173/ or similar.
pause
