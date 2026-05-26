#!/bin/bash
# Script de build PyInstaller
# Génère un exécutable standalone dans le dossier dist/

cd "$(dirname "$0")"

echo "📦 Installation de PyInstaller..."
pip install pyinstaller --quiet

echo "🔨 Compilation en cours..."
pyinstaller \
    --onefile \
    --windowed \
    --name "WebSEOToolkit" \
    --add-data "requirements.txt:." \
    main.py

echo ""
echo "✅ Build terminé ! L'exécutable se trouve dans : dist/WebSEOToolkit"