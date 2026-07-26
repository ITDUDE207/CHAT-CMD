$ErrorActionPreference = "Stop"

Write-Host "Installing installer tools..." -ForegroundColor Green
python -m pip install --user pyinstaller pywin32

Write-Host "Building Windows installer package..." -ForegroundColor Green
python -m PyInstaller --onefile --console --name chatapp .\legacy\main.py

Write-Host "Installing WiX Toolset if available..." -ForegroundColor Green
$wix = Get-Command candle -ErrorAction SilentlyContinue
if (-not $wix) {
    Write-Host "WiX Toolset not found. Install it from https://wixtoolset.org/ and then run the packaging step manually." -ForegroundColor Yellow
    exit 0
}

Write-Host "Creating MSI installer..." -ForegroundColor Green
@'
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" Name="ChatApp" Language="1033" Version="1.0.0" Manufacturer="CHAT-CMD" UpgradeCode="{11111111-2222-3333-4444-555555555555}">
    <Package InstallerVersion="200" Compressed="yes" InstallScope="perMachine" />
    <MediaTemplate />
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="ChatApp" />
      </Directory>
    </Directory>
    <ComponentGroup Id="ProductComponents">
      <Component Id="MainExe" Directory="INSTALLFOLDER" Guid="{66666666-7777-8888-9999-000000000000}">
        <File Id="ChatAppExe" Source="dist\chatapp.exe" KeyPath="yes" />
      </Component>
    </ComponentGroup>
    <Feature Id="MainFeature" Title="Main Feature" Level="1">
      <ComponentGroupRef Id="ProductComponents" />
    </Feature>
  </Product>
</Wix>
'@ | Set-Content .\chatapp.wxs

candle .\chatapp.wxs
light .\chatapp.wixobj
Move-Item .\chatapp.msi .\dist\chatapp.msi -Force
Write-Host "Installer created at dist\chatapp.msi" -ForegroundColor Green
