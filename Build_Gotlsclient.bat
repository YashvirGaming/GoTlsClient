@echo off
set SCRIPT_NAME=Gotlsclient.py
set ICON=icon.ico

echo ==========================================
echo  Building %SCRIPT_NAME% with Nuitka
echo ==========================================

REM Clean old EXE
if exist %~nSCRIPT_NAME%.exe del %~nSCRIPT_NAME%.exe

REM Nuitka build
python -m nuitka ^
 --standalone ^
 --onefile ^
 --include-module=Gotlsclient ^
 --enable-plugin=tk-inter ^
 --windows-console-mode=disable ^
 --jobs=12 ^
 --output-dir=. ^
 --windows-icon-from-ico=%ICON% ^
 %SCRIPT_NAME%

echo ==========================================
echo  Build complete! EXE: %~nSCRIPT_NAME%.exe
echo ==========================================
pause
