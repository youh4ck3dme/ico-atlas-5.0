#!/bin/bash
# 🔧 Script na riešenie konfliktov v PR #6
# Pull Request: https://github.com/youh4ck3dme/DIMITRI-CHECKER/pull/6

set -e  # Zastaviť pri chybe

echo "═══════════════════════════════════════════════════════════"
echo "🔧 RIEŠENIE KONFLIKTOV PR #6"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 1. Uložiť aktuálne zmeny
echo "📋 Krok 1: Kontrola aktuálneho stavu..."
cd /Users/youh4ck3dme/Downloads/DIMITRI-CHECKER
git status

# 2. Commitnúť untracked súbory (ak ešte nie sú)
echo ""
echo "📋 Krok 2: Commitnutie nových súborov..."
if [ -n "$(git status --porcelain | grep '^??')" ]; then
    echo "   Pridávam nové súbory..."
    git add .dockerignore PROJECT_SUMMARY.md backend/Dockerfile backend/services/redis_cache.py docker-compose.yml frontend/Dockerfile
    git commit -m "feat: Add Docker setup and Redis cache service" || echo "   ⚠️  Súbory už môžu byť commitnuté"
else
    echo "   ✅ Žiadne nové súbory na commitnutie"
fi

# 3. Fetch najnovšie zmeny
echo ""
echo "📋 Krok 3: Fetch najnovších zmien z origin..."
git fetch origin

# 4. Rebase na main
echo ""
echo "📋 Krok 4: Rebase na origin/main..."
echo "   ⚠️  Toto môže spôsobiť konflikty - pripravte sa na ich riešenie"
read -p "   Pokračovať? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "   ❌ Zrušené"
    exit 1
fi

git rebase origin/main

# 5. Kontrola konfliktov
echo ""
echo "📋 Krok 5: Kontrola konfliktov..."
if [ -n "$(git status --porcelain | grep '^UU')" ]; then
    echo "   ⚠️  Nájdené konflikty!"
    echo ""
    echo "   Konfliktné súbory:"
    git status --porcelain | grep '^UU' | awk '{print "      -", $2}'
    echo ""
    echo "   📝 Postup riešenia:"
    echo "      1. Otvorte konfliktné súbory v editore"
    echo "      2. Nájdite konfliktné značky (<<<<<<< HEAD, =======, >>>>>>> origin/main)"
    echo "      3. Vyriešte konflikty (zachovať obe verzie alebo zlúčiť)"
    echo "      4. Odstráňte konfliktné značky"
    echo "      5. Spustite: git add <súbor>"
    echo "      6. Spustite: git rebase --continue"
    echo ""
    echo "   📄 Detailné návody nájdete v:"
    echo "      - PR_CONFLICT_DETAILS.md"
    echo "      - PR_CONFLICT_RESOLUTION.md"
    echo ""
    echo "   ⚠️  Po vyriešení konfliktov pokračujte:"
    echo "      git add backend/services/auth.py backend/services/stripe_service.py"
    echo "      git rebase --continue"
else
    echo "   ✅ Žiadne konflikty!"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ SCRIPT DOKONČENÝ"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📋 Ďalšie kroky:"
echo "   1. Vyriešte konflikty (ak existujú)"
echo "   2. Spustite testy: python -m pytest tests/ -v"
echo "   3. Push: git push origin changes --force-with-lease"
echo ""

