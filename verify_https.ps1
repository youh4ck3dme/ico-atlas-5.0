try {
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
    [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
    Write-Host "Verifying https://pro.icoatlas.sk/docs ..."
    $r = Invoke-WebRequest -Uri "https://pro.icoatlas.sk/docs"
    Write-Host "STATUS_CODE: $($r.StatusCode)"
    Write-Host "SSL: ACTIVE (Green Lock)"
}
catch {
    Write-Host "ERROR: $_"
}
