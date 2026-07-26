$ErrorActionPreference = "Stop"

Write-Host "Installing PyInstaller..." -ForegroundColor Green
python -m pip install --user pyinstaller

Write-Host "Building console executable..." -ForegroundColor Green
python -m PyInstaller --onefile --console --name chatapp .\legacy\main.py

Write-Host "Done! Output is in dist\chatapp.exe" -ForegroundColor Green
