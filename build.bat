@echo off
REM Build script for Thesis and FloatingTodo applications
REM Requires: PyInstaller installed (pip install pyinstaller)

setlocal enabledelayedexpansion

echo ================================================
echo Building Thesis Apps and FloatingTodo
echo ================================================

REM Check if PyInstaller is installed
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: PyInstaller is not installed
    echo Please install it with: pip install pyinstaller
    exit /b 1
)

REM Create dist directory if it doesn't exist
if not exist "dist" mkdir dist

REM Build Thesis Advanced
echo.
echo Building Thesis Checker Advanced...
pyinstaller --noconsole --onefile ^
    --name "ThesisChecker_Advanced" ^
    --collect-all PyQt6 ^
    --collect-all Qt6 ^
    --hidden-import=thesis_themes ^
    thesis_app_advanced.py
if %errorlevel% neq 0 (
    echo Error building Thesis Checker Advanced
    exit /b 1
)

REM Build Thesis Modern
echo.
echo Building Thesis Checker Modern...
pyinstaller --noconsole --onefile ^
    --name "ThesisChecker_Modern" ^
    --collect-all PyQt6 ^
    --collect-all Qt6 ^
    thesis_app_modern.py
if %errorlevel% neq 0 (
    echo Error building Thesis Checker Modern
    exit /b 1
)

REM Build Thesis Launcher
echo.
echo Building Thesis Launcher...
pyinstaller --noconsole --onefile ^
    --name "ThesisChecker" ^
    --collect-all PyQt6 ^
    --collect-all Qt6 ^
    run_thesis.py
if %errorlevel% neq 0 (
    echo Error building Thesis Launcher
    exit /b 1
)

REM Build Thesis Classic
echo.
echo Building Thesis Checker Classic...
pyinstaller --noconsole --onefile ^
    --name "ThesisChecker_Classic" ^
    thesis_checker.py
if %errorlevel% neq 0 (
    echo Error building Thesis Checker Classic
    exit /b 1
)

REM Build FloatingTodo
echo.
echo Building FloatingTodo...
pyinstaller --noconsole --onefile ^
    --name "FloatingTodo" ^
    main.py
if %errorlevel% neq 0 (
    echo Error building FloatingTodo
    exit /b 1
)

echo.
echo ================================================
echo Build Complete!
echo ================================================
echo.
echo Generated executables in 'dist' folder:
echo   - ThesisChecker_Advanced.exe (Recommended)
echo   - ThesisChecker_Modern.exe
echo   - ThesisChecker.exe (Launcher)
echo   - ThesisChecker_Classic.exe
echo   - FloatingTodo.exe
echo.
