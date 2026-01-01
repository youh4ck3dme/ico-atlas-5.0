$sourcePath = "C:\Users\engli\Desktop\v4\v4"
$destinationPath = "C:\Users\engli\Desktop\iluminati_complete_project_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').zip"

Write-Host "Creating ZIP archive of ILUMINATI project..."
Write-Host "Source: $sourcePath"
Write-Host "Destination: $destinationPath"

try {
    Compress-Archive -Path "$sourcePath\*" -DestinationPath $destinationPath -Force
    Write-Host "ZIP archive created successfully!"
    Write-Host "File location: $destinationPath"

    # Get file size
    $fileSize = (Get-Item $destinationPath).Length
    Write-Host "File size: $([math]::Round($fileSize / 1MB, 2)) MB"
} catch {
    Write-Host "Error creating ZIP: $_"
}

Read-Host "Press Enter to exit"