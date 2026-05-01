@echo off
echo =======================================================
echo NEX-PULSE AI OPTIMIZER - Compilacion Segura
echo =======================================================
echo.
echo Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo Empaquetando con PyInstaller (One-Dir Mode + UAC Admin)...
echo Este proceso usa --onedir para evitar detecciones de antivirus
echo.

python -m PyInstaller --noconfirm ^
    --onedir ^
    --noconsole ^
    --name "NEX-PULSE-Agent" ^
    --uac-admin ^
    --clean ^
    --add-data "src/config.py;." ^
    src/main.py

echo.
if %errorlevel% neq 0 (
    echo [ERROR] La compilacion ha fallado. Verifica los logs.
    pause
    exit /b %errorlevel%
)

echo [EXITO] Compilacion terminada. Tu archivo EXE esta en la carpeta dist\NEX-PULSE-Agent\
pause
