# PostgreSQL Database Setup

## Prehľad

ILUMINATI SYSTEM používa PostgreSQL databázu pre:
- **Históriu vyhľadávaní** - tracking všetkých search queries
- **Company cache** - dlhodobé uloženie firiem (24h+ TTL)
- **Analytics** - event tracking pre business intelligence

## Inštalácia

### 1. Inštalácia PostgreSQL

**macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Windows:**
Stiahnuť z: https://www.postgresql.org/download/windows/

### 2. Vytvorenie databázy

```bash
# Prihlásiť sa do PostgreSQL
psql -U postgres

# Vytvoriť databázu
CREATE DATABASE iluminati_db;

# Vytvoriť používateľa (voliteľné)
CREATE USER iluminati_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE iluminati_db TO iluminati_user;

# Ukončiť
\q
```

### 3. Automatický setup

```bash
cd backend
./setup_database.sh
```

Alebo manuálne:

```bash
cd backend
source venv/bin/activate
pip install psycopg2-binary sqlalchemy alembic
python3 -c "from services.database import init_database; init_database()"
```

## Konfigurácia

### Environment Variables

```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/iluminati_db"
```

Alebo v `.env` súbore:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/iluminati_db
```

### Default nastavenia

- **Host:** localhost
- **Port:** 5432
- **Database:** iluminati_db
- **User:** postgres
- **Password:** postgres

## Database Schema

### search_history
- `id` - Primary key
- `query` - Search query
- `country` - Detekovaná krajina (SK, CZ, PL, HU)
- `result_count` - Počet výsledkov
- `risk_score` - Max risk score
- `search_timestamp` - Čas vyhľadávania
- `user_ip` - IP adresa používateľa
- `response_data` - JSON s výsledkami

### company_cache
- `id` - Primary key
- `identifier` - IČO/KRS/Adószám (unique)
- `country` - Krajina
- `company_name` - Názov firmy
- `data` - JSON s kompletnými dátami
- `risk_score` - Risk score
- `created_at` - Čas vytvorenia
- `updated_at` - Čas aktualizácie
- `expires_at` - Čas expirácie

### analytics
- `id` - Primary key
- `event_type` - Typ eventu (search, export, error)
- `event_data` - JSON s dátami eventu
- `timestamp` - Čas eventu
- `user_ip` - IP adresa
- `user_agent` - User agent string

## API Endpoints

### GET /api/database/stats
Vráti štatistiky databázy:
```json
{
  "status": "ok",
  "available": true,
  "search_history_count": 1234,
  "company_cache_count": 567,
  "analytics_count": 8901
}
```

### GET /api/search/history?limit=100&country=SK
Vráti históriu vyhľadávaní:
```json
[
  {
    "id": 1,
    "query": "88888888",
    "country": "SK",
    "result_count": 9,
    "risk_score": 7.0,
    "search_timestamp": "2024-12-19T05:00:00",
    "user_ip": "127.0.0.1"
  }
]
```

## Použitie v kóde

```python
from services.database import (
    save_search_history,
    get_search_history,
    save_company_cache,
    get_company_cache,
    save_analytics
)

# Uložiť vyhľadávanie
save_search_history(
    query="88888888",
    country="SK",
    result_count=9,
    risk_score=7.0
)

# Získať históriu
history = get_search_history(limit=50, country="SK")

# Uložiť firmu do cache
save_company_cache(
    identifier="88888888",
    country="SK",
    company_name="Test Firma s.r.o.",
    data={"nodes": [...], "edges": [...]},
    risk_score=7.0
)

# Analytics
save_analytics(
    event_type="export",
    event_data={"format": "pdf", "query": "88888888"}
)
```

## Maintenance

### Cleanup expirovaného cache

```python
from services.database import cleanup_expired_cache

# Automaticky sa volá pri štarte aplikácie
# Alebo manuálne:
deleted = cleanup_expired_cache()
print(f"Vymazaných {deleted} expirovaných záznamov")
```

### Backup

```bash
pg_dump -U postgres iluminati_db > backup_$(date +%Y%m%d).sql
```

### Restore

```bash
psql -U postgres iluminati_db < backup_20241219.sql
```

## Troubleshooting

### Databáza nie je dostupná

Aplikácia automaticky fallbackuje na in-memory cache ak PostgreSQL nie je dostupný.

### Connection refused

1. Skontrolovať, či PostgreSQL beží:
   ```bash
   brew services list  # macOS
   sudo systemctl status postgresql  # Linux
   ```

2. Skontrolovať port:
   ```bash
   lsof -i :5432
   ```

### Permission denied

```bash
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD 'new_password';
```

## Production

Pre produkciu odporúčam:
- Použiť managed PostgreSQL (AWS RDS, Google Cloud SQL, Azure Database)
- Nastaviť connection pooling
- Pravidelné backupy
- Monitoring a alerting
- Read replicas pre analytics queries

---

*Posledná aktualizácia: December 2024*

