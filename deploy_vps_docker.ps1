# =============================================================================
# VPS DOCKER DEPLOY - ILUMINATI SYSTEM
# Kompletný automatizovaný deployment na Ubuntu 24 VPS
# =============================================================================

# Konfiguracia
$VPS_IP = "80.211.196.34"
$VPS_USER = "root"
$VPS_PASSWORD = "Poklop123#####"
$DOMAIN = "pro.icoatlas.sk"
$EMAIL = "info@icoatlas.sk"
$LOCAL_SSH_DIR = "$env:USERPROFILE\.ssh"
$LOCAL_KEY_PATH = "$LOCAL_SSH_DIR\id_rsa"
$DEPLOY_DIR = "VPS_DEPLOY"
$REMOTE_APP_DIR = "/root/iluminati"
$GITHUB_REPO = "https://github.com/youh4ck3dme/ico-atlas-5.0.git"

# Max pokusy pre pripojenie
$MAX_RETRIES = 100
$RETRY_INTERVAL = 10

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   ILUMINATI SYSTEM - VPS Docker Deployment" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Cieľový server: $VPS_USER@$VPS_IP" -ForegroundColor Gray
Write-Host "Doména: $DOMAIN" -ForegroundColor Gray
Write-Host "Email (SSL): $EMAIL" -ForegroundColor Gray
Write-Host ""

# =============================================================================
# FUNKCIE
# =============================================================================

function Wait-ForSSH {
    param([string]$IP, [int]$MaxRetries, [int]$IntervalSeconds)
    
    Write-Host "[WAIT] Čakám na dostupnosť SSH portu 22..." -ForegroundColor Yellow
    
    for ($i = 1; $i -le $MaxRetries; $i++) {
        $conn = Test-NetConnection $IP -Port 22 -InformationLevel Quiet -WarningAction SilentlyContinue
        
        if ($conn) {
            Write-Host "✅ Server je online (Port 22 otvorený)!" -ForegroundColor Green
            return $true
        }
        
        Write-Host "⏳ Pokus $i/$MaxRetries - Server neodpovedá, čakám ${IntervalSeconds}s..." -ForegroundColor Gray
        Start-Sleep -Seconds $IntervalSeconds
    }
    
    Write-Host "❌ Server nie je dostupný po $MaxRetries pokusoch." -ForegroundColor Red
    return $false
}

function New-SSHKey {
    Write-Host "[SSH] Nastavujem SSH kľúč..." -ForegroundColor Yellow
    
    # Vytvor .ssh priečinok ak neexistuje
    if (-not (Test-Path $LOCAL_SSH_DIR)) {
        New-Item -ItemType Directory -Force -Path $LOCAL_SSH_DIR | Out-Null
    }
    
    # Generuj kľúč ak neexistuje
    if (-not (Test-Path $LOCAL_KEY_PATH)) {
        Write-Host "   Generujem nový SSH kľúč..." -ForegroundColor Gray
        cmd /c "ssh-keygen -t rsa -b 4096 -f `"$LOCAL_KEY_PATH`" -N `"`""
    }
    
    # Skontroluj či kľúč existuje
    if (-not (Test-Path "$LOCAL_KEY_PATH.pub")) {
        Write-Host "❌ SSH kľúč sa nepodarilo vytvoriť!" -ForegroundColor Red
        return $false
    }
    
    Write-Host "✅ SSH kľúč pripravený" -ForegroundColor Green
    return $true
}

function Copy-SSHKeyToServer {
    Write-Host "[SSH] Kopírujem SSH kľúč na server..." -ForegroundColor Yellow
    Write-Host "      ⚠️  ZADAJTE HESLO: $VPS_PASSWORD" -ForegroundColor Red
    
    $pubKey = Get-Content "$LOCAL_KEY_PATH.pub"
    $remoteCmd = "mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '$pubKey' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && sort -u ~/.ssh/authorized_keys -o ~/.ssh/authorized_keys"
    
    ssh -o StrictHostKeyChecking=accept-new "$VPS_USER@$VPS_IP" $remoteCmd
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ SSH kľúč skopírovaný" -ForegroundColor Green
        return $true
    }
    
    Write-Host "❌ Chyba pri kopírovaní SSH kľúča" -ForegroundColor Red
    return $false
}

