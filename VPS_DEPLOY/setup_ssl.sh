#!/bin/bash
# =============================================================================
# SSL CERTIFICATE SETUP - Let's Encrypt
# ILUMINATI SYSTEM
# =============================================================================

set -e

DOMAIN="pro.icoatlas.sk"
EMAIL="info@icoatlas.sk"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN} ILUMINATI SYSTEM - SSL Setup${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""

APP_DIR="/root/iluminati"
cd $APP_DIR

# Create certbot directories
mkdir -p certbot/conf
mkdir -p certbot/www

# Create temporary self-signed certificate for initial nginx startup
echo -e "${YELLOW}[1/4] Vytváram dočasný certifikát...${NC}"
mkdir -p certbot/conf/live/$DOMAIN
openssl req -x509 -nodes -newkey rsa:4096 \
    -keyout certbot/conf/live/$DOMAIN/privkey.pem \
    -out certbot/conf/live/$DOMAIN/fullchain.pem \
    -subj "/CN=$DOMAIN" \
    -days 1

# Start nginx with temporary certificate
echo -e "${YELLOW}[2/4] Spúšťam nginx s dočasným certifikátom...${NC}"
docker compose -f docker-compose.prod.yml up -d nginx

# Wait for nginx
sleep 5

# Get real certificate from Let's Encrypt
echo -e "${YELLOW}[3/4] Získavam SSL certifikát od Let's Encrypt...${NC}"
docker compose -f docker-compose.prod.yml run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN

# Reload nginx with real certificate
echo -e "${YELLOW}[4/4] Reloadujem nginx s reálnym certifikátom...${NC}"
docker compose -f docker-compose.prod.yml exec nginx nginx -s reload

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN} SSL certifikát úspešne nainštalovaný!${NC}"
echo -e "${GREEN} Doména: https://$DOMAIN${NC}"
echo -e "${GREEN}============================================${NC}"
