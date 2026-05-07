#!/bin/bash
# Build script for Thesis and FloatingTodo applications
# Note: This script generates .app files for macOS and executables for Linux

set -e

echo "================================================"
echo "Building Thesis Apps and FloatingTodo"
echo "================================================"

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "Error: PyInstaller is not installed"
    echo "Please install it with: pip install pyinstaller"
    exit 1
fi

# Create dist directory if it doesn't exist
mkdir -p dist

# Build Thesis Advanced
echo ""
echo "Building Thesis Checker Advanced..."
pyinstaller --noconsole --onefile \
    --name "ThesisChecker_Advanced" \
    --collect-all PyQt6 \
    --collect-all Qt6 \
    --hidden-import=thesis_themes \
    thesis_app_advanced.py

# Build Thesis Modern
echo ""
echo "Building Thesis Checker Modern..."
pyinstaller --noconsole --onefile \
    --name "ThesisChecker_Modern" \
    --collect-all PyQt6 \
    --collect-all Qt6 \
    thesis_app_modern.py

# Build Thesis Launcher
echo ""
echo "Building Thesis Launcher..."
pyinstaller --noconsole --onefile \
    --name "ThesisChecker" \
    --collect-all PyQt6 \
    --collect-all Qt6 \
    run_thesis.py

# Build Thesis Classic
echo ""
echo "Building Thesis Checker Classic..."
pyinstaller --noconsole --onefile \
    --name "ThesisChecker_Classic" \
    thesis_checker.py

# Build FloatingTodo
echo ""
echo "Building FloatingTodo..."
pyinstaller --noconsole --onefile \
    --name "FloatingTodo" \
    main.py

echo ""
echo "================================================"
echo "Build Complete!"
echo "================================================"
echo ""
echo "Generated executables in 'dist' folder:"
echo "  - ThesisChecker_Advanced (Recommended)"
echo "  - ThesisChecker_Modern"
echo "  - ThesisChecker (Launcher)"
echo "  - ThesisChecker_Classic"
echo "  - FloatingTodo"
echo ""