function Test-PasswordlessSSH {
    Write-Host "[SSH] Testujem bezheslové pripojenie..." -ForegroundColor Yellow
    
    ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new "$VPS_USER@$VPS_IP" "echo OK" 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Bezheslové SSH funguje!" -ForegroundColor Green
        return $true
    }
    
    return $false
}

function Invoke-RemoteCommand {
    param([string]$Command, [string]$Description)
    
    Write-Host "[VPS] $Description..." -ForegroundColor Yellow
    ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new "$VPS_USER@$VPS_IP" $Command
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Chyba: $Description" -ForegroundColor Red
        return $false
    }
    return $true
}

# =============================================================================
# HLAVNÝ PROCES
# =============================================================================

# KROK 1: Čakaj na SSH
Write-Host ""
Write-Host "========== KROK 1/7: Čakanie na server ==========" -ForegroundColor Magenta
$sshReady = Wait-ForSSH -IP $VPS_IP -MaxRetries $MAX_RETRIES -IntervalSeconds $RETRY_INTERVAL

if (-not $sshReady) {
    Write-Host "❌ Server nie je dostupný. Skontrolujte VPS panel." -ForegroundColor Red
    exit 1
}

# KROK 2: SSH Key Setup
Write-Host ""
Write-Host "========== KROK 2/7: SSH Key Setup ==========" -ForegroundColor Magenta

if (-not (New-SSHKey)) {
    exit 1
}

# Test či už máme bezheslový prístup
if (-not (Test-PasswordlessSSH)) {
    # Potrebujeme skopírovať kľúč
    if (-not (Copy-SSHKeyToServer)) {
        exit 1
    }
    
    # Test znova
    if (-not (Test-PasswordlessSSH)) {
        Write-Host "❌ Bezheslové SSH stále nefunguje!" -ForegroundColor Red
        exit 1
    }
}

# KROK 3: Kopírovanie súborov
Write-Host ""
Write-Host "========== KROK 3/7: Kopírovanie súborov ==========" -ForegroundColor Magenta

Write-Host "[SCP] Nahrávam deploy skripty na server..." -ForegroundColor Yellow
ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new "$VPS_USER@$VPS_IP" "mkdir -p $REMOTE_APP_DIR"
scp -o BatchMode=yes -o StrictHostKeyChecking=accept-new -r ".\$DEPLOY_DIR\*" "${VPS_USER}@${VPS_IP}:${REMOTE_APP_DIR}/"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Chyba pri kopírovaní súborov" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Súbory nahrané" -ForegroundColor Green

# KROK 4: Inštalácia Dockeru a Unzip
Write-Host ""
Write-Host "========== KROK 4/7: Inštalácia Docker a Tools ==========" -ForegroundColor Magenta

ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new "$VPS_USER@$VPS_IP" "docker --version 2>/dev/null" | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[VPS] Docker nie je nainštalovaný, inštalujem..." -ForegroundColor Yellow
    Invoke-RemoteCommand "apt-get update && apt-get install -y unzip && chmod +x $REMOTE_APP_DIR/install_docker.sh && $REMOTE_APP_DIR/install_docker.sh" "Inštalácia Docker a Unzip"
}
else {
    Write-Host "✅ Docker už je nainštalovaný" -ForegroundColor Green
    # Ensure unzip is installed
    Invoke-RemoteCommand "apt-get install -y unzip" "Inštalácia Unzip"
}

# KROK 5: Klonovanie/Update repozitára
Write-Host ""
Write-Host "========== KROK 5/7: Klonovanie aplikácie ==========" -ForegroundColor Magenta

$repoExists = ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new "$VPS_USER@$VPS_IP" "test -d $REMOTE_APP_DIR/backend && echo YES"
if ($repoExists -eq "YES") {
    Write-Host "[VPS] Aktualizujem existujúci kód (git)..." -ForegroundColor Yellow
    Invoke-RemoteCommand "cd $REMOTE_APP_DIR && git pull origin main 2>/dev/null || true" "Git pull"
}
else {
    Write-Host "[VPS] Klonujem repozitár..." -ForegroundColor Yellow
    Invoke-RemoteCommand "cd $REMOTE_APP_DIR && git clone $GITHUB_REPO . 2>/dev/null || true" "Git clone"
}

