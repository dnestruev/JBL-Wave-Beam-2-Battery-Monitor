@echo off
echo ========================================
echo   JBL Wave Beam 2 Battery Monitor
echo   Установка зависимостей
echo ========================================
echo.

echo Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден!
    echo Скачайте Python с https://python.org
    echo Не забудьте поставить галочку "Add Python to PATH"
    pause
    exit /b
)

echo [OK] Python найден
echo.

echo Установка PyQt6...
pip install -r requirements.txt

echo.
echo ========================================
echo   Установка завершена!
echo   Запустите run.bat для старта
echo ========================================
pause
