#!/bin/bash
# =============================================================================
# DOCKER INSTALLATION SCRIPT FOR UBUNTU 24
# ILUMINATI SYSTEM - Automatic Setup
# =============================================================================

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN} ILUMINATI SYSTEM - Docker Installation${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""

# 1. Update system
echo -e "${YELLOW}[1/6] Aktualizujem systém...${NC}"
apt-get update
apt-get upgrade -y

# 2. Install required packages
echo -e "${YELLOW}[2/6] Inštalujem potrebné balíčky...${NC}"
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    ufw

# 3. Add Docker GPG key and repository
echo -e "${YELLOW}[3/6] Pridávam Docker repozitár...${NC}"
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update

# 4. Install Docker
echo -e "${YELLOW}[4/6] Inštalujem Docker Engine...${NC}"
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 5. Start and enable Docker
echo -e "${YELLOW}[5/6] Spúšťam Docker službu...${NC}"
systemctl start docker
systemctl enable docker

# 6. Configure firewall
echo -e "${YELLOW}[6/6] Konfigurujem firewall...${NC}"
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw --force enable

# Verify installation
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN} Docker inštalácia dokončená!${NC}"
echo -e "${GREEN}============================================${NC}"
docker --version
docker compose version
echo ""
echo -e "${GREEN}✅ Systém je pripravený na deployment!${NC}"
