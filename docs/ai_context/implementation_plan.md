# Fix Backend 500 Errors: Database Resilience & Search Logic

This plan addresses the widespread 500 Internal Server Errors in the backend caused by PostgreSQL connection failures and a specific `TypeError` in the search service.

## Proposed Changes

### Database Service
#### [MODIFY] [database.py](file:///c:/Users/engli/Desktop/v4/v4/backend/services/database.py)
- Update `init_database` to attempt connection to PostgreSQL (if configured) and gracefully fallback to SQLite if the connection fails.
- Ensure `_initialized` is set correctly and the fallback engine is usable.
- Improve error logging for database connection issues.

### Search Service
#### [MODIFY] [search_by_name.py](file:///c:/Users/engli/Desktop/v4/v4/backend/services/search_by_name.py)
- Fix `TypeError` in `func.cast` by ensuring the second argument is a valid SQLAlchemy type (using `Text` class instead of `"text"` string if applicable).
- Add better error handling around full-text search similarity queries.

### ORSR Provider
#### [MODIFY] [sk_orsr_provider.py](file:///c:/Users/engli/Desktop/v4/v4/backend/services/sk_orsr_provider.py)
- Wrap database operations in more granular try-except blocks to ensure scraping continues even if caching/saving to DB fails.

### [Hybrid Cache]

#### [MODIFY] [cache.py](file:///c:/Users/engli/Desktop/v4/v4/backend/services/cache.py)
- Replace simple L1 dictionary with `collections.OrderedDict` to implement an LRU (Least Recently Used) eviction policy.
- Limit L1 cache to a maximum number of items (e.g., 1000) to prevent memory bloating.
- Implement "TTL jitter": add a random variation to TTLs when saving to L2 (Redis) to prevent many keys expiring at once and causing a cache stampede.

#### [MODIFY] [redis_cache.py](file:///c:/Users/engli/Desktop/v4/v4/backend/services/redis_cache.py)
- Improve logging for connection failures.
- Ensure all dictionary values are reliably serialized/deserialized as JSON.

---

---

### [VPS Docker Deployment]

#### [NEW] [deploy_vps_docker.ps1](file:///c:/Users/engli/Desktop/v4/v4/deploy_vps_docker.ps1)
- Main PowerShell orchestrator for VPS deployment.
- Includes SSH connection retry logic and host key management.

#### [NEW] [install_docker.sh](file:///c:/Users/engli/Desktop/v4/v4/VPS_DEPLOY/install_docker.sh)
- Shell script to install Docker Engine and Compose on Ubuntu 24.

#### [NEW] [docker-compose.prod.yml](file:///c:/Users/engli/Desktop/v4/v4/VPS_DEPLOY/docker-compose.prod.yml)
- Production-grade service orchestration (PostgreSQL, Redis, Backend, Frontend, Nginx, Certbot).

#### [NEW] [default.conf](file:///c:/Users/engli/Desktop/v4/v4/VPS_DEPLOY/nginx/conf.d/default.conf)
- Nginx configuration for SSL termination and reverse proxying to Docker services.

## Verification Plan

### Automated Tests
- [x] Run `test_real_ico.py` to verify IČO search stability.
- [x] Run `test_hybrid_cache.py` to verify cache logic.
- [ ] Run `deploy_vps_docker.ps1` to verify full remote deployment.

### Manual Verification
- [ ] Verify `https://pro.icoatlas.sk` is accessible after deployment.
- [ ] Check `docker compose ps` on VPS to ensure all services are healthy.
- [ ] Verify SSL certificate validity in the browser.

### Graph Linking (New)
#### [NEW] [graph_service.py](file:///c:/Users/engli/Desktop/v4/v4/backend/services/graph_service.py)
- Implement `GraphService` with `upsert_node`, `upsert_edge`.
- Implement stable ID generation (`pers_sk_...`) and cross-company linking logic.

#### [MODIFY] [database.py](file:///c:/Users/engli/Desktop/v4/v4/backend/services/database.py)
- Add `GraphNode` and `GraphEdge` SQLAlchemy models.

#### [MODIFY] [main.py](file:///c:/Users/engli/Desktop/v4/v4/backend/main.py)
- Integrate `GraphService` ingestion into the company details/search flow.
- Pass structured `executive_people` and `shareholder_people` to `ingest_company_relationships`.
### 7. Execution: Automated Native Deployment
The user requested full deployment management. We utilize `VPS_DEPLOY/native/deploy_vps_native.ps1` to orchestrate the transition.
- **Automation:** 
    1.  Local: Zip `backend/` (excluding artifacts/venv).
    2.  Transfer: SCP payload to `/tmp/deploy` on VPS.
    3.  Remote: Exec `deploy_native.sh` to install Nginx, Certbot, Systemd, and Python Environment.
- **Outcome:** Full native deployment on `https://pro.icoatlas.sk` with resilient auto-renewing SSL.
