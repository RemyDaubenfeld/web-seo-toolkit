#!/bin/bash
# Script de build PyInstaller
# Génère un exécutable standalone dans le dossier dist/

cd "$(dirname "$0")"

VENV_DIR=".venv-build"

echo "🐍 Création du venv de build..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "📦 Installation de PyInstaller..."
pip install --upgrade pip pyinstaller --quiet

# Installe les dépendances du projet si elles existent
if [ -f "requirements.txt" ]; then
    echo "📋 Installation des dépendances..."
    pip install -r requirements.txt --quiet
fi

echo "🔨 Compilation en cours..."
pyinstaller \
    --onefile \
    --windowed \
    --name "WebSEOToolkit" \
    --add-data "requirements.txt:." \
    main.py

deactivate

echo ""
echo "✅ Build terminé ! L'exécutable se trouve dans : dist/WebSEOToolkit"