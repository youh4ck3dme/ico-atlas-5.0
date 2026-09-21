# Sprievodca nasadením a opravou ILUMINATI SYSTEM (VPS)

Tento dokument obsahuje presné inštrukcie na nasadenie, opravu a overenie aplikácie na produkčnom VPS serveri.

## 1. Príprava a Oprava Konfigurácie

Pred nasadením je kritické skontrolovať kľúčové konfiguračné súbory, aby sa predišlo chybám ako "Unexpected token <" (404) alebo problémom s CORS.

### Frontend API URL (`frontend/.env`)
Pre produkciu musí byť `VITE_API_URL` nastavená na **prázdnu hodnotu**, aby frontend používal relatívne cesty (`/api/...`) a dopyty prechádzali cez Nginx proxy.

```properties
# Súbor: frontend/.env
VITE_API_URL=
```

### Konfigurácia API Loadera (`frontend/src/config/api.js`)
Uistite sa, že kód nevnucuje `localhost` ak beží na HTTPS.

```javascript
// frontend/src/config/api.js
const getApiUrl = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  if (apiUrl) return apiUrl;
  
  // NA HTTPS (PRODUKCIA) VRÁŤ PRÁZDNUI REŤAZEC -> RELATÍVNA CESTA
  if (window.location.protocol === 'https:') {
    return '';
  }
  
  return 'http://localhost:8000';
};
```

---

## 2. Automatizované Nasadenie (Deployment)

Na nasadenie používajte aktualizovaný PowerShell skript `deploy_vps_docker.ps1`. Tento skript automaticky:
1.  Skomprimuje aktuálny kód.
2.  Nahrá ho na VPS (`80.211.196.34`).
3.  Vynúti rebuild frontendu (fix cache problémov).
4.  Reštartuje Docker kontajnery.
5.  Spustí/obnoví SSL certifikáty.

**Spustenie:**
```powershell
.\deploy_vps_docker.ps1
```

---

## 3. SSL Certifikát (Certbot)

Skript sa pokúša automaticky získať SSL certifikát. Ak diagnostika hlási chybu, môžete certifikát vynútiť manuálne priamo na serveri.

**Manuálna oprava SSL (ak automatika zlyhá):**
1.  Prihláste sa na server: `ssh root@80.211.196.34`
2.  Spustite certbot v kontajneri čistým spôsobom:

```bash
# Na VPS:
docker compose -f ~/iluminati/docker-compose.prod.yml run --rm certbot certonly --webroot --webroot-path /var/www/certbot -d pro.icoatlas.sk --force-renewal
```

3.  Reštartujte Nginx, aby načítal nový certifikát:
```bash
docker compose -f ~/iluminati/docker-compose.prod.yml restart nginx
```

---

## 4. Overenie a Testovanie

Po nasadení vykonajte tieto testy na overenie funkčnosti.

**A. Test dostupnosti:**
Otvorte `https://pro.icoatlas.sk`. Stránka by mala nabehnúť bez bezpečnostných varovaní (zámok v prehliadači).

**B. Test vyhľadávania (Kritický):**
1. Do vyhľadávania zadajte IČO: `35763469`.
2. Ak sa zobrazí graf alebo karta firmy (Slovak Telekom), všetko funguje.
3. Ak sa zobrazí **červená chyba "404"** alebo **"Unexpected token <"**:
   - Znamená to, že frontend volá zlú URL (napr. `/api/api/search`).
   - Riešenie: Skontrolujte krok 1 a spustite nasadenie znova s `--no-cache` (skript to už robí).
4. Ak sa zobrazí **"Network Error"** alebo **"Failed to fetch"**:
   - Znamená to, že frontend volá `localhost` namiesto servera.
   - Riešenie: Skontrolujte krok 1 (`api.js`) a prenasadzujte.

**C. Spustenie Diagnostiky:**
Spustite lokálny diagnostický nástroj na overenie stavu servera:
```powershell
.\diagnose_vps.ps1
```

---

## Rýchle Príkazy pre Vývojára

**Reštart servera (Docker only):**
```powershell
ssh root@80.211.196.34 "cd ~/iluminati && docker compose -f docker-compose.prod.yml restart"
```

**Zobrazenie logov (Debugging):**
```powershell
ssh root@80.211.196.34 "cd ~/iluminati && docker compose -f docker-compose.prod.yml logs -f frontend backend nginx"
```


---

## 5. Bezpečnostná Konfigurácia SSL (Secure SSL Prompt)

Ak potrebujete manuálne nastaviť alebo opraviť SSL s maximálnou bezpečnosťou (A+ rating), použite tento postup.

### Krok 1: Generovanie silných Diffie-Hellman parametrov
(Voliteľné, ale odporúčané pre vyššiu bezpečnosť)
`ash
docker compose -f ~/iluminati/docker-compose.prod.yml exec nginx openssl dhparam -out /etc/nginx/dhparam.pem 2048
``n
### Krok 2: Vynútenie Certifikátu (Prompt pre Certbot)
Spustite tento príkaz pre získanie nového certifikátu:
`ash
docker compose -f ~/iluminati/docker-compose.prod.yml run --rm certbot certonly \
  --webroot \
  --webroot-path /var/www/certbot \
  -d pro.icoatlas.sk \
  --deploy-hook 'chmod 644 /etc/letsencrypt/live/pro.icoatlas.sk/privkey.pem' \
  --force-renewal
``n
### Krok 3: Overenie Bezpečnostných Hlavičiek
Nginx konfigurácia (default.conf) už obsahuje tieto kľúčové hlavičky. Skontrolujte ich prítomnosť cez curl -I https://pro.icoatlas.sk:
- Strict-Transport-Security (HSTS)
- X-Frame-Options: SAMEORIGIN (Ochrana proti clickjackingu)
- X-Content-Type-Options: nosniff (Ochrana MIME typov)
- Referrer-Policy: strict-origin-when-cross-origin`n
### Krok 4: Automatická Obnova
Certbot kontajner v docker-compose.prod.yml automaticky kontroluje obnovu každých 12 hodín. Nie je potrebný žiadny ďalší zásah.
