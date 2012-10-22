@echo off
set scrDir=%~dp0
set scrPath=%scrDir%davetag.py
call %scrDir%/DaveTag/Scripts/activate.bat
python.exe %scrPath% %*
call %scrDir%/DaveTag/Scripts/deactivate.bat