@echo off
setlocal
cd /d "%~dp0"
python -m unittest discover -s tests -v
if errorlevel 1 goto :failed
python tools\validate_bank.py
if errorlevel 1 goto :failed

echo.
echo Semua pengujian dan validasi bank kata lulus.
pause
exit /b 0

:failed
echo.
echo Ada pengujian atau validasi yang gagal.
pause
exit /b 1
