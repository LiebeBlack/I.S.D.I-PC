#!/bin/bash
echo "======================================================="
echo "   CONSTRUYENDO APLICACION INSTALABLE PARA LINUX"
echo "======================================================="
echo "[1/2] Verificando dependencias..."
python3 -m pip install -r requirements.txt pyinstaller
echo ""
echo "[2/2] Empaquetando la aplicacion..."
pyinstaller --noconfirm --windowed --onedir --name "ISDI-PC" --paths src --add-data "src:src" src/main.py
echo ""
echo "======================================================="
echo "[ OK ] ¡Compilacion Finalizada!"
echo "La carpeta del ejecutable esta en 'dist/ISDI-PC/'"
echo "======================================================="
