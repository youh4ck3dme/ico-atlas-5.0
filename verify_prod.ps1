[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
try {
    Write-Host "Checking https://pro.icoatlas.sk/api/search?q=Slovnaft&graph=1 ..."
    $r = Invoke-WebRequest -Uri "https://pro.icoatlas.sk/api/search?q=Slovnaft&graph=1"
    Write-Host "STATUS_CODE: $($r.StatusCode)"
    if ($r.Content -match '"nodes"') {
        Write-Host "✅ GRAPH DATA FOUND"
    }
    else {
        Write-Host "❌ NO GRAPH DATA"
    }
    Write-Host "CONTENT_PREVIEW: $($r.Content.Substring(0, [math]::Min(200, $r.Content.Length)))"
}
catch {
    Write-Host "ERROR: $_"
    try {
        Write-Host "RESPONSE: $($_.Exception.Response.StatusCode)"
    }
    catch {}
}
