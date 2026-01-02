# =============================================================================
# VPS NATIVE DEPLOY - ILUMINATI SYSTEM
# Deploys Native Nginx + Systemd + Python Code to Ubuntu 24
# =============================================================================

# Konfiguracia (Load form deploy_vps_docker.ps1 style)
$VPS_IP = "80.211.196.34"
$VPS_USER = "root"
$LOCAL_SSH_DIR = "$env:USERPROFILE\.ssh"
$LOCAL_KEY_PATH = "$LOCAL_SSH_DIR\id_rsa"
$DEPLOY_DIR_LOCAL = "VPS_DEPLOY\native"
$REMOTE_TMP = "/tmp/deploy"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   ILUMINATI SYSTEM - Native Production Deployment" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Target: $VPS_USER@$VPS_IP"
Write-Host ""

# 1. Prepare Backend Zip (excluding heavy directories)
Write-Host "[1/4] Preparing Application Package..." -ForegroundColor Yellow
$ZipPath = "$DEPLOY_DIR_LOCAL\backend.zip"
if (Test-Path $ZipPath) { Remove-Item $ZipPath }

# We use a temporary folder to curate what we zip (avoiding venv/pycache)
$TempStage = "$env:TEMP\iluminati_stage"
if (Test-Path $TempStage) { Remove-Item $TempStage -Recurse -Force }
New-Item -ItemType Directory -Path $TempStage | Out-Null
Copy-Item -Path "backend" -Destination $TempStage -Recurse

# Cleanup staging
Get-ChildItem -Path "$TempStage\backend" -Recurse -Include "__pycache__", "venv", ".pytest_cache", ".git" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Zip it
Compress-Archive -Path "$TempStage\backend" -DestinationPath $ZipPath -Force
Write-Host "Package created at $ZipPath" -ForegroundColor Green

# 2. Upload Files
Write-Host "[2/4] Uploading Files to VPS..." -ForegroundColor Yellow
# Create remote dir
ssh -i $LOCAL_KEY_PATH -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP "mkdir -p $REMOTE_TMP"

# Upload Configs & Script
scp -i $LOCAL_KEY_PATH "$DEPLOY_DIR_LOCAL\deploy_native.sh" "$VPS_USER@$VPS_IP:$REMOTE_TMP/"
scp -i $LOCAL_KEY_PATH "$DEPLOY_DIR_LOCAL\pro.icoatlas.sk.conf" "$VPS_USER@$VPS_IP:$REMOTE_TMP/"
scp -i $LOCAL_KEY_PATH "$DEPLOY_DIR_LOCAL\icoatlas-pro-api.service" "$VPS_USER@$VPS_IP:$REMOTE_TMP/"

# Upload Backend Zip
Write-Host "Uploading backend.zip (this may take a moment)..."
scp -i $LOCAL_KEY_PATH $ZipPath "$VPS_USER@$VPS_IP:$REMOTE_TMP/"

Write-Host "Files uploaded." -ForegroundColor Green

# 3. Execute Deployment
Write-Host "[3/4] Executing Remote Deployment Script..." -ForegroundColor Yellow
# Make script executable and run it
# We pass through the bash command
$Cmd = "chmod +x $REMOTE_TMP/deploy_native.sh && $REMOTE_TMP/deploy_native.sh"

ssh -i $LOCAL_KEY_PATH $VPS_USER@$VPS_IP $Cmd

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
    Write-Host "Verify at https://pro.icoatlas.sk"
}
else {
    Write-Host ""
    Write-Host "❌ DEPLOYMENT FAILED with code $LASTEXITCODE" -ForegroundColor Red
}

# Cleanup Local
Remove-Item $ZipPath -ErrorAction SilentlyContinue
Remove-Item $TempStage -Recurse -Force -ErrorAction SilentlyContinue
