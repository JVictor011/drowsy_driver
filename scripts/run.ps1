param(
  [string]$ProjectRoot = "C:\DEV\TCC\drowsy_driver"
)
Set-Location $ProjectRoot
if (!(Test-Path ".\.venv\Scripts\python.exe")) {
  py -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python -m pip install --upgrade pip
  python -m pip install --no-cache-dir -r requirements.txt
} else {
  .\.venv\Scripts\Activate.ps1
}
python .\src\drowsy_driver\app.py
