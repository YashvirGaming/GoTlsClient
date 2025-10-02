@echo off
set SCRIPT_NAME=Gotlsclient.py
set PYTHON_VERSION=3.10.9
set PYTHON_URL=https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe
set PYTHON_INSTALLER=python-3.10.9-amd64.exe

echo ==========================================
echo   🚀 TLS Proxy Builder (Python %PYTHON_VERSION% + Nuitka)
echo ==========================================

:: Check if Python exists
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Downloading Python %PYTHON_VERSION%...
    powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"
    echo 📦 Installing Python %PYTHON_VERSION%...
    start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    del %PYTHON_INSTALLER%
)

:: Verify Python version
for /f "tokens=2 delims= " %%v in ('python --version') do set INSTALLED_VERSION=%%v
echo 🔎 Found Python version: %INSTALLED_VERSION%

echo %INSTALLED_VERSION% | findstr /c:"%PYTHON_VERSION%" >nul
if errorlevel 1 (
    echo ⚠️ Python is not %PYTHON_VERSION%. Please install Python %PYTHON_VERSION% manually from:
    echo     https://www.python.org/downloads/release/python-3109/
    pause
    exit /b
)

:: Ensure pip is available
python -m ensurepip --upgrade >nul 2>&1

:: Install/upgrade pip + Nuitka
echo 📦 Installing/updating Nuitka...
python -m pip install --upgrade pip >nul
python -m pip install --upgrade nuitka >nul

:: Show versions
python --version
python -m nuitka --version

:: Remove old EXE if exists
if exist %~nSCRIPT_NAME%.exe del %~nSCRIPT_NAME%.exe

:: Build EXE
echo ==========================================
echo  Building %SCRIPT_NAME% with Nuitka (CLI)
echo ==========================================

python -m nuitka ^
 --standalone ^
 --onefile ^
 --include-module=Gotlsclient ^
 --windows-console-mode=attach ^
 --jobs=12 ^
 --output-dir=. ^
 %SCRIPT_NAME%

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Build failed with error code %ERRORLEVEL%
) else (
    echo.
    echo ✅ Build complete! EXE: %~nSCRIPT_NAME%.exe
)

echo.
pause
