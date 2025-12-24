# ================================
# ALF Universal Launcher
# ================================

Write-Host "=== Adaptive Learning Framework Launcher ===" -ForegroundColor Cyan

# 1. Ga naar de map waar dit script staat
Set-Location "$PSScriptRoot"

# 2. Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Install it from https://www.python.org" -ForegroundColor Red
    exit
}

# 3. Dependencies installeren indien nodig
if (Test-Path "requirements.txt") {
    Write-Host "Checking Python dependencies..."
    python -m pip install -r requirements.txt
}

# 4. Start ALF
Write-Host "Starting ALF..." -ForegroundColor Green
python alf_app.py

