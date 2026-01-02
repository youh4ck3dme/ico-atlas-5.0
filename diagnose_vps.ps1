# VPS Diagnostic Script for ILUMINATI SYSTEM
$ErrorActionPreference = "Prevent"

$VPS_USER = "root"
$VPS_IP = "80.211.196.34"

$URL = "https://pro.icoatlas.sk"

function Test-Check {
    param([string]$Name, [scriptblock]$Action)
    Write-Host "[$Name]..." -NoNewline
    try {
        & $Action
        Write-Host " OK" -ForegroundColor Green
    }
    catch {
        Write-Host " FAILED" -ForegroundColor Red
        Write-Host "    Error: $_" -ForegroundColor Red
    }
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   ILUMINATI VPS DIAGNOSTIC TOOL v1.0   " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 1. SSH Connectivity
Test-Check "SSH Connection" {
    $res = ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new "$VPS_USER@$VPS_IP" "echo CONNECTED" 2>$null
    if ($res -ne "CONNECTED") { throw "Cannot connect via SSH" }
}

# 2. Docker Service Status
Test-Check "Docker Service" {
    ssh -o BatchMode=yes "$VPS_USER@$VPS_IP" "systemctl is-active docker" | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Docker service is not active" }
}

# 3. Disk Space Check
Test-Check "Disk Space (>10% free)" {
    $usage = ssh -o BatchMode=yes "$VPS_USER@$VPS_IP" "df -h / | tail -1 | awk '{print `$5}' | tr -d '%'"
    if ([int]$usage -gt 90) { throw "Disk usage is critically high: $usage%" }
    Write-Host " (Usage: $usage%)" -NoNewline -ForegroundColor Gray
}

# 4. Container Health Check
Write-Host "`nchecking containers..." -ForegroundColor Yellow
$containers = @("iluminati_backend", "iluminati_frontend", "iluminati_postgres", "iluminati_redis", "iluminati_nginx")

foreach ($c in $containers) {
    Test-Check "Container: $c" {
        $status = ssh -o BatchMode=yes "$VPS_USER@$VPS_IP" "docker inspect -f '{{.State.Status}}' $c 2>/dev/null"
        if ($status -ne "running") { throw "Container is not running (Status: $status)" }
        
        # Check health if available
        $health = ssh -o BatchMode=yes "$VPS_USER@$VPS_IP" "docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}no_check{{end}}' $c"
        if ($health -eq "unhealthy") { throw "Container is UNHEALTHY" }
    }
}

# 5. Database Connection Check (Remote)
Test-Check "Database Connection (Backend Logs)" {
    $log = ssh -o BatchMode=yes "$VPS_USER@$VPS_IP" "docker logs iluminati_backend --tail 50"
    if ($log -match "Connection refused") { throw "Backend cannot connect to DB" }
    if ($log -match "OperationalError") { throw "Database Operational Error" }
}

# 6. Public Endpoint Check
Test-Check "Public HTTPS Endpoint ($URL)" {
    try {
        $req = Invoke-WebRequest -Uri $URL -Method Head -ErrorAction Stop
        if ($req.StatusCode -ne 200) { throw "Status Code: $($req.StatusCode)" }
    }
    catch {
        throw "Website is unreachable: $_"
    }
}

# 7. SSL Certificate Validity
Test-Check "SSL Certificate" {
    $tcp = New-Object Net.Sockets.TcpClient
    $tcp.Connect("pro.icoatlas.sk", 443)
    $stream = $tcp.GetStream()
    $ssl = New-Object Net.Security.SslStream($stream)
    $ssl.AuthenticateAsClient("pro.icoatlas.sk")
    $cert = $ssl.RemoteCertificate
    $days = ($cert.GetExpirationDateString() | Get-Date) - (Get-Date)
    
    if ($days.Days -lt 7) { throw "Certificate expires in less than 7 days!" }
    Write-Host " (Valid for $($days.Days) days)" -NoNewline -ForegroundColor Gray
    
    $ssl.Close()
    $tcp.Close()
}

Write-Host ""
Write-Host "✅ DIAGNOSTICS COMPLETE" -ForegroundColor Green
