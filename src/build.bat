@echo off
cd %~dp0
pyinstaller --onefile las2mesh.py --icon ..\material\icon.ico
copy /Y .\dist\las2mesh.exe ..\release