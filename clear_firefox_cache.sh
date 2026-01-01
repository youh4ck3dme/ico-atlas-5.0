#!/bin/bash

# Skript na vyčistenie cache v Firefox Developer Edition
# Použitie: ./clear_firefox_cache.sh

echo "🧹 Čistím cache v Firefox Developer Edition..."
echo ""

# Cesta k Firefox Developer Edition profilu
FIREFOX_PROFILE_DIR="$HOME/Library/Application Support/Firefox/Profiles"

if [ -d "$FIREFOX_PROFILE_DIR" ]; then
    # Nájsť Developer Edition profil
    DEV_PROFILE=$(find "$FIREFOX_PROFILE_DIR" -name "*dev-edition*" -type d | head -1)
    
    if [ -n "$DEV_PROFILE" ]; then
        echo "📁 Nájdený profil: $DEV_PROFILE"
        
        # Vymazať cache
        if [ -d "$DEV_PROFILE/cache2" ]; then
            rm -rf "$DEV_PROFILE/cache2"/*
            echo "   ✅ Cache vymazaný"
        fi
        
        # Vymazať offline cache
        if [ -d "$DEV_PROFILE/OfflineCache" ]; then
            rm -rf "$DEV_PROFILE/OfflineCache"/*
            echo "   ✅ Offline cache vymazaný"
        fi
        
        # Vymazať storage
        if [ -d "$DEV_PROFILE/storage" ]; then
            rm -rf "$DEV_PROFILE/storage"/*
            echo "   ✅ Storage vymazaný"
        fi
        
        echo ""
        echo "✅ Cache v Firefox Developer Edition vyčistený!"
        echo ""
        echo "💡 Teraz:"
        echo "   1. Zatvor Firefox Developer Edition (ak je otvorený)"
        echo "   2. Spusti Firefox Developer Edition znova"
        echo "   3. Otvor https://localhost:8009/"
    else
        echo "⚠️ Developer Edition profil nebol nájdený"
        echo "💡 Môžeš manuálne vymazať cache cez Firefox:"
        echo "   Ctrl+Shift+Delete (Windows/Linux) alebo Cmd+Shift+Delete (Mac)"
    fi
else
    echo "⚠️ Firefox profilový adresár nebol nájdený"
    echo "💡 Môžeš manuálne vymazať cache cez Firefox:"
    echo "   Ctrl+Shift+Delete (Windows/Linux) alebo Cmd+Shift+Delete (Mac)"
fi

echo ""
echo "📋 Manuálne inštrukcie pre Firefox Developer Edition:"
echo "   1. Otvor Firefox Developer Edition"
echo "   2. Stlač Cmd+Shift+Delete (Mac) alebo Ctrl+Shift+Delete (Windows/Linux)"
echo "   3. Vyber 'Cache' a 'Cookies'"
echo "   4. Klikni 'Clear Now' / 'Vymazať teraz'"
echo "   5. Obnov stránku (Cmd+Shift+R alebo Ctrl+F5)"

