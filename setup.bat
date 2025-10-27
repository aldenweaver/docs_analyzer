@echo off
REM Setup script for Documentation Quality Analyzer (Windows)
REM Creates virtual environment and installs dependencies

echo Setting up Documentation Quality Analyzer...

REM Check Python version
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo Next steps:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate.bat
echo.
echo   2. Copy .env.example to .env and configure:
echo      copy .env.example .env
echo      REM Edit .env and add your ANTHROPIC_API_KEY (optional)
echo.
echo   3. Run the analyzer:
echo      python doc_analyzer.py \path\to\docs
echo.
echo   4. Or run tests:
echo      pytest test_analyzer.py -v
echo.
echo To deactivate the virtual environment later, run: deactivate
