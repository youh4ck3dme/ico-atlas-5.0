# =============================================================================
# DOCKER DEPLOY SCRIPT - ILUMINATI SYSTEM
# =============================================================================

Write-Host "=== DOCKER DEPLOYMENT - ILUMINATI SYSTEM ===" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "[1/4] Kontrolujem Docker..." -ForegroundColor Yellow
try {
    docker version | Out-Null
    Write-Host "✅ Docker beží" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker nie je nainštalovaný alebo nebeží!" -ForegroundColor Red
    Write-Host "   Prosím, nainštalujte Docker Desktop z https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Stop existing containers
Write-Host "[2/4] Zastavujem existujúce kontajnery..." -ForegroundColor Yellow
docker-compose down 2>$null
Write-Host "✅ Kontajnery zastavené" -ForegroundColor Green

# Build and start containers
Write-Host "[3/4] Building a spúšťam kontajnery..." -ForegroundColor Yellow
Write-Host "   (Toto môže trvať 5-10 minút pri prvom spustení)" -ForegroundColor Gray
docker-compose up --build -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Chyba pri spustení Docker kontajnerov" -ForegroundColor Red
    exit 1
}

# Wait for services to be healthy
Write-Host "[4/4] Čakám na inicializáciu služieb..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check health
Write-Host "Kontrolujem zdravie služieb..." -ForegroundColor Gray
docker-compose ps

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "✅✅✅ DOCKER DEPLOYMENT HOTOVÝ!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Aplikácia je dostupná na:" -ForegroundColor Yellow
Write-Host "   Frontend: http://localhost" -ForegroundColor White
Write-Host "   Frontend Alt: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend API: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Užitočné príkazy:" -ForegroundColor Yellow
Write-Host "   Zobraziť logy:     docker-compose logs -f" -ForegroundColor Cyan
Write-Host "   Zastaviť:          docker-compose down" -ForegroundColor Cyan
Write-Host "   Reštartovať:       docker-compose restart" -ForegroundColor Cyan
Write-Host "   Vymazať všetko:    docker-compose down -v" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Databáza:" -ForegroundColor Yellow
Write-Host "   PostgreSQL na localhost:5432" -ForegroundColor White
Write-Host "   Redis na localhost:6379" -ForegroundColor White
Write-Host ""
