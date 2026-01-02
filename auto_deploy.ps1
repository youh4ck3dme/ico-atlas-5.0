# =============================================================================
# AUTOMATIZOVANY DEPLOY SCRIPT (SSH KEY SETUP + DEPLOY) - OPRAVENA VERZIA
# =============================================================================

# Konfiguracia
$VPS_IP = "80.211.196.34"
$VPS_USER = "root"
$LOCAL_SSH_DIR = "$env:USERPROFILE\.ssh"
$LOCAL_KEY_PATH = "$LOCAL_SSH_DIR\id_rsa"
$DEPLOY_DIR = "VPS_DEPLOY"

Write-Host "=== AUTOMATICKY DEPLOY ILUMINATI SYSTEM ===" -ForegroundColor Cyan
Write-Host "Ciel: $VPS_USER@$VPS_IP" -ForegroundColor Gray

# 1. KONTROLA A VYTVORENIE SSH KLUCA
# ----------------------------------
if (-not (Test-Path "$LOCAL_KEY_PATH")) {
    Write-Host "[1/5] Generujem novy SSH kluc (id_rsa)..." -ForegroundColor Yellow
    
    # Vytvori .ssh adresar ak neexistuje
    if (-not (Test-Path $LOCAL_SSH_DIR)) {
        New-Item -ItemType Directory -Force -Path $LOCAL_SSH_DIR | Out-Null
    }

    # Opraveny prikaz pre generovanie kluca bez hesla v PowerShell
    # Pouzijeme '""' pre prazdne heslo
    cmd /c "ssh-keygen -t rsa -b 4096 -f ""$LOCAL_KEY_PATH"" -N """""

    if (-not (Test-Path "$LOCAL_KEY_PATH")) {
        Write-Host "❌ Nepodarilo sa vygenerovat SSH kluc. Skuste to rucne prikazom:" -ForegroundColor Red
        Write-Host "ssh-keygen -t rsa -b 4096 -f ""$LOCAL_KEY_PATH"" -N """""
        exit 1
    }
    Write-Host "Kluc vygenerovany." -ForegroundColor Green
}
else {
    Write-Host "[1/5] SSH kluc uz existuje." -ForegroundColor Green
}

# 2. NASTAVENIE BEZHESLOVEHO PRISTUPU
# -----------------------------------
Write-Host "[2/5] Cakam na dostupnosť servera (Port 22)..." -ForegroundColor Yellow

# Loopa pre cakanie na nabehnutie servera
$MaxRetries = 100
$RetryCount = 0

while ($true) {
    # Test portu 22
    $conn = Test-NetConnection $VPS_IP -Port 22 -InformationLevel Quiet
    if ($conn) {
        Write-Host "✅ Server je online (Port 22 otvoreny)!" -ForegroundColor Green
        break
    }
    
    $RetryCount++
    if ($RetryCount -ge $MaxRetries) {
        Write-Host "❌ Server stale neodpoveda po 100 pokusoch. Skontrolujte VNC konzolu a firewall." -ForegroundColor Red
        exit 1
    }
    
    Write-Host "⏳ Cakam na server... ($RetryCount/$MaxRetries) - (Ak to trva dlho, RESTARTUJTE VPS v admine)" -ForegroundColor Gray
    Start-Sleep -Seconds 10
}

Write-Host "Kopirujem SSH kluc na server..." -ForegroundColor Yellow

$PubKeyPath = "$LOCAL_KEY_PATH.pub"
if (-not (Test-Path $PubKeyPath)) {
    Write-Host "❌ Verejny kluc (id_rsa.pub) nebol najdeny!" -ForegroundColor Red
    exit 1
}

$PubKey = Get-Content $PubKeyPath
if ([string]::IsNullOrWhiteSpace($PubKey)) {
    Write-Host "❌ Verejny kluc je prazdny!" -ForegroundColor Red
    exit 1
}

Write-Host "      ⚠️  TERAZ ZADAJTE HESLO K VPS (Poklop123#####) POSLEDNYKRAT ⚠️" -ForegroundColor Red

# Prikaz na vytvorenie .ssh zlozky a pridanie kluca
$RemoteCmd = "mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '$PubKey' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

ssh $VPS_USER@$VPS_IP $RemoteCmd

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Chyba pri kopirovani kluca." -ForegroundColor Red
    Write-Host "   Moze ist o zlyhanie siete (Connection refused) alebo nespravne heslo."
    Write-Host "   Skontrolujte, ci server bezi a ci je IP adresa spravna ($VPS_IP)"
    exit 1
}
Write-Host "✅ Kluc uspesne skopirovany." -ForegroundColor Green

# 3. TEST PRIPOJENIA
# ------------------
Write-Host "[3/5] Testujem pripojenie bez hesla..." -ForegroundColor Yellow
ssh -o BatchMode=yes -o ConnectTimeout=10 $VPS_USER@$VPS_IP "echo 'Connection OK'" | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Bezheslove pripojenie funkcne!" -ForegroundColor Green
}
else {
    Write-Host "❌ Bezheslove pripojenie zlyhalo." -ForegroundColor Red
    exit 1
}

# 4. KOPIROVANIE SUBOROV
# ----------------------
Write-Host "[4/5] Nahravam deploy skripty na server..." -ForegroundColor Yellow
# Opravena syntax pre scp
scp -o BatchMode=yes -r ".\$DEPLOY_DIR" "${VPS_USER}@${VPS_IP}:/root/"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Subory nahrane." -ForegroundColor Green
}
else {
    Write-Host "❌ Chyba pri nahravani suborov." -ForegroundColor Red
    exit 1
}

# 5. SPUSTENIE DEPLOYU
# --------------------
Write-Host "[5/5] SPUSTAM DEPLOYMENT NA VPS..." -ForegroundColor Magenta
Write-Host "      (Toto moze trvat niekolko minut - sledujte vystup)" -ForegroundColor Gray
Write-Host "------------------------------------------------------" -ForegroundColor Gray

ssh -o BatchMode=yes $VPS_USER@$VPS_IP "chmod +x /root/$DEPLOY_DIR/deploy.sh && /root/$DEPLOY_DIR/deploy.sh"

Write-Host "------------------------------------------------------" -ForegroundColor Gray
Write-Host "✅✅✅ HOTOVO! Aplikacia by mala bezat na https://pro.icoatlas.sk" -ForegroundColor Cyan
