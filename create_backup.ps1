$Source = "c:\Users\engli\Desktop\v4\v4"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmm"
$DestZip = "c:\Users\engli\Desktop\icoatlas_v5_full_$Timestamp.zip"
$Staging = "$env:TEMP\icoatlas_staging_$Timestamp"

Write-Host "1. Creating staging area at $Staging..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path $Staging -Force | Out-Null

Write-Host "2. Copying source files..." -ForegroundColor Cyan
Write-Host "   (Excluding: node_modules, venv, .git, dist, __pycache__)" -ForegroundColor Gray
# /E = recursive, /XD = exclude directories, /XF = exclude files, /NFL /NDL = no file/dir logging (quieter)
robocopy $Source $Staging /E /XD node_modules venv .venv __pycache__ .git .pytest_cache dist .idea .vscode /XF *.log *.zip *.tmp /NFL /NDL

# Robocopy exit codes 0-7 are success
if ($LASTEXITCODE -gt 7) {
    Write-Host "Error during copy!" -ForegroundColor Red
    Exit
}

Write-Host "3. Compressing to $DestZip..." -ForegroundColor Cyan
Compress-Archive -Path "$Staging\*" -DestinationPath $DestZip -Force

Write-Host "4. Cleaning up..." -ForegroundColor Cyan
Remove-Item -Path $Staging -Recurse -Force

Write-Host "✅ BACKUP SUCCESSFUL!" -ForegroundColor Green
Write-Host "File saved to: $DestZip" -ForegroundColor Green
