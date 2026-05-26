#!/bin/bash
cd "$(dirname "$0")"

# Vérification de Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé."
    exit 1
fi

python3 main.py