# Trend Lab Integration Script - Phases 1 to 40
# Author: Jagdev Singh Dosanjh
# Purpose: Integrate all developed phases into deployed Streamlit app

Write-Host "Starting Full Integration: Phases 1-40..." -ForegroundColor Cyan

# Step 1: Navigate to app directory
$AppPath = "D:\trading_settings_lab"
Set-Location $AppPath

# Step 2: Pull latest updates from Git (if versioned)
Write-Host "Pulling latest code updates..."
git pull origin main

# Step 3: Create core folders for each layer
Write-Host "Creating core folders..."
New-Item -ItemType Directory -Path ".\indicators" -Force
New-Item -ItemType Directory -Path ".\strategies" -Force
New-Item -ItemType Directory -Path ".\portfolio" -Force
New-Item -ItemType Directory -Path ".\narration" -Force
New-Item -ItemType Directory -Path ".\optimization" -Force
New-Item -ItemType Directory -Path ".\cognition" -Force
New-Item -ItemType Directory -Path ".\emotion" -Force
New-Item -ItemType Directory -Path ".\identity" -Force
New-Item -ItemType Directory -Path ".\narrative" -Force
New-Item -ItemType Directory -Path ".\rituals" -Force
New-Item -ItemType Directory -Path ".\archetypes" -Force
New-Item -ItemType Directory -Path ".\worldmap" -Force
New-Item -ItemType Directory -Path ".\seasons" -Force
New-Item -ItemType Directory -Path ".\festivals" -Force
New-Item -ItemType Directory -Path ".\mythic_trials" -Force
New-Item -ItemType Directory -Path ".\cosmic_layer" -Force
New-Item -ItemType Directory -Path ".\transcendence" -Force

# Step 4: Copy all phase modules into pages
Write-Host "Copying phase modules..."
$PhaseModules = @(
    "phase01_indicators.py", "phase02_strategy.py", "phase03_portfolio.py", "phase04_narration.py",
    "phase05_backtest.py", "phase06_equitycurve.py", "phase07_riskmetrics.py", "phase08_tradejournal.py",
    "phase09_plotting.py", "phase10_pdfreport.py", "phase11_cli.py", "phase12_yaml.py",
    "phase13_multistrategy.py", "phase14_optimizer.py", "phase15_grading.py", "phase16_audio.py",
    "phase17_teacherpanel.py", "phase18_leaderboard.py", "phase19_sessiontracker.py", "phase20_export.py",
    "phase21_comparison.py", "phase22_portfolio_sim.py", "phase23_live_trading.py", "phase24_competitions.py",
    "phase25_social.py", "phase26_collaboration.py", "phase27_knowledgegraph.py", "phase28_adaptive.py",
    "phase29_cognition.py", "phase30_emotion.py", "phase31_purpose.py", "phase32_narrative.py",
    "phase33_rituals.py", "phase34_archetypes.py", "phase35_worldmap.py", "phase36_seasons.py",
    "phase37_festivals.py", "phase38_mythic.py", "phase39_cosmic.py", "phase40_transcendence.py"
)

foreach ($module in $PhaseModules) {
    Copy-Item ".\expansions\$module" ".\pages\" -Force
}

# Step 5: Update sidebar navigation
Write-Host "Updating sidebar navigation..."
$SidebarPath = ".\core\sidebar_config.yaml"
Add-Content $SidebarPath "`n# Phase Modules Navigation"
foreach ($module in $PhaseModules) {
    $name = $module -replace "_", " " -replace ".py", ""
    Add-Content $SidebarPath "- $name"
}

# Step 6: Restart Streamlit app
Write-Host "Restarting Streamlit app..."
Stop-Process -Name "streamlit" -Force -ErrorAction SilentlyContinue
Start-Process "streamlit" -ArgumentList "run app.py"

# Step 7: Log integration event
$LogPath = ".\logs\integration_log.txt"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content $LogPath "$Timestamp - Full Phase Integration (1-40) completed by Jagdev Singh Dosanjh"

Write-Host "All Phases Integrated Successfully." -ForegroundColor Green
