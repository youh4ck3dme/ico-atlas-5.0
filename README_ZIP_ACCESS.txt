ILUMINATI PROJECT - NÁVOD NA PRÍSTUP

Vaše údaje o projekte:
========================

Projekt sa nachádza na: C:\Users\engli\Desktop\v4\v4

Struktúra projektu:
==================
v4/
├── backend/          # Python FastAPI server
├── frontend/         # React/Vite aplikácia
├── docs/            # Dokumentácia
├── tests/           # Testy
├── ssl/             # SSL certifikáty
├── docker-compose.yml # Docker konfigurácia
├── full_deploy.sh   # Jednotný spúšťací skript
└── README.md        # Hlavná dokumentácia

Spustenie projektu:
==================
1. Otvorte Git Bash
2. Prejdite do adresára: cd /c/Users/engli/Desktop/v4/v4
3. Spustite: ./full_deploy.sh

Alebo manuálne:
1. Backend: cd backend && python main.py
2. Frontend: cd frontend && npm run dev

Prístup k aplikácii:
===================
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Nová cenová stránka: http://localhost:5173/pricing

ZIP archív:
==========
Ak potrebujete ZIP súbor, projekt je už rozbalený na vašej ploche.
Pre vytvorenie ZIP použite:
- Windows Explorer: Kliknite pravým tlačidlom na priečinok v4 → Odoslať do → Komprimovaný priečinok
- Alebo PowerShell: Compress-Archive -Path "C:\Users\engli\Desktop\v4\v4\*" -DestinationPath "C:\Users\engli\Desktop\iluminati_project.zip"

Kontakt:
=======
Projekt je plne funkčný a pripravený na použitie!