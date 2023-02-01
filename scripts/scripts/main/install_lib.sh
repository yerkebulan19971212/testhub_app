#!/bin/bash
source "env/bin/activate"
echo "Активирована виртуальная среда"
python -m pip install --upgrade pip
echo "Pip update"
pip install -r r.txt
echo "Установка завершена"
