#!/bin/bash
cd "$(dirname "$0")"

BINARY="WebSEOToolkit-linux"
INSTALL_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/webseo-toolkit.desktop"

echo "🔧 Installing Web SEO Toolkit..."

if [ ! -f "$BINARY" ]; then
    echo "❌ Binary '$BINARY' not found. Make sure install.sh is in the same folder as the binary."
    exit 1
fi

if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "⚠️  Missing dependency: python3-tk. Installing..."
    sudo apt install python3-tk -y
fi

mkdir -p "$INSTALL_DIR"
cp "$BINARY" "$INSTALL_DIR/WebSEOToolkit"
chmod +x "$INSTALL_DIR/WebSEOToolkit"

mkdir -p "$DESKTOP_DIR"
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Web SEO Toolkit
Comment=SEO Audit, Markdown Converter and Sitemap Generator
Exec=$INSTALL_DIR/WebSEOToolkit
Icon=applications-internet
Terminal=false
Categories=Utility;Network;
EOF

chmod +x "$DESKTOP_FILE"

if command -v update-desktop-database &>/dev/null; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null
fi

echo ""
echo "✅ Installation complete!"
echo "   → Launch the app from your application menu"
echo "   → Or from the terminal: WebSEOToolkit"