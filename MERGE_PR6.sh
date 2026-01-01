#!/bin/bash
# 🔧 Script na merge PR #6 do main branch
# Pull Request: https://github.com/youh4ck3dme/DIMITRI-CHECKER/pull/6

set -e  # Zastaviť pri chybe

echo "═══════════════════════════════════════════════════════════"
echo "🔧 MERGE PR #6 DO MAIN"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Aktuálna cesta
PROJECT_DIR="/Users/youh4ck3dme/Downloads/DIMITRI-CHECKER"
cd "$PROJECT_DIR"

echo "📍 Cesta: $PROJECT_DIR"
echo ""

# 1. Prejsť na main branch
echo "📋 Krok 1: Prechádzam na main branch..."
git checkout main

# 2. Aktualizovať main z remote
echo ""
echo "📋 Krok 2: Aktualizujem main z remote..."
git pull origin main

# 3. Merge changes branch do main
echo ""
echo "📋 Krok 3: Mergujem changes branch do main..."
git merge changes --no-ff -m "Merge PR #6: Add Docker setup, Redis cache, Excel export"

# 4. Push na remote
echo ""
echo "📋 Krok 4: Pushujem zmeny na remote..."
git push origin main

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ MERGE DOKONČENÝ!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📊 PR #6 bol úspešne mergnutý do main branch!"
echo ""
echo "🔗 PR Link: https://github.com/youh4ck3dme/DIMITRI-CHECKER/pull/6"
echo ""

