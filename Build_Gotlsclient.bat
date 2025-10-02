@echo off
set SCRIPT_NAME=Gotlsclient.py

echo ==========================================
echo  Building %SCRIPT_NAME% with Nuitka (CLI)
echo ==========================================

REM Remove old EXE if it exists
if exist %~nSCRIPT_NAME%.exe del %~nSCRIPT_NAME%.exe

REM Nuitka build (no tkinter, no icon, pure CLI)
python -m nuitka ^
 --standalone ^
 --onefile ^
 --include-module=Gotlsclient ^
 --windows-console-mode=attach ^
 --jobs=12 ^
 --output-dir=. ^
 %SCRIPT_NAME%

echo ==========================================
echo  Build complete! EXE: %~nSCRIPT_NAME%.exe
echo ==========================================
pause
