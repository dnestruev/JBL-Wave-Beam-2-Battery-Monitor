#!/bin/bash
echo "========================================"
echo "  JBL Wave Beam 2 Battery Monitor"
echo "  Установка зависимостей"
echo "========================================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[ОШИБКА] Python не найден!"
    echo "Установите Python 3.7 или выше"
    exit 1
fi

echo "[OK] Python найден"
echo ""

echo "Установка PyQt6..."
pip3 install -r requirements.txt

echo ""
echo "========================================"
echo "  Установка завершена!"
echo "  Запустите: python3 main.py"
echo "========================================"
