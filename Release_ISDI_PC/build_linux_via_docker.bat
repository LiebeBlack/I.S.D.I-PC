@echo off
title Compilador I.S.D.I - Linux via Docker
echo =======================================================
echo    COMPILANDO PARA LINUX (COMPATIBILIDAD VIRTUAL)
echo =======================================================
echo ADVERTENCIA: Docker Desktop debe de estar ejecutandose.
echo.
mkdir out 2>nul
echo [1/2] Construyendo el entorno base seguro...
docker build -t isdi-linux-builder .
IF %ERRORLEVEL% NEQ 0 (
    echo [!] Error: No se pudo conectar a Docker o compilar.
    pause
    exit /b %ERRORLEVEL%
)
echo [2/2] Empaquetando internamente y extrayendo las carpetas...
docker run --rm -v "%CD%\out:/app/out" isdi-linux-builder
echo.
echo =======================================================
echo [ OK ] ¡Compilacion Completada Exitosamente!
echo Revisa la subcarpeta: Release_ISDI_PC\out\dist\ISDI-PC\
echo =======================================================
pause
