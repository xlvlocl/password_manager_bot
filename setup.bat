@echo off
rmdir /s /q .git
del README.md .gitignore requirements.txt setup.sh
python setup.py
timeout /t 2 /nobreak >nul
del setup.py
del setup.bat