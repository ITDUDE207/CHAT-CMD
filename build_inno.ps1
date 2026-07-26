$ErrorActionPreference = "Stop"

Write-Host "Installing PyInstaller..." -ForegroundColor Green
python -m pip install --user pyinstaller

Write-Host "Building console executable..." -ForegroundColor Green
python -m PyInstaller --onefile --console --name chatapp .\legacy\main.py

Write-Host "Checking for Inno Setup..." -ForegroundColor Green
$inno = Get-Command iscc -ErrorAction SilentlyContinue
if (-not $inno) {
    Write-Host "Inno Setup was not found. Install it from https://jrsoftware.org/isinfo.php and then run this script again." -ForegroundColor Yellow
    exit 0
}

Write-Host "Creating Inno Setup installer..." -ForegroundColor Green
@'
[Setup]
AppName=ChatApp
AppVersion=1.0
DefaultDirName={autopf}\ChatApp
DefaultGroupName=ChatApp
OutputDir=.
OutputBaseFilename=chatapp-setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\chatapp.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ChatApp"; Filename: "{app}\chatapp.exe"
'@ | Set-Content .\chatapp.iss

iscc .\chatapp.iss
Write-Host "Installer created at chatapp-setup.exe" -ForegroundColor Green
