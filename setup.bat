@echo off
rmdir /s /q .git
python script.py
timeout /t 5 /nobreak >nul
del setup.py
del setup.sh
del setup.bat