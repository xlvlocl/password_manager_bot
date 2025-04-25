rm -rf .git
rm -f README.md .gitignore requirements.txt setup.bat
python3 setup.py
sleep 2
rm -rf setup.py
rm -rf setup.sh