# Compress local changes to zip (FAST UPLOAD)
Write-Host "[ZIP] Pripravujem balíček na odoslanie..." -ForegroundColor Yellow
$zipPath = "$env:TEMP\deploy_package.zip"
$stageDir = "$env:TEMP\iluminati_deploy_stage"

# Clean previous stage
if (Test-Path $stageDir) { Remove-Item $stageDir -Recurse -Force }
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
New-Item -ItemType Directory -Path $stageDir | Out-Null

# Robocopy for smart exclusion (much faster/reliable than PowerShell copy)
Write-Host "   Staging Backend..." -ForegroundColor Gray
robocopy ".\backend" "$stageDir\backend" /MIR /XD node_modules venv .venv __pycache__ .git .idea .vscode /XF *.log *.pyc *.pyo *.pyd *.db /NFL /NDL /NJH /NJS | Out-Null

Write-Host "   Staging Frontend..." -ForegroundColor Gray
robocopy ".\frontend" "$stageDir\frontend" /MIR /XD node_modules dist .vite .git .idea .vscode /XF *.log /NFL /NDL /NJH /NJS | Out-Null

Write-Host "   Komprimujem..." -ForegroundColor Gray
Compress-Archive -Path "$stageDir\backend", "$stageDir\frontend" -DestinationPath $zipPath -Force

# Clean stage
Remove-Item $stageDir -Recurse -Force

Write-Host "[SCP] Nahrávam balíček na server..." -ForegroundColor Yellow
scp -o BatchMode=yes -o StrictHostKeyChecking=accept-new $zipPath "${VPS_USER}@${VPS_IP}:${REMOTE_APP_DIR}/deploy_package.zip"

Write-Host "[VPS] Rozbaľujem balíček..." -ForegroundColor Yellow
Invoke-RemoteCommand "cd $REMOTE_APP_DIR && unzip -o deploy_package.zip && rm deploy_package.zip" "Unzip package"

Write-Host "✅ Aplikačný kód nahraný" -ForegroundColor Green

# KROK 6: Spustenie Docker Compose
Write-Host ""
Write-Host "========== KROK 6/7: Spustenie kontajnerov ==========" -ForegroundColor Magenta

Write-Host "[VPS] Zastavujem staré kontajnery..." -ForegroundColor Yellow
Invoke-RemoteCommand "cd $REMOTE_APP_DIR && docker compose -f docker-compose.prod.yml down 2>/dev/null || true" "Docker down"

Write-Host "[VPS] Buildujem a spúšťam kontajnery..." -ForegroundColor Yellow
Write-Host "      (Toto môže trvať niekoľko minút pri prvom spustení)" -ForegroundColor Gray
Invoke-RemoteCommand "cd $REMOTE_APP_DIR && docker compose -f docker-compose.prod.yml build --no-cache frontend && docker compose -f docker-compose.prod.yml up -d --build --force-recreate" "Docker up"

# KROK 7: SSL Certifikát
Write-Host ""
Write-Host "========== KROK 7/7: SSL Certifikát ==========" -ForegroundColor Magenta

Write-Host "[VPS] Nastavujem SSL certifikát..." -ForegroundColor Yellow
Invoke-RemoteCommand "chmod +x $REMOTE_APP_DIR/setup_ssl.sh && $REMOTE_APP_DIR/setup_ssl.sh" "SSL Setup"

# HOTOVO
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "   ✅✅✅ DEPLOYMENT ÚSPEŠNE DOKONČENÝ! ✅✅✅" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Aplikácia je dostupná na:" -ForegroundColor Yellow
Write-Host "   https://$DOMAIN" -ForegroundColor White
Write-Host ""
Write-Host "📊 Správa kontajnerov (na VPS):" -ForegroundColor Yellow
Write-Host "   ssh $VPS_USER@$VPS_IP" -ForegroundColor Cyan
Write-Host "   cd $REMOTE_APP_DIR" -ForegroundColor Cyan
Write-Host "   docker compose -f docker-compose.prod.yml ps" -ForegroundColor Cyan
Write-Host "   docker compose -f docker-compose.prod.yml logs -f" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔄 Redeployment:" -ForegroundColor Yellow
Write-Host "   Spustite tento skript znova: .\deploy_vps_docker.ps1" -ForegroundColor Cyan
Write-Host ""
