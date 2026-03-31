@echo off
title Compilador I.S.D.I - Windows
echo =======================================================
echo    CONSTRUYENDO APLICACION INSTALABLE (CARPETA) WINDOWS
echo =======================================================
echo [1/2] Verificando e Instalando dependencias...
pip install -r requirements.txt pyinstaller
echo.
echo [2/2] Empaquetando la aplicacion (Modo Carpeta y Path Src)...
REM Usamos pyinstaller directamente para forzar el modo carpeta y arreglar el PATH de importaciones
pyinstaller --noconfirm --windowed --onedir --name "ISDI-PC" --paths src --add-data "src;src" src/main.py
echo.
echo =======================================================
echo [ OK ] ¡Compilacion Finalizada!
echo El programa se encuentra DENTRO de la carpeta:
echo 'dist/ISDI-PC/' y el archivo ejecutable esta ahi dentro.
echo =======================================================
pause
