# =============================================================================
# FIX PRODUCTION SCRIPT
# Puts missing pieces together: .env, Unzip Code, Start DB
# =============================================================================

$VPS_IP = "80.211.196.34"
$VPS_USER = "root"
$KEY_PATH = "$env:USERPROFILE\.ssh\id_rsa"

Write-Host "🔧 Fixing Production..." -ForegroundColor Yellow

# 1. Create .env file locally
$EnvContent = @"
DATABASE_URL=postgresql://iluminati_user:IluminatiSecurePass2026@localhost:5432/iluminati_db
SECRET_KEY=production-secret-key-fixed
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://pro.icoatlas.sk,http://localhost
ENVIRONMENT=production
"@
$EnvPath = "$env:TEMP\prod.env"
Set-Content -Path $EnvPath -Value $EnvContent

# 1b. Create Zip
Write-Host "Creating backend.zip..."
$ZipPath = "$env:TEMP\backend.zip"
if (Test-Path $ZipPath) { Remove-Item $ZipPath }
# Copy to temp stage to separate from venv
$TempStage = "$env:TEMP\iluminati_fix"
if (Test-Path $TempStage) { Remove-Item $TempStage -Recurse -Force }
New-Item -ItemType Directory -Path $TempStage | Out-Null
Copy-Item -Path "backend" -Destination $TempStage -Recurse
# Cleanup
Get-ChildItem -Path "$TempStage\backend" -Recurse -Include "__pycache__", "venv", ".pytest_cache", ".git" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
# Zip
Compress-Archive -Path "$TempStage\backend" -DestinationPath $ZipPath -Force

# 2. Upload Files
Write-Host "Uploading Files..."
scp -i $KEY_PATH $EnvPath "$($VPS_USER)@$($VPS_IP):/var/www/icoatlas-pro/.env"
scp -i $KEY_PATH $ZipPath "$($VPS_USER)@$($VPS_IP):/tmp/deploy/backend.zip"

# 3. Remote Fixes
Write-Host "Executing Remote Fixes..."
$Cmd = "apt install -y unzip; unzip -o /tmp/deploy/backend.zip -d /var/www/icoatlas-pro/; chown -R www-data:www-data /var/www/icoatlas-pro; chmod -R 755 /var/www/icoatlas-pro; docker start iluminati_postgres; docker start iluminati_redis; systemctl restart icoatlas-pro-api; sleep 2; systemctl status icoatlas-pro-api --no-pager"

ssh -i $KEY_PATH $VPS_USER@$VPS_IP $Cmd

Write-Host "Done. Try verifying now." -ForegroundColor Green
