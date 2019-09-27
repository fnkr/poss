REM https://bitbucket.org/anthony_tuininga/cx_freeze/issue/81/python-34-venv-importlib-attributeerror
REM %~dp0env\Scripts\pip install cx_freeze===?.?.?
REM %~dp0env\Scripts\python %~dp0env\Scripts\cxfreeze %~dp0poss.py

cxfreeze %~dp0poss.py^
 --include-path "%~dp0env\Lib\site-packages"^
 --include-modules "requests,pyperclip"^
 --exclude-modules "config"^
 --target-dir "%~dp0dist"^
 --icon "%~dp0icon.ico"^
 --compress -O
