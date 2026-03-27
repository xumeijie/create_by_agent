@echo off
REM Test Automation Framework - Setup Script for Windows

echo.
echo ================================
echo Test Automation Framework Setup
echo ================================
echo.

REM Check Python installation
echo 🔍 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Found Python %PYTHON_VERSION%
echo.

REM Check Poetry installation
echo 🔍 Checking Poetry installation...
poetry --version >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing Poetry...
    python -m pip install poetry
    echo ✓ Poetry installed
) else (
    for /f %%i in ('poetry --version 2^>^&1') do set POETRY_VERSION=%%i
    echo ✓ Found !POETRY_VERSION!
)
echo.

REM Configure Poetry
echo ⚙️  Configuring Poetry...
poetry config virtualenvs.in-project true
echo ✓ Poetry configured to create .venv in project directory
echo.

REM Install dependencies
echo 📥 Installing dependencies...
poetry install
echo ✓ Dependencies installed
echo.

REM Show next steps
echo.
echo ================================
echo ✅ Setup complete!
echo ================================
echo.
echo Next steps:
echo.
echo 1. Activate virtual environment:
echo    poetry shell
echo.
echo 2. Run tests:
echo    poetry run pytest
echo.
echo 3. Or run commands directly:
echo    poetry run pytest tests/test_unit.py
echo.
echo For more details, see: POETRY_SETUP.md
echo.
pause
