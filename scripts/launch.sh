#!/bin/bash
cd "$(dirname "$0")/.."

VENV_DIR=".venv"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed."
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    if [ -f "requirements.txt" ]; then
        echo "📦 Installing dependencies..."
        pip install -r requirements.txt --quiet
    fi
else
    source "$VENV_DIR/bin/activate"
fi

python3 main.py