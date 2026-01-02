$VPS_IP = "80.211.196.34"
$VPS_USER = "root"
$KEY_PATH = "$env:USERPROFILE\.ssh\id_rsa"
$ID_RSA = "$env:USERPROFILE\.ssh\id_rsa"

Write-Host "📦 Configuring FRONTEND Deployment..." -ForegroundColor Cyan

# 1. Zip Dist
$DistPath = "frontend\dist"
$ZipPath = "$env:TEMP\frontend.zip"
if (Test-Path $ZipPath) { Remove-Item $ZipPath }
Compress-Archive -Path "$DistPath\*" -DestinationPath $ZipPath -Force

# 2. Upload
Write-Host "Uploading frontend..."
scp -i $ID_RSA $ZipPath "$($VPS_USER)@$($VPS_IP):/tmp/deploy/frontend.zip"

# 3. Create Nginx Config
$NginxConfig = @"
server {
    listen 80;
    server_name pro.icoatlas.sk;
    return 301 https://`$host`$request_uri;
}

server {
    listen 443 ssl;
    server_name pro.icoatlas.sk;

    ssl_certificate /etc/letsencrypt/live/pro.icoatlas.sk/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/pro.icoatlas.sk/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # FRONTEND (Static)
    root /var/www/icoatlas-pro/frontend/dist;
    index index.html;

    location / {
        try_files `$uri `$uri/ /index.html;
    }

    # BACKEND (API Proxy)
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host `$host;
        proxy_set_header X-Real-IP `$remote_addr;
        proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto `$scheme;
    }

    location /docs {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host `$host;
    }

    location /openapi.json {
        proxy_pass http://127.0.0.1:8000;
    }
}
"@
$LocalConfigPath = "$env:TEMP\pro.icoatlas.sk.conf"
Set-Content -Path $LocalConfigPath -Value $NginxConfig
scp -i $ID_RSA $LocalConfigPath "$($VPS_USER)@$($VPS_IP):/etc/nginx/sites-available/pro.icoatlas.sk"

# 4. Remote commands (Unzip + Restart)
$Cmd = "mkdir -p /var/www/icoatlas-pro/frontend/dist; unzip -o /tmp/deploy/frontend.zip -d /var/www/icoatlas-pro/frontend/dist/; ln -sf /etc/nginx/sites-available/pro.icoatlas.sk /etc/nginx/sites-enabled/; nginx -t && systemctl restart nginx"
ssh -i $ID_RSA $VPS_USER@$VPS_IP $Cmd

Write-Host "Frontend Deployed & Nginx Updated!" -ForegroundColor Green
