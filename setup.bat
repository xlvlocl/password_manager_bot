@echo off
rmdir /s /q .git
python setup.py
timeout /t 5 /nobreak >nul
del setup.py
del setup.sh
del setup.bat