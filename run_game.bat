@echo off
setlocal
cd /d "%~dp0"
python main.py
set EXIT_CODE=%ERRORLEVEL%
echo.
if not "%EXIT_CODE%"=="0" echo Program selesai dengan kode %EXIT_CODE%.
pause
exit /b %EXIT_CODE%
