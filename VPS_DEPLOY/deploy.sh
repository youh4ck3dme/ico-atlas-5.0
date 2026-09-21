#!/bin/bash

# ==============================================================================
# ILUMINATI SYSTEM - ONE-CLICK DEPLOY SCRIPT (Ubuntu 24.04 LTS)
# Autor: Antigravity AI
# Verzia: 1.0.0
# ==============================================================================

# Nastavenie premennych
DOMAIN="pro.icoatlas.sk"
REPO_URL="https://github.com/youh4ck3dme/ico-atlas-5.0.git"
APP_DIR="/var/www/ico-atlas"
DB_NAME="iluminati_db"
DB_USER="iluminati_user"
DB_PASS="IluminatiSecurePass2026" # Zmente v produkcii!
EMAIL="info@icoatlas.sk" # Pre Let's Encrypt

# Farby
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Error handling
set -e

echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}   STARTUJEM DEPLOYMENT NA: $DOMAIN                   ${NC}"
echo -e "${BLUE}======================================================${NC}"

# 1. Update Systemu
echo -e "\n${GREEN}[1/8] Aktualizujem systemove baliky...${NC}"
apt-get update && apt-get upgrade -y
apt-get install -y git python3 python3-pip python3-venv nginx postgresql postgresql-contrib redis-server certbot python3-certbot-nginx curl acl build-essential libpq-dev

# 2. Instalacia Node.js (v20 LTS)
echo -e "\n${GREEN}[2/8] Instalujem Node.js v20...${NC}"
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt-get install -y nodejs
else
    echo "Node.js uz je nainstalovany."
fi

# 3. Nastavenie Databazy (PostgreSQL)
echo -e "\n${GREEN}[3/8] Konfigurujem PostgreSQL...${NC}"
# Check if user exists, if not create
sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1 || \
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"

# Check if db exists, if not create
sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1 || \
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"

echo "Databaza pripravena."

# 4. Stiahnutie a Priprava Aplikacie
echo -e "\n${GREEN}[4/8] Stahujem kod z GitHub...${NC}"
if [ -d "$APP_DIR" ]; then
    echo "Adresar existuje, aktualizujem..."
    cd $APP_DIR
    git pull
else
    git clone $REPO_URL $APP_DIR
    cd $APP_DIR
fi

# Nastavenie prav
chown -R www-data:www-data $APP_DIR
chmod -R 755 $APP_DIR
setfacl -R -m u:root:rwx $APP_DIR # Allow root to write

# 5. Backend Setup
echo -e "\n${GREEN}[5/8] Instalujem Backend...${NC}"
cd $APP_DIR/backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file for backend if not exists
if [ ! -f ".env" ]; then
    echo "Vytvaram .env subor..."
    cat > .env << EOL
DATABASE_URL=postgresql://$DB_USER:$DB_PASS@localhost/$DB_NAME
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=https://$DOMAIN
BACKEND_URL=https://$DOMAIN/api
REDIS_URL=redis://localhost:6379/0
EOL
fi

# Migracie DB (ak existuju)
# alembic upgrade head || echo "Skipping alembic migrations for now"

deactivate

# 6. Frontend Setup
echo -e "\n${GREEN}[6/8] Budujem Frontend...${NC}"
cd $APP_DIR/frontend
npm install
# Vytvorit .env pre frontend build
echo "VITE_API_URL=https://$DOMAIN/api" > .env
npm run build

# Copy build to where nginx expects it or keep in dist
# We will point Nginx to $APP_DIR/frontend/dist

# 7. Systemd Service pre Backend
echo -e "\n${GREEN}[7/8] Vytvaram Systemd sluzbu...${NC}"
cat > /etc/systemd/system/ico-atlas.service << EOL
[Unit]
Description=Gunicorn instance directly serving FastAPI
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=$APP_DIR/backend
Environment="PATH=$APP_DIR/backend/venv/bin"
ExecStart=$APP_DIR/backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 4

[Install]
WantedBy=multi-user.target
EOL

systemctl daemon-reload
systemctl enable ico-atlas
systemctl restart ico-atlas

# 8. Nginx Konfiguracia
echo -e "\n${GREEN}[8/8] Konfigurujem Nginx a SSL...${NC}"
cat > /etc/nginx/sites-available/$DOMAIN << EOL
server {
    server_name $DOMAIN;

    location / {
        root $APP_DIR/frontend/dist;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        
        # Rewrites /api/v1/... to /api/v1/... (fastapi expects /api prefix usually if mounted there, or stripped)
        # Check main.py if it has root_path set or handles /api
        # Assuming main.py serves on /api or we strip it. 
        # Usually uvicorn serving FastAPI at / handles paths as defined. 
        # If your FastAPI routes start with /api, then direct proxy is fine.
    }
}
EOL

# Enable site
ln -sf /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

# SSL Certificate
echo -e "\n${BLUE}Ziskavam SSL certifikat (Let's Encrypt)...${NC}"
# Non-interactive mode
certbot --nginx --non-interactive --agree-tos -m $EMAIL -d $DOMAIN --redirect || echo "⚠️ Certbot zlyhal alebo uz existuje. Skontrolujte rucne."

echo -e "\n${GREEN}======================================================${NC}"
echo -e "${GREEN}   DEPLOYMENT UKONCENY USPESNE! 🚀                    ${NC}"
echo -e "${GREEN}   Web bezi na: https://$DOMAIN                       ${NC}"
echo -e "${GREEN}======================================================${NC}"
