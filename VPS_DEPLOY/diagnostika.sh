#!/bin/bash

# Farby pre vystup
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN}   DIAGNOSTIKA VPS - ILUMINATI SYSTEM (Ubuntu 24)   ${NC}"
echo -e "${GREEN}====================================================${NC}"

# 1. OS Verzia
echo -e "\n${GREEN}[1] VERZIA OPERACNEHO SYSTEMU:${NC}"
lsb_release -d
uname -r

# 2. Hardver
echo -e "\n${GREEN}[2] DOSTUPNY HARDVER (CPU/RAM/DISK):${NC}"
lscpu | grep "Model name"
free -h
df -h /

# 3. Siet a IP
echo -e "\n${GREEN}[3] SIETOVE ROZHRANIA:${NC}"
ip addr show | grep inet | grep -v 127.0.0.1

# 4. Otvorene porty
echo -e "\n${GREEN}[4] OBSADENE PORTY (LISTEN):${NC}"
ss -tulpn | grep LISTEN

# 5. Firewall Status
echo -e "\n${GREEN}[5] STAV FIREWALLU (UFW):${NC}"
ufw status verbose

# 6. Kontrola existujuceho softveru
echo -e "\n${GREEN}[6] KONTROLA ZAVISLOSTI:${NC}"

check_cmd() {
    if command -v $1 &> /dev/null; then
        echo -e "✅ $1: $( $1 --version 2>/dev/null | head -n 1 || echo 'Nainstalovane' )"
    else
        echo -e "${RED}❌ $1: Nenainstalovane${NC}"
    fi
}

check_cmd python3
check_cmd pip3
check_cmd node
check_cmd npm
check_cmd nginx
check_cmd psql
check_cmd docker
check_cmd git

# 7. Prava zapisu
echo -e "\n${GREEN}[7] KONTROLA PRAV:${NC}"
CURRENT_USER=$(whoami)
echo "Aktualny pouzivatel: $CURRENT_USER"
if [ "$CURRENT_USER" = "root" ]; then
    echo "✅ Spustene pod rootom (OK pre deploy)"
else
    echo -e "${RED}⚠️  UPOZORNENIE: Skript nie je spusteny pod rootom!${NC}"
fi

echo -e "\n${GREEN}====================================================${NC}"
echo -e "${GREEN}   DIAGNOSTIKA DOKONCENA                           ${NC}"
echo -e "${GREEN}====================================================${NC}"
