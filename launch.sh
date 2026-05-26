#!/bin/bash
cd "$(dirname "$0")"

VENV_DIR=".venv"

# Vérification de Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé."
    exit 1
fi

# Création du venv si absent
if [ ! -d "$VENV_DIR" ]; then
    echo "🐍 Création de l'environnement virtuel..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    if [ -f "requirements.txt" ]; then
        echo "📦 Installation des dépendances..."
        pip install -r requirements.txt --quiet
    fi
else
    source "$VENV_DIR/bin/activate"
fi

python3 main.py