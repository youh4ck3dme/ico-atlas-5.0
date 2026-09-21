try {
    Write-Host "Checking http://pro.icoatlas.sk/api/search?q=Slovnaft&graph=1 ..."
    $r = Invoke-WebRequest -Uri "http://pro.icoatlas.sk/api/search?q=Slovnaft&graph=1"
    Write-Host "STATUS: $($r.StatusCode)"
    
    if ($r.Content -match '"nodes"') {
        Write-Host "✅ GRAPH DATA FOUND"
    }
    else {
        Write-Host "❌ NO GRAPH DATA"
    }
    
    $len = [math]::Min(300, $r.Content.Length)
    Write-Host "CONTENT: $($r.Content.Substring(0, $len))"
}
catch {
    Write-Host "ERROR: $_"
}
