#!/bin/bash
source "venv/bin/activate"
echo "Активирована виртуальная среда"
python -m pip install --upgrade pip
echo "Pip update"
pip install -r requirements.txt
echo "Установка завершена"
