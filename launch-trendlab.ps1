# launch-trendlab.ps1
# Author: Jagdev Singh Dosanjh
# Purpose: Launch Trading Settings Lab with all integrated phases

Write-Host "Launching Trading Settings Lab..." -ForegroundColor Cyan

# Step 1: Navigate to project folder
Set-Location "D:\trading_settings_lab"

# Step 2: Activate virtual environment (if exists)
$VenvPath = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $VenvPath) {
    Write-Host "🔄 Activating virtual environment..."
    & $VenvPath
} else {
    Write-Host "No virtual environment found. Skipping activation..." -ForegroundColor Yellow
}

# Step 3: Run Streamlit app
Write-Host "Running Streamlit app..."
streamlit run app.py

# Step 4: Log ceremonial launch
$LogPath = ".\logs\launch_log.txt"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content $LogPath "$Timestamp - Trading Settings Lab launched by Jagdev Singh Dosanjh"

Write-Host "✅ App launched successfully. All phases are already integrated." -ForegroundColor Green
