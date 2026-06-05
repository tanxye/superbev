@echo off
title SUPERBEV - Setup
echo ============================================
echo   SUPERBEV- Starting up...
echo ============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed on this computer.
    echo.
    echo Please install Python 3 from:
    echo    https://www.python.org/downloads/
    echo.
    echo IMPORTANT: On the installer, tick the box that says
    echo "Add Python to PATH" before clicking Install.
    echo.
    echo After installing Python, double-click run_game.bat again.
    pause
    start https://www.python.org/downloads/
    exit /b
)

echo Python found. Installing required libraries...
echo (This only happens once - future launches will be instant)
echo.

python -m pip install --upgrade pip --quiet
python -m pip install pygame pillow --quiet

echo.
echo Launching game...
echo.
python main.py

if %errorlevel% neq 0 (
    echo.
    echo Something went wrong launching the game.
    echo Please take a screenshot of this window and share it for help.
    pause
)
