#!/bin/bash
# PyInstaller build script
# Generates a standalone executable in the dist/ folder

cd "$(dirname "$0")/.."

VENV_DIR=".venv-build"

echo "🐍 Creating build virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "📦 Installing PyInstaller..."
pip install --upgrade pip pyinstaller --quiet

if [ -f "requirements.txt" ]; then
    echo "📋 Installing project dependencies..."
    pip install -r requirements.txt --quiet
fi

echo "🔨 Building..."
pyinstaller \
    --onefile \
    --windowed \
    --name "WebSEOToolkit" \
    main.py

deactivate

echo ""
echo "✅ Build complete! Executable located at: dist/WebSEOToolkit"