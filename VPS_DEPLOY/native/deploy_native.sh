#!/bin/bash
# Native Deployment Script for Ubuntu 24

# 1. Install Dependencies
apt update
apt install -y nginx ufw python3-venv python3-pip

# 2. Setup Certbot
snap install core; snap refresh core
snap install --classic certbot
ln -sf /snap/bin/certbot /usr/bin/certbot

# 3. Setup Firewall
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

# 4a. Setup Application Directory
APP_DIR="/var/www/icoatlas-pro"
mkdir -p $APP_DIR
# Code should be copied here by the caller (deploy_vps_native.ps1) before creating venv
# Assuming /tmp/deploy/backend contains the source
if [ -d "/tmp/deploy/backend" ]; then
    cp -r /tmp/deploy/backend/* $APP_DIR/
fi

# 4b. Setup Python Environment
python3 -m venv $APP_DIR/venv
source $APP_DIR/venv/bin/activate
pip install --upgrade pip
if [ -f "$APP_DIR/requirements.txt" ]; then
    pip install -r $APP_DIR/requirements.txt
fi
# Install uvicorn/gunicorn if not in requirements (though they should be)
pip install uvicorn gunicorn

# 4c. Copy Configs
# Update service file to point to correct working directory if needed
# (Assuming service file assumes /var/www/icoatlas-pro)
cp /tmp/deploy/icoatlas-pro-api.service /etc/systemd/system/
cp /tmp/deploy/pro.icoatlas.sk.conf /etc/nginx/sites-available/pro.icoatlas.sk
ln -sf /etc/nginx/sites-available/pro.icoatlas.sk /etc/nginx/sites-enabled/

# 4d. Permissions
# Ensure www-data can read/write logs if any, and execute
chown -R www-data:www-data $APP_DIR
chmod -R 755 $APP_DIR

# 5. Reload Services
systemctl daemon-reload
systemctl enable icoatlas-pro-api
systemctl start icoatlas-pro-api
systemctl restart icoatlas-pro-api 

nginx -t && systemctl reload nginx

# 6. SSL
certbot --nginx -d pro.icoatlas.sk --non-interactive --agree-tos --email admin@icoatlas.sk

echo "Deployment configuration updated. Verify app is running on port 8000."
