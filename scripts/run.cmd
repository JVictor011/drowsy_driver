@echo off
set ROOT=C:\DEV\TCC\drowsy_driver
cd /d %ROOT%
if not exist .venv\Scripts\python.exe (
  py -m venv .venv
  call .venv\Scripts\activate.bat
  python -m pip install --upgrade pip
  python -m pip install --no-cache-dir -r requirements.txt
) else (
  call .venv\Scripts\activate.bat
)
python .\src\drowsy_driver\app.py