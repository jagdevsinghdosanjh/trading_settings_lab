# Phase Expansion Script for Trading Settings Lab
# Author: Jagdev Singh Dosanjh
# Purpose: Integrate Phases 36–40 into deployed Streamlit app

Write-Host "🌟 Starting Mythic Expansion: Phases 36–40..." -ForegroundColor Cyan

# Step 1: Navigate to app directory
$AppPath = "C:\Users\YourUsername\trading-settings-lab"
Set-Location $AppPath

# Step 2: Pull latest updates from your Git repo (if versioned)
Write-Host "🔄 Pulling latest code updates..."
git pull origin main

# Step 3: Create new folders for seasonal and mythic layers
Write-Host "📁 Creating symbolic folders..."
New-Item -ItemType Directory -Path ".\realms" -Force
New-Item -ItemType Directory -Path ".\seasons" -Force
New-Item -ItemType Directory -Path ".\mythic_trials" -Force
New-Item -ItemType Directory -Path ".\cosmic_map" -Force

# Step 4: Copy new Python modules into app
Write-Host "📦 Copying new modules..."
Copy-Item ".\expansions\phase36_seasons.py" ".\pages\" -Force
Copy-Item ".\expansions\phase37_festivals.py" ".\pages\" -Force
Copy-Item ".\expansions\phase38_mythic.py" ".\pages\" -Force
Copy-Item ".\expansions\phase39_cosmic.py" ".\pages\" -Force
Copy-Item ".\expansions\phase40_transcendence.py" ".\pages\" -Force

# Step 5: Update navigation sidebar
Write-Host "🧭 Updating sidebar navigation..."
$SidebarPath = ".\core\sidebar_config.yaml"
Add-Content $SidebarPath "`n- Seasons & Festivals`n- Mythic Trials`n- Cosmic Map`n- Transcendence Ceremony"

# Step 6: Restart Streamlit app
Write-Host "🚀 Restarting Streamlit app..."
Stop-Process -Name "streamlit" -Force -ErrorAction SilentlyContinue
Start-Process "streamlit" -ArgumentList "run app.py"

# Step 7: Log ceremonial integration
$LogPath = ".\logs\integration_log.txt"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content $LogPath "$Timestamp — Phases 36–40 integrated by Jagdev Singh Dosanjh"

Write-Host "✅ Mythic Expansion Complete. Your universe now includes Seasons, Festivals, Myths, and Stars." -ForegroundColor Green
