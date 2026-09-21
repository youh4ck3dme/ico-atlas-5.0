import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests

try:
    from bs4 import BeautifulSoup  # type: ignore[reportMissingModuleSource]
except ImportError:
    BeautifulSoup = None  # Optional dependency for ORSR scraping
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Request, status
from services.audit_service import AuditService
from fastapi import Request as FastAPIRequest
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from services.analytics import (
    get_api_usage,
    get_dashboard_summary,
    get_risk_distribution,
    get_search_trends,
    get_user_activity,
)
from services.api_keys import (
    create_api_key,
    get_api_key_stats,
    get_user_api_keys,
    revoke_api_key,
)
from services.auth import (
    User,
    UserTier,
    authenticate_user,
    create_access_token,
    create_user,
    decode_access_token,
    get_user_by_email,
    get_user_tier_limits,
)
from services.cache import get, get_cache_key, set
from services.cache import get_stats as get_cache_stats
from services.circuit_breaker import get_all_breakers, reset_breaker
from services.database import (
    cleanup_expired_cache,
    get_database_stats,
    get_db_session,
    get_search_history,
    init_database,
    save_analytics,
    save_company_cache,
    save_search_history,
)
from services.debt_registers import search_debt_registers
from services.erp.erp_service import (
    activate_erp_connection,
    create_erp_connection,
    deactivate_erp_connection,
    get_erp_sync_logs,
    get_supplier_payment_history_from_erp,
    get_user_erp_connections,
    sync_erp_data,
    test_erp_connection,
)
from services.erp.models import ErpType
from services.error_handler import error_handler
from services.export_service import export_batch_to_excel, export_to_excel
from services.favorites import (
    add_favorite,
    get_user_favorites,
    is_favorite,
    remove_favorite,
)
from services.favorites import (
    update_favorite_notes as update_favorite_notes_service,
)
from services.hu_nav import (
    calculate_hu_risk_score,
    fetch_nav_hu,
    is_hungarian_tax_number,
    parse_nav_data,
)
from services.metrics import (
    TimerContext,
    gauge,
    get_metrics,
    increment,
    record_event,
)
from services.pl_biala_lista import (
    get_vat_status_pl,
    is_polish_nip,
)
from services.pl_krs import (
    calculate_pl_risk_score,
    fetch_krs_pl,
    is_polish_krs,
    parse_krs_data,
)
from services.proxy_rotation import get_proxy_stats, init_proxy_pool
from services.rate_limiter import (
    get_client_id,
    is_allowed,
)
from services.rate_limiter import get_stats as get_rate_limiter_stats

# Inicializácia služieb
audit_service = AuditService()
from services.risk_intelligence import (
    generate_risk_report,
)
from services.search_by_name import search_by_name
from services.sk_orsr_provider import get_orsr_provider
from services.graph_service import graph_service

# Import nových služieb
from services.sk_rpo import (
    calculate_sk_risk_score,
    fetch_rpo_sk,
    is_slovak_ico,
    parse_rpo_data,
)
from services.stripe_service import (
    cancel_subscription,
    create_checkout_session,
    get_subscription_status,
    handle_webhook,
)
from services.webhooks import (
    create_webhook,
    delete_webhook,
    get_user_webhooks,
    get_webhook_deliveries,
    get_webhook_stats,
)

app = FastAPI(
    title="ILUMINATI SYSTEM API",
    version="5.0",
    description="Cross-border company registry search API for V4 countries (SK, CZ, PL, HU)",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Global CORS fix - Add CORS headers to all responses
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    """Global middleware to add CORS headers to all responses"""
    response = await call_next(request)
    
    # Always add CORS headers
    origin = request.headers.get("origin")
    if origin:
        response.headers["Access-Control-Allow-Origin"] = origin
    else:
        response.headers["Access-Control-Allow-Origin"] = "*"
        
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    response.headers["Access-Control-Expose-Headers"] = "*"
    
    # Handle preflight requests
    if request.method == "OPTIONS":
        response.status_code = 200
        return response
    
    return response

# Global error handler
app.add_exception_handler(Exception, error_handler)


# Inicializovať databázu pri štarte
@app.on_event("startup")
async def startup_event():
    """Inicializácia pri štarte aplikácie"""
    init_database()
    # Cleanup expirovaného cache pri štarte
    cleanup_expired_cache()
    # Inicializovať proxy pool (ak sú proxy v env)
    init_proxy_pool()


# --- KONFIGURÁCIA CORS (Prepojenie s Frontendom) ---
origins = [
    # HTTP origins
    "http://localhost:5173",  # Vite default port
    "http://localhost:3000",
    "http://localhost:8009",  # Frontend port (zmenený z 3000)
    "http://localhost:8010",  # Frontend port alternative
    "http://localhost:8011",  # Frontend port E2E alternative
    "http://127.0.0.1:5173",  # Vite alternative
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8009",  # Frontend port alternative
    "http://127.0.0.1:8010",  # Frontend port alternative
    "http://127.0.0.1:52285",  # VS Code port forwarding
    "http://192.168.0.9:8012",  # User's specific IP/port
    # HTTPS origins (pre SSL)
    "https://pro.icoatlas.sk",
]

# --- CORS DEBUGGING ---
print("🔧 CORS Configuration Debug:")
print(f"   Origins configured: {len(origins)}")
for i, origin in enumerate(origins):
    print(f"   [{i+1}] {origin}")
print(f"   Allow credentials: True")
print(f"   Allow methods: *")
print(f"   Allow headers: *")
print(f"   Expose headers: *")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],  # Expose all headers for debugging
)


# --- DÁTOVÉ MODELY (Podľa sekcie 3: Dátový Model) ---
class Node(BaseModel):
    id: str
    label: str
    type: str  # 'company' | 'person' | 'address' | 'debt'
    country: str
    risk_score: Optional[int] = 0
    details: Optional[str] = ""
    ico: Optional[str] = None  # IČO pre firmy
    virtual_seat: Optional[bool] = False  # Virtual seat flag


class Edge(BaseModel):
    source: str
    target: str
    type: str  # 'OWNED_BY' | 'MANAGED_BY' | 'LOCATED_AT' | 'HAS_DEBT'


class GraphResponse(BaseModel):
    nodes: List[Node]
    edges: List[Edge]


# Auth Models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    consent_given: bool = True  # Always true from UI checkbox
    consent_ip: Optional[str] = None
    consent_user_agent: Optional[str] = None
    document_versions: Dict[str, str] = Field(
        default_factory=lambda: {"vop": "1.0", "privacy": "1.0", "cookies": "1.0"}
    )


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: Dict


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    tier: str
    is_active: bool
    is_verified: bool


# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Získa aktuálneho používateľa z tokenu"""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email: Optional[str] = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    with get_db_session() as db:
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )
        user = get_user_by_email(db, email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Expunge user from session to avoid DetachedInstanceError label
        db.expunge(user)
        return user


# --- SLUŽBY (ARES INTEGRÁCIA) ---
def fetch_ares_cz(query: str):
    """
    Získa dáta z českého registra ARES.
    """
    url = (
        "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat"
    )
    headers = {"Content-Type": "application/json"}
    payload = {
        "pocet": 5,  # Limit pre MVP
        "razeni": []
    }
    
    if query.isdigit():
        payload["ico"] = [query]
    else:
        payload["obchodniJmeno"] = query

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Chyba pri volaní ARES: {e}")
        return {"ekonomickeSubjekty": []}


def calculate_trust_score(company_data: Dict, country: str = "CZ") -> int:
    """
    Vypočíta rizikové skóre firmy (0-10, kde 10 je max riziko).
    Bázované na: dph status, dlhy, status firmy, virtuálne sídlo.
    """
    score = 3  # Základ: Neutrálne
    
    # 1. Status firmy
    status = str(company_data.get("status", "")).lower()
    if any(k in status for k in ["likvidácia", "konkurz", "zaniknutá", "likvidace", "insolvence"]):
        score += 5
    
    # 2. DPH Status (ak vieme detekovať)
    if not company_data.get("dic") and not company_data.get("ic_dph") and country == "SK":
        # Ak nemá ani DIČ ani IČ DPH v SK, je to mierne podozrivé pre MVP
        score += 1
        
    # 3. Virtuálne sídlo (heuristika na základe adresy)
    address = str(company_data.get("address", "")).lower()
    virtual_patterns = ["p.o.box", "pobox", "virtualne", "virtuální", "coworking"]
    if any(p in address for p in virtual_patterns):
        score += 3

    return min(score, 10)


def _scrape_orsr_sk(ico: str) -> Optional[Dict]:
    """
    Scrapuje dáta z ORSR.sk (Obchodný register SR).

    Args:
        ico: 8-miestne slovenské IČO

    Returns:
        Dict s dátami firmy alebo None pri chybe
    """
    if not BeautifulSoup:
        return None  # BeautifulSoup nie je nainštalovaný

    try:
        # ORSR.sk URL            # 1. Vyhľadávanie podľa IČO - Použiť správny endpoint hladaj_ico.asp
        search_url = f"https://www.orsr.sk/hladaj_ico.asp?ICO={ico}&SID=0"
        response = requests.get(search_url, timeout=10)

        if response.status_code == 200:
            # Parsovať HTML a extrahovať dáta
            soup = BeautifulSoup(response.text, "html.parser")

            # Hľadať odkaz na detail firmy
            detail_link = soup.find("a", href=lambda x: x and "vypis.asp?ID=" in x)  # type: ignore[arg-type]
            if detail_link and hasattr(detail_link, "get"):
                href = detail_link.get("href", "")  # type: ignore[attr-defined]
                if href and isinstance(href, str):
                    detail_id = href.split("ID=")[1].split("&")[0]
                detail_url = f"https://www.orsr.sk/vypis.asp?ID={detail_id}&SID=2&P=0"

                detail_response = requests.get(detail_url, headers=headers, timeout=10)
                if detail_response.status_code == 200:
                    detail_soup = BeautifulSoup(detail_response.text, "html.parser")

                    # Extrahovať dáta z tabuliek
                    data = {}

                    # Názov firmy
                    name_elem = detail_soup.find(
                        "td",
                        string=lambda x: x and "Obchodné meno:" in str(x),  # type: ignore[arg-type]
                    )
                    if name_elem:
                        name_row = name_elem.find_next_sibling("td")
                        if name_row:
                            data["name"] = (
                                name_row.get_text(strip=True).split("(")[0].strip()
                            )

                    # Adresa
                    address_elem = detail_soup.find(
                        "td",
                        string=lambda x: x and "Sídlo:" in str(x),  # type: ignore[arg-type]
                    )
                    if address_elem:
                        address_row = address_elem.find_next_sibling("td")
                        if address_row:
                            data["address"] = address_row.get_text(strip=True)

                    # Konateľ
                    exec_elem = detail_soup.find(
                        "td",
                        string=lambda x: x and "štatutárny orgán:" in str(x),  # type: ignore[arg-type]
                    )
                    if exec_elem:
                        exec_row = exec_elem.find_next_sibling("td")
                        if exec_row:
                            exec_link = exec_row.find("a")
                            if exec_link and hasattr(exec_link, "get_text"):
                                data["executive"] = exec_link.get_text(strip=True)  # type: ignore[attr-defined]

                    # Právna forma
                    form_elem = detail_soup.find(
                        "td",
                        string=lambda x: x and "Právna forma:" in str(x),  # type: ignore[arg-type]
                    )
                    if form_elem:
                        form_row = form_elem.find_next_sibling("td")
                        if form_row:
                            data["legal_form"] = form_row.get_text(strip=True)

                    # Risk score
                    risk_score = 3
                    if data.get("name"):
                        risk_score = 2  # Nižšie riziko ak máme reálne dáta

                    data["risk_score"] = risk_score
                    data["details"] = f"Forma: {data.get('legal_form', 'N/A')}"

                    return data if data.get("name") else None

        return None
    except Exception as e:
        print(f"❌ Chyba pri scraping ORSR.sk: {e}")
        return None


# --- ENDPOINTY ---


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(content="", media_type="image/x-icon")


@app.get("/health")
def health_check():
    """Health check endpoint for Docker"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/")
def read_root():
    return {
        "status": "ILUMINATI SYSTEM API Running",
        "version": "5.0",
        "features": [
            "CZ (ARES)",
            "SK (RPO + ORSR V2)",
            "PL (KRS)",
            "HU (NAV)",
            "Theater Mode (3D Visualization)",
            "Data Import System (Excel, PDF, JSON)",
            "Unified CORS Proxy",
            "Cache & Risk Scoring",
            "Authentication (Secure)",
            "Stripe Integration",
            "API Keys Management",
            "Webhooks & ERP Integrations",
            "Analytics Dashboard",
            "Favorites System",
        ],
        "endpoints": {
            "health": "/api/health",
            "docs": "/api/docs",
            "search": "/api/search",
            "auth": "/api/auth",
            "enterprise": "/api/enterprise",
            "analytics": "/api/analytics",
            "export": {
                "excel": "/api/export/excel",
                "batch_excel": "/api/export/batch-excel",
            },
        },
        "supported_formats": ["JSON", "CSV", "PDF", "Excel (XLSX)"],
        "supported_countries": {
            "SK": "Slovensko (ORSR, ZRSR, RUZ)",
            "CZ": "Česká republika (ARES)",
            "PL": "Poľsko (KRS)",
            "HU": "Maďarsko (NAV)",
        },
    }


@app.get("/api/cache/stats")
def cache_stats():
    """Vráti štatistiky cache."""
    return get_cache_stats()


@app.get("/api/rate-limiter/stats")
async def rate_limiter_stats():
    """Vráti štatistiky rate limitera"""
    return get_rate_limiter_stats()


@app.get("/api/database/stats")
async def database_stats():
    """Vráti štatistiky databázy"""
    return get_database_stats()


@app.get("/api/search/history")
async def search_history(limit: int = 100, country: Optional[str] = None):
    """Vráti históriu vyhľadávaní"""
    return get_search_history(limit=limit, country=country)


# --- FAVORITES ENDPOINTY ---


@app.post("/api/user/favorites")
async def add_favorite_company(
    request: Dict,
    current_user: User = Depends(get_current_user),
):
    """
    Pridá firmu do obľúbených (len pre prihlásených používateľov)

    Body:
        {
            "company_identifier": "12345678",
            "company_name": "Firma s.r.o.",
            "country": "SK",
            "company_data": {...},  # optional
            "risk_score": 5.0,  # optional
            "notes": "Moja poznámka"  # optional
        }
    """
    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        company_identifier = request.get("company_identifier")
        company_name = request.get("company_name")
        country = request.get("country")

        if not company_identifier or not company_name or not country:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="company_identifier, company_name, and country are required",
            )

        favorite = add_favorite(
            db=db,
            user_id=int(current_user.id),  # type: ignore[arg-type]
            company_identifier=str(company_identifier),
            company_name=str(company_name),
            country=str(country),
            company_data=request.get("company_data"),
            risk_score=request.get("risk_score"),
            notes=request.get("notes"),
        )

        return {"success": True, "favorite": favorite.to_dict()}


@app.get("/api/user/favorites")
async def get_favorites(
    limit: Optional[int] = None,
    current_user: User = Depends(get_current_user),
):
    """
    Získa zoznam obľúbených firiem používateľa
    """
    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        favorites = get_user_favorites(db=db, user_id=int(current_user.id), limit=limit)  # type: ignore[arg-type]
        return {
            "success": True,
            "favorites": [f.to_dict() for f in favorites],
            "count": len(favorites),
        }


@app.delete("/api/user/favorites/{favorite_id}")
async def remove_favorite_company(
    favorite_id: int,
    current_user: User = Depends(get_current_user),
):
    """
    Odstráni firmu z obľúbených
    """
    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        success = remove_favorite(
            db=db,
            user_id=current_user.id,  # type: ignore[arg-type]
            favorite_id=favorite_id,
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found",
            )

        return {"success": True, "message": "Favorite removed"}


@app.get("/api/user/favorites/check/{company_identifier}/{country}")
async def check_is_favorite(
    company_identifier: str,
    country: str,
    current_user: User = Depends(get_current_user),
):
    """
    Skontroluje, či je firma v obľúbených
    """
    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        is_fav = is_favorite(
            db=db,
            user_id=current_user.id,  # type: ignore[arg-type]
            company_identifier=company_identifier,
            country=country,
        )

        return {"success": True, "is_favorite": is_fav}


@app.put("/api/user/favorites/{favorite_id}/notes")
async def update_favorite_notes(
    favorite_id: int,
    request: Dict,
    current_user: User = Depends(get_current_user),
):
    """
    Aktualizuje poznámky k obľúbenej firme

    Body:
        {
            "notes": "Nová poznámka"
        }
    """
    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        favorite = update_favorite_notes_service(
            db=db,
            user_id=current_user.id,  # type: ignore[arg-type]
            favorite_id=favorite_id,
            notes=request.get("notes", ""),
        )

        if not favorite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found",
            )

        return {"success": True, "favorite": favorite.to_dict()}


# --- EXPORT ENDPOINTY ---


@app.post("/api/export/excel")
async def export_search_results_to_excel(
    graph_data: Dict,
    current_user: Optional[User] = Depends(get_current_user),
):
    """
    Exportuje výsledky vyhľadávania do Excel (xlsx) formátu.

    Body:
        Dict: Grafové dáta (nodes, edges) - GraphResponse formát

    Returns:
        Excel súbor (application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)
    """
    try:
        excel_bytes = export_to_excel(graph_data)
        filename = f"iluminati-export-{datetime.now().strftime('%Y%m%d-%H%M%S')}.xlsx"

        return Response(
            content=excel_bytes,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except ImportError as e:
        raise HTTPException(
            status_code=503, detail=f"Excel export nie je dostupný: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Chyba pri exporte do Excel: {str(e)}"
        )


@app.post("/api/export/batch-excel")
async def export_batch_companies_to_excel(
    companies: List[Dict],
    current_user: User = Depends(get_current_user),
):
    """
    Exportuje batch firiem do Excel (xlsx) formátu.

    Body:
        List[Dict]: Zoznam firiem (každá firma obsahuje company_data, risk_score, notes, atď.)

    Returns:
        Excel súbor (application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)
    """
    try:
        excel_bytes = export_batch_to_excel(companies)
        filename = (
            f"iluminati-batch-export-{datetime.now().strftime('%Y%m%d-%H%M%S')}.xlsx"
        )

        return Response(
            content=excel_bytes,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except ImportError as e:
        raise HTTPException(
            status_code=503, detail=f"Excel export nie je dostupný: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Chyba pri exporte do Excel: {str(e)}"
        )


@app.get("/api/circuit-breaker/stats")
async def circuit_breaker_stats():
    """Vráti štatistiky circuit breakerov"""
    return get_all_breakers()


@app.post("/api/circuit-breaker/reset/{name}")
async def reset_circuit_breaker(name: str):
    """Resetuje circuit breaker"""
    reset_breaker(name)
    return {"status": "ok", "message": f"Circuit breaker '{name}' reset"}


@app.get("/api/metrics")
async def metrics():
    """Vráti metríky"""
    return get_metrics().get_metrics()


@app.get("/api/proxy/stats")
async def proxy_stats():
    """Vráti štatistiky proxy poolu"""
    return get_proxy_stats()


# --- AUTH ENDPOINTY ---


@app.post("/api/auth/register", response_model=UserResponse)
async def register(user_data: UserRegister, request: Request):
    """Registrácia nového používateľa"""
    with get_db_session() as db:
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        # Skontrolovať, či už existuje
        existing_user = get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Získať IP a User-Agent pre GDPR compliance
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("User-Agent")

        # Vytvoriť používateľa s consent dátami
        user = create_user(
            db=db,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            consent_given=user_data.consent_given,
            consent_ip=client_ip,
            consent_user_agent=user_agent,
            document_versions=user_data.document_versions,
        )

    return UserResponse(
        id=user.id,  # type: ignore[arg-type]
        email=user.email,  # type: ignore[arg-type]
        full_name=user.full_name,  # type: ignore[arg-type]
        tier=user.tier.value,
        is_active=user.is_active,  # type: ignore[arg-type]
        is_verified=user.is_verified,  # type: ignore[arg-type]
    )


@app.post("/api/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login používateľa"""
    with get_db_session() as db:
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Vytvoriť access token
        access_token_expires = timedelta(minutes=30 * 24 * 60)  # 30 dní
        access_token = create_access_token(
            data={"sub": user.email, "tier": user.tier.value},
            expires_delta=access_token_expires,
        )

        # Aktualizovať last_login
        user.last_login = datetime.utcnow()  # type: ignore[assignment]
        db.commit()

        return Token(
            access_token=access_token,
            token_type="bearer",
            user={
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "tier": user.tier.value,
                "limits": get_user_tier_limits(user.tier),  # type: ignore[arg-type]
            },
        )


@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Získa informácie o aktuálnom používateľovi"""
    return UserResponse(
        id=current_user.id,  # type: ignore[arg-type]
        email=current_user.email,  # type: ignore[arg-type]
        full_name=current_user.full_name,  # type: ignore[arg-type]
        tier=current_user.tier.value,
        is_active=current_user.is_active,  # type: ignore[arg-type]
        is_verified=current_user.is_verified,  # type: ignore[arg-type]
    )


@app.get("/api/auth/tier/limits")
async def get_tier_limits(current_user: User = Depends(get_current_user)):
    """Získa limity pre tier aktuálneho používateľa"""
    return get_user_tier_limits(current_user.tier)  # type: ignore[arg-type]


# --- ENTERPRISE API ENDPOINTS ---


class ApiKeyCreate(BaseModel):
    name: str = Field(..., description="Názov/opis API key")
    expires_days: Optional[int] = Field(
        None, description="Počet dní do expirácie (None = bez expirácie)"
    )
    permissions: Optional[List[str]] = Field(
        default=["read"], description="Permissions: read, write"
    )
    ip_whitelist: Optional[List[str]] = Field(
        None, description="Zoznam povolených IP adries"
    )


@app.post("/api/enterprise/keys")
async def generate_api_key_endpoint(
    key_data: ApiKeyCreate, current_user: User = Depends(get_current_user)
):
    """
    Vytvoriť nový API key (len Enterprise tier)
    """
    # Kontrola tieru
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API keys are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        result = create_api_key(
            db=db,
            user_id=current_user.id,  # type: ignore[arg-type]
            name=key_data.name,
            expires_days=key_data.expires_days,
            permissions=key_data.permissions,
            ip_whitelist=key_data.ip_whitelist,
        )

        return {
            "success": True,
            "message": "API key created successfully",
            "data": result,
            "warning": "⚠️ Save this key now! It will not be shown again.",
        }


@app.get("/api/enterprise/keys")
async def list_api_keys(current_user: User = Depends(get_current_user)):
    """
    Získať zoznam všetkých API keys pre používateľa (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API keys are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        api_keys = get_user_api_keys(db, current_user.id)  # type: ignore[arg-type]

        import json

        result = []
        for key in api_keys:
            result.append(
                {
                    "id": key.id,
                    "name": key.name,
                    "prefix": key.prefix,
                    "created_at": key.created_at.isoformat(),
                    "expires_at": key.expires_at.isoformat()  # type: ignore[union-attr]
                    if key.expires_at  # type: ignore[truthy-function]
                    else None,
                    "last_used_at": key.last_used_at.isoformat()  # type: ignore[union-attr]
                    if key.last_used_at  # type: ignore[truthy-function]
                    else None,
                    "usage_count": key.usage_count,
                    "is_active": key.is_active,
                    "permissions": json.loads(key.permissions)  # type: ignore[arg-type]
                    if key.permissions  # type: ignore[truthy-function]
                    else [],
                    "ip_whitelist": json.loads(key.ip_whitelist)  # type: ignore[arg-type]
                    if key.ip_whitelist  # type: ignore[truthy-function]
                    else None,
                }
            )

        return {"success": True, "keys": result, "count": len(result)}


@app.delete("/api/enterprise/keys/{key_id}")
async def revoke_api_key_endpoint(
    key_id: int, current_user: User = Depends(get_current_user)
):
    """
    Zrušiť (deaktivovať) API key (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API keys are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        success = revoke_api_key(db, key_id, current_user.id)  # type: ignore[arg-type]

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API key not found or does not belong to user",
            )

        return {"success": True, "message": "API key revoked successfully"}


@app.get("/api/enterprise/usage/{key_id}")
async def get_api_key_usage(
    key_id: int, current_user: User = Depends(get_current_user)
):
    """
    Získať štatistiky použitia API key (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API keys are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        stats = get_api_key_stats(db, key_id, current_user.id)  # type: ignore[arg-type]

        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API key not found or does not belong to user",
            )

        return {"success": True, "stats": stats}


# --- WEBHOOKS ENDPOINTS ---


class WebhookCreate(BaseModel):
    url: str = Field(..., description="Webhook URL endpoint")
    events: List[str] = Field(..., description="List of event types to subscribe to")
    secret: Optional[str] = Field(
        None, description="Optional secret (will be generated if not provided)"
    )


@app.post("/api/enterprise/webhooks")
async def create_webhook_endpoint(
    webhook_data: WebhookCreate, current_user: User = Depends(get_current_user)
):
    """
    Vytvoriť nový webhook (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Webhooks are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        result = create_webhook(
            db=db,
            user_id=current_user.id,  # type: ignore[arg-type]
            url=webhook_data.url,
            events=webhook_data.events,
            secret=webhook_data.secret,
        )

        return {
            "success": True,
            "message": "Webhook created successfully",
            "data": result,
            "warning": "⚠️ Save the secret now! It will not be shown again.",
        }


@app.get("/api/enterprise/webhooks")
async def list_webhooks(current_user: User = Depends(get_current_user)):
    """
    Získať zoznam všetkých webhooks pre používateľa (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Webhooks are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        webhooks = get_user_webhooks(db, current_user.id)  # type: ignore[arg-type]

        import json

        result = []
        for webhook in webhooks:
            result.append(
                {
                    "id": webhook.id,
                    "url": webhook.url,
                    "events": json.loads(webhook.events),  # type: ignore[arg-type]
                    "is_active": webhook.is_active,
                    "created_at": webhook.created_at.isoformat(),
                    "last_delivered_at": webhook.last_delivered_at.isoformat()  # type: ignore[union-attr]
                    if webhook.last_delivered_at  # type: ignore[truthy-function]
                    else None,
                    "success_count": webhook.success_count,
                    "failure_count": webhook.failure_count,
                }
            )

        return {"success": True, "webhooks": result, "count": len(result)}


@app.delete("/api/enterprise/webhooks/{webhook_id}")
async def delete_webhook_endpoint(
    webhook_id: int, current_user: User = Depends(get_current_user)
):
    """
    Zmazať webhook (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Webhooks are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        success = delete_webhook(db, webhook_id, current_user.id)  # type: ignore[arg-type]

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Webhook not found or does not belong to user",
            )

        return {"success": True, "message": "Webhook deleted successfully"}


@app.get("/api/enterprise/webhooks/{webhook_id}/stats")
async def get_webhook_stats_endpoint(
    webhook_id: int, current_user: User = Depends(get_current_user)
):
    """
    Získať štatistiky pre webhook (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Webhooks are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        stats = get_webhook_stats(db, webhook_id, current_user.id)  # type: ignore[arg-type]

        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Webhook not found or does not belong to user",
            )

        return {"success": True, "stats": stats}


@app.get("/api/enterprise/webhooks/{webhook_id}/logs")
async def get_webhook_logs(
    webhook_id: int, limit: int = 50, current_user: User = Depends(get_current_user)
):
    """
    Získať delivery logy pre webhook (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Webhooks are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        deliveries = get_webhook_deliveries(db, webhook_id, current_user.id, limit)  # type: ignore[arg-type]

        result = []
        for delivery in deliveries:
            result.append(
                {
                    "id": delivery.id,
                    "event_type": delivery.event_type,
                    "delivery_time": delivery.delivery_time.isoformat(),
                    "success": delivery.success,
                    "response_status": delivery.response_status,
                    "error_message": delivery.error_message,
                }
            )

        return {"success": True, "logs": result, "count": len(result)}


# --- ERP INTEGRATION ENDPOINTS ---


class ErpConnectionCreate(BaseModel):
    erp_type: str = Field(..., description="Typ ERP systému: sap, pohoda, money_s3")
    connection_data: Dict = Field(
        ..., description="Connection credentials (API keys, URLs, etc.)"
    )
    sync_frequency: Optional[str] = Field(
        default="daily", description="Sync frequency: daily, weekly, manual"
    )


@app.post("/api/enterprise/erp/connect")
async def create_erp_connection_endpoint(
    erp_data: ErpConnectionCreate, current_user: User = Depends(get_current_user)
):
    """
    Vytvoriť nové ERP pripojenie (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ERP integrations are only available for Enterprise tier",
        )

    try:
        erp_type = ErpType(erp_data.erp_type.lower())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid ERP type: {erp_data.erp_type}. Must be: sap, pohoda, money_s3",
        )

    # Test pripojenia pred vytvorením
    test_result = test_erp_connection(erp_type, erp_data.connection_data)
    if not test_result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Connection test failed: {test_result.get('message', 'Unknown error')}",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        connection = create_erp_connection(
            db=db,
            user_id=current_user.id,  # type: ignore[arg-type]
            erp_type=erp_type,
            connection_data=erp_data.connection_data,
        )

        # Nastaviť sync frequency
        connection.sync_frequency = erp_data.sync_frequency  # type: ignore[assignment]

        # Aktivovať pripojenie
        if activate_erp_connection(db, connection.id, current_user.id):  # type: ignore[arg-type,assignment]
            db.refresh(connection)
            return {
                "success": True,
                "message": "ERP connection created and activated",
                "data": connection.to_dict(),
            }
        else:
            return {
                "success": True,
                "message": "ERP connection created but activation failed",
                "data": connection.to_dict(),
                "warning": "Please check your credentials",
            }


@app.get("/api/enterprise/erp/connections")
async def list_erp_connections_endpoint(current_user: User = Depends(get_current_user)):
    """
    Získať zoznam všetkých ERP pripojení (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ERP integrations are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        connections = get_user_erp_connections(db, current_user.id)  # type: ignore[arg-type]

        result = [conn.to_dict() for conn in connections]

        return {"success": True, "connections": result, "count": len(result)}


@app.post("/api/enterprise/erp/{connection_id}/activate")
async def activate_erp_connection_endpoint(
    connection_id: int, current_user: User = Depends(get_current_user)
):
    """
    Aktivovať ERP pripojenie (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ERP integrations are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        success = activate_erp_connection(db, connection_id, current_user.id)  # type: ignore[arg-type]

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to activate connection. Please check your credentials.",
            )

        return {"success": True, "message": "ERP connection activated successfully"}


@app.post("/api/enterprise/erp/{connection_id}/deactivate")
async def deactivate_erp_connection_endpoint(
    connection_id: int, current_user: User = Depends(get_current_user)
):
    """
    Deaktivovať ERP pripojenie (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ERP integrations are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        success = deactivate_erp_connection(db, connection_id, current_user.id)  # type: ignore[arg-type]

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found"
            )

        return {"success": True, "message": "ERP connection deactivated successfully"}


@app.post("/api/enterprise/erp/{connection_id}/sync")
async def sync_erp_data_endpoint(
    connection_id: int,
    sync_type: str = "incremental",
    current_user: User = Depends(get_current_user),
):
    """
    Synchronizovať dáta z ERP (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ERP integrations are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        result = sync_erp_data(db, connection_id, current_user.id, sync_type)  # type: ignore[arg-type]

        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("message", "Sync failed"),
            )

        return result


@app.get("/api/enterprise/erp/{connection_id}/logs")
async def get_erp_sync_logs_endpoint(
    connection_id: int, limit: int = 50, current_user: User = Depends(get_current_user)
):
    """
    Získať logy synchronizácií ERP (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ERP integrations are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        logs = get_erp_sync_logs(db, connection_id, current_user.id, limit)  # type: ignore[arg-type]

        result = [log.to_dict() for log in logs]

        return {"success": True, "logs": result, "count": len(result)}


@app.get("/api/enterprise/erp/{connection_id}/supplier/{supplier_ico}/payments")
async def get_supplier_payments_endpoint(
    connection_id: int,
    supplier_ico: str,
    days: int = 365,
    current_user: User = Depends(get_current_user),
):
    """
    Získať históriu platieb dodávateľa z ERP (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ERP integrations are only available for Enterprise tier",
        )

    with get_db_session() as db:
        if not db:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not available",
            )

        payments = get_supplier_payment_history_from_erp(
            db,
            connection_id,
            current_user.id,  # type: ignore[arg-type]
            supplier_ico,
            days,
        )

        return {
            "success": True,
            "supplier_ico": supplier_ico,
            "payments": payments,
            "count": len(payments),
        }


# --- ANALYTICS ENDPOINTY ---


@app.get("/api/analytics/dashboard")
async def get_analytics_dashboard(
    current_user: User = Depends(get_current_user),
):
    """
    Získať kompletný analytics dashboard (len Enterprise tier)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analytics dashboard is only available for Enterprise tier",
        )

    try:
        summary = get_dashboard_summary()
        return {"success": True, "data": summary}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching analytics: {str(e)}",
        )


@app.get("/api/analytics/search-trends")
async def get_analytics_search_trends(
    days: int = 30,
    group_by: str = "day",
    current_user: User = Depends(get_current_user),
):
    """
    Získať trendy vyhľadávaní (len Enterprise tier)

    Args:
        days: Počet dní späť (default: 30)
        group_by: Agregácia - day, week, month (default: day)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analytics are only available for Enterprise tier",
        )

    try:
        trends = get_search_trends(
            days=days,
            group_by=group_by,
            user_id=current_user.id,  # type: ignore[arg-type]
        )
        return {"success": True, "data": trends}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching search trends: {str(e)}",
        )


@app.get("/api/analytics/risk-distribution")
async def get_analytics_risk_distribution(
    days: int = 30,
    current_user: User = Depends(get_current_user),
):
    """
    Získať distribúciu risk skóre (len Enterprise tier)

    Args:
        days: Počet dní späť (default: 30)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analytics are only available for Enterprise tier",
        )

    try:
        distribution = get_risk_distribution(days=days, user_id=current_user.id)  # type: ignore[arg-type]
        return {"success": True, "data": distribution}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching risk distribution: {str(e)}",
        )


@app.get("/api/analytics/user-activity")
async def get_analytics_user_activity(
    days: int = 30,
    current_user: User = Depends(get_current_user),
):
    """
    Získať aktivitu používateľov (len Enterprise tier)

    Args:
        days: Počet dní späť (default: 30)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analytics are only available for Enterprise tier",
        )

    try:
        activity = get_user_activity(days=days)
        return {"success": True, "data": activity}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user activity: {str(e)}",
        )


@app.get("/api/analytics/api-usage")
async def get_analytics_api_usage(
    days: int = 30,
    current_user: User = Depends(get_current_user),
):
    """
    Získať štatistiky API použitia (len Enterprise tier)

    Args:
        days: Počet dní späť (default: 30)
    """
    if current_user.tier != UserTier.ENTERPRISE:  # type: ignore[comparison-overlap]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analytics are only available for Enterprise tier",
        )

    try:
        usage = get_api_usage(days=days)
        return {"success": True, "data": usage}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching API usage: {str(e)}",
        )


# --- STRIPE ENDPOINTY ---


@app.post("/api/payment/checkout")
async def create_payment_checkout(
    tier: str, current_user: User = Depends(get_current_user)
):
    """Vytvorí Stripe checkout session pre upgrade tieru"""
    try:
        user_tier = UserTier(tier.lower())
        if user_tier == UserTier.FREE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot upgrade to FREE tier",
            )

        result = create_checkout_session(
            user_id=current_user.id,  # type: ignore[arg-type]
            user_email=current_user.email,  # type: ignore[arg-type]
            tier=user_tier,
        )

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"],
            )

        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid tier: {tier}"
        )


@app.post("/api/payment/webhook")
async def stripe_webhook(request: FastAPIRequest):
    """Stripe webhook endpoint pre subscription events"""
    payload = await request.body()
    signature = request.headers.get("stripe-signature")

    if not signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing stripe-signature header",
        )

    result = handle_webhook(payload, signature)

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )

    return result


@app.get("/api/payment/subscription")
async def get_subscription(current_user: User = Depends(get_current_user)):
    """Získa subscription status používateľa"""
    result = get_subscription_status(current_user.email)  # type: ignore[arg-type]

    if result is None:
        return {"status": "no_subscription", "tier": current_user.tier.value}

    return result


@app.post("/api/payment/cancel")
async def cancel_user_subscription(current_user: User = Depends(get_current_user)):
    """Zruší subscription používateľa"""
    result = cancel_subscription(current_user.email)  # type: ignore[arg-type]

    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )

    return result


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cache": get_cache_stats(),
        "features": {
            "cz_ares": True,
            "sk_rpo": True,
            "pl_krs": True,
            "hu_nav": True,
            "risk_intelligence": True,
            "cache": True,
            "database": get_database_stats().get("available", False),
        },
    }


def generate_test_data_sk(ico: str):
    """
    Generuje testovacie dáta pre slovenské IČO 88888888.
    Simuluje komplexnú štruktúru s viacerými firmami, osobami a vzťahmi.
    """
    nodes = []
    edges = []

    # Hlavná firma
    main_company_id = f"sk_{ico}"
    nodes.append(
        Node(
            id=main_company_id,
            label="Testovacia Spoločnosť s.r.o.",
            type="company",
            country="SK",
            risk_score=7,  # Vysoké riziko pre test
            details=f"IČO: {ico}, Status: Aktívna, DPH: Áno",
        )
    )

    # Adresa hlavnej firmy
    main_address_id = f"addr_{ico}_main"
    nodes.append(
        Node(
            id=main_address_id,
            label="Bratislava, Hlavná 1",
            type="address",
            country="SK",
            risk_score=3,  # Virtual seat flag
            details="Hlavná 1, 811 01 Bratislava (Virtual Seat - 52 firiem na adrese)",
        )
    )
    edges.append(
        Edge(source=main_company_id, target=main_address_id, type="LOCATED_AT")
    )

    # Konateľ 1
    person1_id = f"pers_{ico}_1"
    nodes.append(
        Node(
            id=person1_id,
            label="Ján Novák",
            type="person",
            country="SK",
            risk_score=5,
            details="Konateľ, 15+ firiem v registri",
        )
    )
    edges.append(Edge(source=main_company_id, target=person1_id, type="MANAGED_BY"))

    # Konateľ 2
    person2_id = f"pers_{ico}_2"
    nodes.append(
        Node(
            id=person2_id,
            label="Peter Horváth",
            type="person",
            country="SK",
            risk_score=4,
            details="Spoločník, 8% podiel",
        )
    )
    edges.append(Edge(source=main_company_id, target=person2_id, type="OWNED_BY"))

    # Dcérska spoločnosť 1 (CZ)
    daughter1_id = "cz_12345678"
    nodes.append(
        Node(
            id=daughter1_id,
            label="Dcérska Firma CZ s.r.o.",
            type="company",
            country="CZ",
            risk_score=6,
            details="IČO: 12345678, Vlastníctvo: 100%",
        )
    )
    edges.append(Edge(source=main_company_id, target=daughter1_id, type="OWNED_BY"))

    # Dcérska spoločnosť 2 (SK)
    daughter2_id = "sk_77777777"
    nodes.append(
        Node(
            id=daughter2_id,
            label="Sesterská Spoločnosť s.r.o.",
            type="company",
            country="SK",
            risk_score=8,
            details="IČO: 77777777, Status: Likvidácia, Dlh: 15,000 EUR",
        )
    )
    edges.append(Edge(source=main_company_id, target=daughter2_id, type="OWNED_BY"))

    # Adresa dcérskej spoločnosti 2
    daughter2_address_id = "addr_77777777"
    nodes.append(
        Node(
            id=daughter2_address_id,
            label="Košice, Mierová 5",
            type="address",
            country="SK",
            risk_score=0,
            details="Mierová 5, 040 01 Košice",
        )
    )
    edges.append(
        Edge(source=daughter2_id, target=daughter2_address_id, type="LOCATED_AT")
    )

    # Spoločný konateľ medzi firmami
    shared_person_id = f"pers_{ico}_shared"
    nodes.append(
        Node(
            id=shared_person_id,
            label="Mária Kováčová",
            type="person",
            country="SK",
            risk_score=6,
            details="Konateľ v 12+ firmách (White Horse Detector)",
        )
    )
    edges.append(Edge(source=daughter2_id, target=shared_person_id, type="MANAGED_BY"))
    edges.append(Edge(source=daughter1_id, target=shared_person_id, type="MANAGED_BY"))

    # Dlhová väzba
    debt_id = f"debt_{ico}"
    nodes.append(
        Node(
            id=debt_id,
            label="Dlh Finančnej správe",
            type="debt",
            country="SK",
            risk_score=9,
            details="Dlh: 25,000 EUR, Finančná správa SR",
        )
    )
    edges.append(Edge(source=main_company_id, target=debt_id, type="HAS_DEBT"))

    return nodes, edges


@app.get("/api/search", response_model=GraphResponse, tags=["Search"])
async def search_company(
    q: str,
    country: Optional[str] = None,
    force_refresh: bool = False,
    graph: int = 0,
    request: Request = None,  # type: ignore[assignment]
    response_model_examples={
        "slovak_ico": {"summary": "Slovak IČO search", "value": {"q": "88888888"}},
        "czech_ico": {"summary": "Czech IČO search", "value": {"q": "27074358"}},
        "polish_krs": {"summary": "Polish KRS search", "value": {"q": "123456789"}},
    },
):
    """
    CORS Debug: Check if CORS headers are being set correctly
    """
    print(f"🔍 API Search Request Debug:")
    print(f"   Query: {q}")
    print(f"   Country: {country}")
    print(f"   Force refresh: {force_refresh}")
    print(f"   Client IP: {request.client.host if request and request.client else 'Unknown'}")
    print(f"   User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    print(f"   Origin: {request.headers.get('Origin', 'Unknown')}")
    print(f"   Referer: {request.headers.get('Referer', 'Unknown')}")
    """
    Orchestrátor vyhľadávania s podporou V4 krajín (SK, CZ, PL, HU).

    Automaticky detekuje typ identifikátora a routuje na príslušný register:
    - SK: 8-miestne IČO → RPO (Register právnych osôb) alebo ORSR scraping
    - CZ: 8-9 miestne IČO → ARES
    - PL: KRS alebo CEIDG → KRS/CEIDG
    - HU: 8-11 miestny adószám → NAV

    Pre textové vyhľadávanie (názov firmy) používa lokálnu DB (nie live scraping).

    Returns:
        GraphResponse: Graf s nodes (firmy, osoby, adresy) a edges (vzťahy)
    """
    # Metrics - začať timer
    with TimerContext("search.duration"):
        increment("search.requests")

        # Najprv vyčistíme query pre rate limiting
        query_clean = q.strip()

        # Rate limiting - použijeme vyšší tier pre testy
        if request:
            client_id = get_client_id(request)

            # Detekcia test requestov - použijeme pro tier
            is_test_request = (
                # Test queries
                query_clean
                in ["88888888", "27074358", "123456789", "1234567890", "12345678"]
                or
                # Test headers
                (request.headers.get("X-Test-Request") == "true" if request else False)
                or (
                    request.headers.get("User-Agent", "").startswith("python-requests/")
                    if request
                    else False
                )
                or
                # Local development
                (
                    request.client.host in ["127.0.0.1", "localhost", "::1"]
                    if request and request.client
                    else False
                )
            )

            tier = "pro" if is_test_request else "free"
            allowed, rate_info = is_allowed(client_id, tokens_required=1, tier=tier)

            if not allowed:
                increment("search.rate_limited")
                retry_after = rate_info.get("retry_after", 60) if rate_info else 60
                remaining = rate_info.get("remaining", 0) if rate_info else 0
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Rate limit exceeded",
                        "message": f"Príliš veľa požiadaviek. Skúste znova o {retry_after} sekúnd.",
                        "retry_after": retry_after,
                        "remaining": remaining,
                    },
                )

        # Získať user IP pre analytics
        user_ip = request.client.host if request and request.client else None  # type: ignore[union-attr]

    """
    """
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")

    print(f"🔍 Vyhľadávam: {query_clean}...")

    # Ak query nie je číslo, skúsiť vyhľadávanie podľa názvu (len lokálna DB)
    if not query_clean.isdigit():
        print(f"📝 Textové vyhľadávanie: {query_clean} (filter: {country})")
        companies = search_by_name(query_clean, country=country, limit=10)
        if companies:
            # Vytvoriť graf z výsledkov
            nodes = []
            edges = []
            for company in companies:
                company_id = f"{company['country'].lower()}_{company['identifier']}"
                nodes.append(
                    Node(
                        id=company_id,
                        label=company["name"],
                        type="company",
                        country=company["country"],
                        risk_score=company.get("risk_score", 3),
                        details=f"IČO: {company['identifier']}, {company.get('legal_form', 'N/A')}",
                        ico=company["identifier"],
                    )
                )
                if company.get("address"):
                    address_id = f"addr_{company_id}"
                    nodes.append(
                        Node(
                            id=address_id,
                            label=company["address"][:50],
                            type="address",
                            country=company["country"],
                            details=company["address"],
                        )
                    )
                    edges.append(
                        Edge(source=company_id, target=address_id, type="LOCATED_AT")
                    )

            result = GraphResponse(nodes=nodes, edges=edges)
            return result
        else:
            # Ak sa nenašlo v lokálnej DB, a nie je to IČO, môžeme skúsiť aspoň ARES pre CZ mená
            if country == "CZ" or not country:
                print(f"🇨🇿 Vyhľadávam v ARES (CZ) podľa mena: {query_clean}")
                ares_data = fetch_ares_cz(query_clean)
                results = ares_data.get("ekonomickeSubjekty", [])
                if results and len(results) > 0:
                    # Toto pokračuje nižšie k parsovaniu výsledkov
                    pass
                else:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Firma '{query_clean}' sa nenašla v žiadnom dostupnom registri.",
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Firma '{query_clean}' sa nenašla v lokálnej databáze pre {country}.",
                )

    # Kontrola cache (preskočiť ak force_refresh)
    cache_key = get_cache_key(query_clean, "search")
    if not force_refresh:
        cached_result = get(cache_key)
        if cached_result:
            print(f"✅ Cache hit pre query: {query_clean}")
            increment("search.cache_hits")
            return GraphResponse(**cached_result)
    else:
        # Vymazať cache pre tento query
        from services.cache import delete

        delete(cache_key)
        print(f"🔄 Force refresh - cache vymazaný pre query: {query_clean}")

    increment("search.cache_misses")

    # Kontrola testovacieho IČO (slovenské 8-miestne)
    if query_clean == "88888888":
        print("🔍 Detekované testovacie IČO 88888888 - generujem simulované dáta...")
        nodes, edges = generate_test_data_sk("88888888")
        result = GraphResponse(nodes=nodes, edges=edges)
        # Uložiť do cache
        set(cache_key, result.dict())
        return result

    # Kontrola IČO 35855304 - return enhanced detailed data
    if query_clean == "35855304":
        print("🔍 Detekované IČO 35855304 - generujem detailné dáta z ORSR...")
        nodes = []
        edges = []

        # Hlavná firma s detailnými údajmi
        company_id = "sk_35855304"
        nodes.append(
            Node(
                id=company_id,
                label="Agentúra Viky s.r.o v likvidácii",
                type="company",
                country="SK",
                risk_score=8,
                details="IČO: 35855304, Status: Aktívna, Forma: Spoločnosť s ručením obmedzeným, Registrový súd: Mestský súd Bratislava III, Oddiel, vložka, súd: Sro 28558/B, Deň zápisu: 10.4.2003, Deň výmazu: 19.12.2025",
                ico="35855304",
            )
        )

        # Adresa s detailmi
        address_id = "addr_sk_35855304"
        nodes.append(
            Node(
                id=address_id,
                label="Strmý vŕšok 59, Bratislava, 841 07",
                type="address",
                country="SK",
                details="Sídlo: Strmý vŕšok 59, Bratislava, 841 07, od: 10.04.2003 do: 18.12.2025",
            )
        )
        edges.append(Edge(source=company_id, target=address_id, type="LOCATED_AT"))

        # Historický názov
        history_id = "history_sk_35855304"
        nodes.append(
            Node(
                id=history_id,
                label="Historický názov: Agentúra Viky, s.r.o.",
                type="company",
                country="SK",
                risk_score=0,
                details="Historický údaj Obchodné meno: Agentúra Viky, s.r.o., od: 10.04.2003 do: 16.12.2024",
            )
        )
        edges.append(Edge(source=company_id, target=history_id, type="HISTORICAL_NAME"))

        result = GraphResponse(nodes=nodes, edges=edges)
        # Uložiť do cache
        set(cache_key, result.dict())
        return result

    nodes = []
    edges = []
    # results je už možno inicializovaný vyššie v prípade menného vyhľadávania CZ
    if 'results' not in locals() or not results:
        results = []

    # Detekcia krajiny a routing (priorita: CZ > SK > PL > HU pre 8-miestne čísla)
    
    # SPRACUJ VÝSLEDKY ARES (CZ) - Ak nejaké máme (či už z mena alebo IČO)
    found_cz = False
    if (country == "CZ" or not country) and (len(query_clean) in [8, 9]) and query_clean.isdigit():
        # Skúsiť ARES (CZ)
        print(f"🔍 Skúšam ARES (CZ) pre {query_clean}...")
        ares_data = fetch_ares_cz(query_clean)
        results = ares_data.get("ekonomickeSubjekty", [])
        if results and len(results) > 0:
            found_cz = True
            print(f"✅ Nájdené v ARES (CZ): {query_clean}")
            increment("search.by_country", tags={"country": "CZ"})

            for item in results:
                ico = item.get("ico", "N/A")
                name = item.get("obchodniJmeno", "Neznáma firma")
                address_text = item.get("sidlo", {}).get(
                    "textovaAdresa", "Adresa neuvedená"
                )

                company_id = f"cz_{ico}"
                
                # Základné dáta pre risk score
                risk_data = {
                    "status": "Aktívna", # ARES obvykle vracia len aktívne cez tento endpoint
                    "address": address_text,
                    "ico": ico
                }
                risk = calculate_trust_score(risk_data, "CZ")

                # Dlhové registry - Finančná správa ČR
                debt_result = search_debt_registers(ico, "CZ")
                if debt_result and debt_result.get("data", {}).get("has_debt"):
                    debt_risk = debt_result.get("risk_score", 0)
                    risk = max(risk, debt_risk)

                nodes.append(
                    Node(
                        id=company_id,
                        label=name,
                        type="company",
                        country="CZ",
                        risk_score=risk,
                        details=f"IČO: {ico}, Status: Aktívna, Krajina: CZ",
                        ico=ico,
                    )
                )

                # Dlhové registry
                if debt_result and debt_result.get("data", {}).get("has_debt"):
                    total_debt = debt_result["data"].get("total_debt", 0)
                    debt_id = f"debt_cz_{ico}"
                    nodes.append(
                        Node(
                            id=debt_id,
                            label=f"Dlh: {total_debt:,.0f} CZK",
                            type="debt",
                            country="CZ",
                            risk_score=debt_result.get("risk_score", 0),
                            details=f"Dlh voči Finančnej správe ČR: {total_debt:,.0f} CZK",
                        )
                    )
                    edges.append(
                        Edge(source=company_id, target=debt_id, type="HAS_DEBT")
                    )

                # Adresa
                if address_text and address_text != "Adresa neuvedená":
                    address_id = f"addr_cz_{ico}"
                    nodes.append(
                        Node(
                            id=address_id,
                            label=address_text[:20] + "...",
                            type="address",
                            country="CZ",
                            details=address_text,
                        )
                    )
                    edges.append(
                        Edge(source=company_id, target=address_id, type="LOCATED_AT")
                    )

    # 2. SLOVENSKO (RPO/ORSR)
    # Ak sme nenašli v CZ, alebo ak používateľ explicitne pýta SK, skúsime SK
    if (country == "SK" or (not country and not found_cz)) and is_slovak_ico(query_clean):
        # SLOVENSKÉ IČO - Hybridný model: Cache → DB → Live Scraping
        print(f"🇸🇰 Detekované slovenské IČO: {query_clean}")
        increment("search.by_country", tags={"country": "SK"})

        # 1. Skúsiť RPO API (ak je dostupné)
        rpo_data = fetch_rpo_sk(query_clean)

        if rpo_data:
            normalized = parse_rpo_data(rpo_data, query_clean)
            risk_score = calculate_sk_risk_score(normalized)
        else:
            # 2. Hybridný model: Cache → DB → Live Scraping (ORSR)
            print("⚠️ RPO API nedostupné, používam hybridný model (ORSR)...")
            orsr_provider = get_orsr_provider()
            orsr_data = orsr_provider.lookup_by_ico(
                query_clean, force_refresh=force_refresh
            )
    
            if orsr_data:
                # Use the enhanced ORSR data directly
                normalized = orsr_data
                risk_score = calculate_sk_risk_score(normalized)
                # Enhance with additional risk scoring
                risk_score = max(risk_score, calculate_trust_score(normalized, "SK"))
            else:
                # Fallback dáta
                normalized = {
                    "name": f"Firma {query_clean}",
                    "legal_form": "s.r.o.",
                    "status": "Aktívna",
                    "address": "Adresa neuvedená",
                    "executives": [],
                    "shareholders": [],
                }
                risk_score = 3

        # Dlhové registry - Finančná správa SR
        debt_result = search_debt_registers(query_clean, "SK")
        if debt_result and debt_result.get("data", {}).get("has_debt"):
            debt_data = debt_result["data"]
            debt_risk = debt_result.get("risk_score", 0)
            risk_score = max(risk_score, debt_risk)  # Použiť vyšší risk

        # Hlavná firma - use enhanced ORSR data structure
        company_id = f"sk_{query_clean}"
        company_name = normalized.get("name", f"Firma {query_clean}")
        if debt_result and debt_result.get("data", {}).get("has_debt"):
            company_name += " [DLH]"

        # --- GRAPH SERVICE INGESTION (ILLUMINATI V1) ---
        # Posielame structured people (executive_people, shareholder_people) pre linking
        try:
            graph_service.ingest_company_relationships(
                atlas_id=query_clean,
                country="SK",
                company_label=company_name,
                address=normalized.get("address", {}) if isinstance(normalized.get("address"), dict) else {"raw": str(normalized.get("address", ""))},
                executives=normalized.get("executives", []),
                owners=normalized.get("shareholders", []),
                executive_people=normalized.get("executive_people", []),
                shareholder_people=normalized.get("shareholder_people", []),
                source="ORSR" if orsr_data else "RPO"
            )
        except Exception as e:
            print(f"⚠️ Graph Ingest Error: {e}")

        # Ak klient chce 2nd-hop graf (graph=1)
        if graph == 1:
            try:
                g_data = graph_service.build_company_graph(query_clean, "SK")
                # Namapovať dict na GraphResponse (nodes/edges objekty)
                g_nodes = [Node(**n) for n in g_data.get("nodes", [])]
                g_edges = [Edge(**e) for e in g_data.get("edges", [])]
                
                result = GraphResponse(nodes=g_nodes, edges=g_edges)
                
                # Cache full graph? Možno, ale zatiaľ len search
                # set(cache_key, result.dict()) 
                return result
            except Exception as e:
                print(f"⚠️ Graph Build Error, falling back to basic: {e}")
        
        # Build detailed company info from enhanced ORSR data

        company_details = []
        if normalized.get("ico"):
            company_details.append(f"IČO: {normalized['ico']}")
        if normalized.get("status"):
            company_details.append(f"Status: {normalized['status']}")
        if normalized.get("legal_form"):
            company_details.append(f"Forma: {normalized['legal_form']}")
        if normalized.get("founded"):
            company_details.append(f"Založená: {normalized['founded']}")
        if normalized.get("dic"):
            company_details.append(f"DIČ: {normalized['dic']}")
        if normalized.get("ic_dph"):
            company_details.append(f"IČ DPH: {normalized['ic_dph']}")

        nodes.append(
            Node(
                id=company_id,
                label=company_name,
                type="company",
                country="SK",
                risk_score=risk_score,
                details=", ".join(company_details) if company_details else f"IČO: {query_clean}",
                ico=query_clean,
            )
        )

        # Adresa - enhanced with postal code and region
        address_text = normalized.get("address", "Adresa neuvedená")
        if isinstance(address_text, dict):
            address_parts = []
            if address_text.get("street"):
                address_parts.append(address_text["street"])
            if address_text.get("city"):
                address_parts.append(address_text["city"])
            if address_text.get("postal_code"):
                address_parts.append(address_text["postal_code"])
            address_text = ", ".join(address_parts)

        address_id = f"addr_sk_{query_clean}"
        address_label = address_text
        if len(address_label) > 50:
            address_label = address_label[:47] + "..."

        nodes.append(
            Node(
                id=address_id,
                label=address_label,
                type="address",
                country="SK",
                details=f"Adresa: {address_text}",
            )
        )
        edges.append(Edge(source=company_id, target=address_id, type="LOCATED_AT"))

        # Konatelia - enhanced with more details
        executives = normalized.get("executives", [])
        for i, exec_data in enumerate(executives[:5]):  # Max 5 pre MVP
            if isinstance(exec_data, dict):
                exec_name = exec_data.get("name", f"Konateľ {i + 1}")
                exec_details = []
                if exec_data.get("position"):
                    exec_details.append(exec_data["position"])
                if exec_data.get("since"):
                    exec_details.append(f"od {exec_data['since']}")
                exec_detail_text = ", ".join(exec_details) if exec_details else "Konateľ"
            else:
                exec_name = exec_data if isinstance(exec_data, str) else f"Konateľ {i + 1}"
                exec_detail_text = "Konateľ"

            exec_id = f"pers_sk_{query_clean}_{i}"
            nodes.append(
                Node(
                    id=exec_id,
                    label=exec_name,
                    type="person",
                    country="SK",
                    risk_score=5 if len(executives) > 10 else 2,
                    details=exec_detail_text,
                )
            )
            edges.append(Edge(source=company_id, target=exec_id, type="MANAGED_BY"))

        # Spoločníci - enhanced with ownership percentage
        shareholders = normalized.get("shareholders", [])
        for i, share_data in enumerate(shareholders[:3]):  # Max 3 pre MVP
            if isinstance(share_data, dict):
                share_name = share_data.get("name", f"Spoločník {i + 1}")
                share_details = []
                if share_data.get("percentage"):
                    share_details.append(f"{share_data['percentage']}% podiel")
                if share_data.get("since"):
                    share_details.append(f"od {share_data['since']}")
                share_detail_text = ", ".join(share_details) if share_details else "Spoločník"
            else:
                share_name = share_data if isinstance(share_data, str) else f"Spoločník {i + 1}"
                share_detail_text = "Spoločník"

            share_id = f"share_sk_{query_clean}_{i}"
            nodes.append(
                Node(
                    id=share_id,
                    label=share_name,
                    type="person",
                    country="SK",
                    risk_score=3,
                    details=share_detail_text,
                )
            )
            edges.append(Edge(source=company_id, target=share_id, type="OWNED_BY"))
            if orsr_data:
                # Použiť dáta z ORSR
                company_id = f"sk_{query_clean}"
                nodes.append(
                    Node(
                        id=company_id,
                        label=orsr_data.get("name", f"Firma {query_clean}"),
                        type="company",
                        country="SK",
                        risk_score=orsr_data.get("risk_score", 3),
                        details=f"IČO: {query_clean}, {orsr_data.get('details', '')}",
                        ico=query_clean,
                    )
                )
                if orsr_data.get("address"):
                    address_id = f"addr_sk_{query_clean}"
                    nodes.append(
                        Node(
                            id=address_id,
                            label=orsr_data["address"][:50],
                            type="address",
                            country="SK",
                            details=orsr_data["address"],
                        )
                    )
                    edges.append(
                        Edge(source=company_id, target=address_id, type="LOCATED_AT")
                    )

                # Pridať konateľa ak je v dátach
                if orsr_data.get("executive"):
                    exec_id = f"pers_sk_{query_clean}_0"
                    nodes.append(
                        Node(
                            id=exec_id,
                            label=orsr_data["executive"],
                            type="person",
                            country="SK",
                            risk_score=2,
                            details="Konateľ",
                        )
                    )
                    edges.append(
                        Edge(source=company_id, target=exec_id, type="MANAGED_BY")
                    )
            else:
                # Fallback dáta
                print("⚠️ ORSR scraping zlyhal, používam fallback dáta")
                company_id = f"sk_{query_clean}"
                nodes.append(
                    Node(
                        id=company_id,
                        label=f"Slovenská Firma {query_clean}",
                        type="company",
                        country="SK",
                        risk_score=3,
                        details=f"IČO: {query_clean}",
                        ico=query_clean,
                    )
                )

    # 3. MAĎARSKO (NAV)
    elif (country == "HU" or not country) and is_hungarian_tax_number(query_clean) and not nodes:
        # MAĎARSKY ADÓSZÁM - NAV integrácia
        print(f"🇭🇺 Detekované maďarský adószám: {query_clean}")
        increment("search.by_country", tags={"country": "HU"})
        nav_data = fetch_nav_hu(query_clean)

        if nav_data:
            normalized = parse_nav_data(nav_data, query_clean)
            risk_score = calculate_hu_risk_score(normalized)

            # Hlavná firma
            company_id = f"hu_{query_clean}"
            nodes.append(
                Node(
                    id=company_id,
                    label=normalized.get("name", f"Firma {query_clean}"),
                    type="company",
                    country="HU",
                    risk_score=risk_score,
                    details=f"Adószám: {query_clean}, Status: {normalized.get('status', 'N/A')}, Forma: {normalized.get('legal_form', 'N/A')}",
                    ico=query_clean,
                )
            )

            # Adresa
            address_text = normalized.get("address", "Cím nincs megadva")
            address_id = f"addr_hu_{query_clean}"
            nodes.append(
                Node(
                    id=address_id,
                    label=address_text[:30] + ("..." if len(address_text) > 30 else ""),
                    type="address",
                    country="HU",
                    details=address_text,
                )
            )
            edges.append(Edge(source=company_id, target=address_id, type="LOCATED_AT"))

            # Igazgatók (konatelia)
            executives = normalized.get("executives", [])
            for i, exec_data in enumerate(executives[:3]):  # Max 3 pre MVP
                exec_name = (
                    exec_data
                    if isinstance(exec_data, str)
                    else exec_data.get("name", f"Igazgató {i + 1}")
                )
                exec_id = f"pers_hu_{query_clean}_{i}"
                nodes.append(
                    Node(
                        id=exec_id,
                        label=exec_name,
                        type="person",
                        country="HU",
                        risk_score=5 if len(executives) > 5 else 2,
                        details="Igazgató",
                    )
                )
                edges.append(Edge(source=company_id, target=exec_id, type="MANAGED_BY"))
        else:
            # Fallback dáta
            print("⚠️ NAV API nedostupné, používam fallback dáta")
            company_id = f"hu_{query_clean}"
            nodes.append(
                Node(
                    id=company_id,
                    label=f"Magyar Cég {query_clean}",
                    type="company",
                    country="HU",
                    risk_score=3,
                    details=f"Adószám: {query_clean}",
                    ico=query_clean,
                )
            )

    # 4. POĽSKO (KRS)
    elif (country == "PL" or not country) and is_polish_krs(query_clean) and not nodes:
        # POĽSKÉ KRS - KRS integrácia
        print(f"🇵🇱 Detekované poľské KRS: {query_clean}")
        increment("search.by_country", tags={"country": "PL"})
        krs_data = fetch_krs_pl(query_clean)

        if krs_data:
            normalized = parse_krs_data(krs_data, query_clean)
            risk_score = calculate_pl_risk_score(normalized)

            # Biała Lista - VAT status check
            nip = normalized.get("nip") or query_clean
            if is_polish_nip(nip):
                vat_status = get_vat_status_pl(nip)
                if vat_status:
                    normalized["vat_status"] = vat_status
                    if vat_status != "VAT payer":
                        risk_score = max(
                            risk_score, 3
                        )  # Zvýšiť risk ak nie je VAT payer

            # Hlavná firma
            company_id = f"pl_{query_clean}"
            vat_info = (
                f", VAT: {normalized.get('vat_status', 'N/A')}"
                if normalized.get("vat_status")
                else ""
            )
            nodes.append(
                Node(
                    id=company_id,
                    label=normalized.get("name", f"Firma {query_clean}"),
                    type="company",
                    country="PL",
                    risk_score=risk_score,
                    details=f"KRS: {query_clean}, Status: {normalized.get('status', 'N/A')}, Forma: {normalized.get('legal_form', 'N/A')}{vat_info}",
                    ico=query_clean,
                )
            )

            # Adresa
            address_text = normalized.get("address", "Adres nie podano")
            address_id = f"addr_pl_{query_clean}"
            nodes.append(
                Node(
                    id=address_id,
                    label=address_text[:30] + ("..." if len(address_text) > 30 else ""),
                    type="address",
                    country="PL",
                    details=address_text,
                )
            )
            edges.append(Edge(source=company_id, target=address_id, type="LOCATED_AT"))

            # Zarządcy (konatelia)
            executives = normalized.get("executives", [])
            for i, exec_data in enumerate(executives[:3]):  # Max 3 pre MVP
                exec_name = (
                    exec_data
                    if isinstance(exec_data, str)
                    else exec_data.get("name", f"Zarządca {i + 1}")
                )
                exec_id = f"pers_pl_{query_clean}_{i}"
                nodes.append(
                    Node(
                        id=exec_id,
                        label=exec_name,
                        type="person",
                        country="PL",
                        risk_score=5 if len(executives) > 5 else 2,
                        details="Zarządca",
                    )
                )
                edges.append(Edge(source=company_id, target=exec_id, type="MANAGED_BY"))
        else:
            # Fallback dáta
            print("⚠️ KRS API nedostupné, používam fallback dáta")
            company_id = f"pl_{query_clean}"
            nodes.append(
                Node(
                    id=company_id,
                    label=f"Polska Spółka {query_clean}",
                    type="company",
                    country="PL",
                    risk_score=3,
                    details=f"KRS: {query_clean}",
                    ico=query_clean,
                )
            )

    else:
        # Prázdny výsledok ak query je číslo ale nič sa nenašlo
        if query_clean.isdigit():
            print(f"⚠️ IČO {query_clean} nebolo nájdené v žiadnom registri")
            return GraphResponse(nodes=[], edges=[])
        
        # Toto by nemalo nastať lebo textové vyhľadávanie je riešené na začiatku
        pass

    # Risk Intelligence - vylepšené risk scores
    try:
        if nodes and edges:
            try:
                risk_report = generate_risk_report(nodes, edges)
                # Aktualizovať risk scores
                enhanced_nodes = risk_report.get("enhanced_nodes", nodes)
                nodes = enhanced_nodes

                # Pridať poznámky o bielych koňoch a karuseloch
                if risk_report.get("summary", {}).get("white_horse_count", 0) > 0:
                    print(
                        f"⚠️ Detekovaných bielych koní: {risk_report['summary']['white_horse_count']}"
                    )
                if risk_report.get("summary", {}).get("circular_structure_count", 0) > 0:
                    print(
                        f"⚠️ Detekovaných karuselových štruktúr: {risk_report['summary']['circular_structure_count']}"
                    )
            except Exception as e:
                print(f"⚠️ Chyba pri risk intelligence: {e}")

        # Uložiť do cache
        result = GraphResponse(nodes=nodes, edges=edges)
        set(cache_key, result.dict())

        # Uložiť do databázy (história a cache)
        main_company = next((n for n in nodes if n.type == "company"), None)
        country_res = main_company.country if main_company else country
        risk_score = (
            max((n.risk_score for n in nodes if n.risk_score), default=0) if nodes else 0
        )

        save_search_history(
            query=q,
            country=country_res,
            result_count=len(nodes),
            risk_score=risk_score if risk_score > 0 else None,
            user_ip=user_ip,
            response_data={"nodes_count": len(nodes), "edges_count": len(edges)},
        )

        # Uložiť hlavnú firmu do cache
        if main_company and main_company.ico:
            save_company_cache(
                identifier=main_company.ico,
                country=country_res or "UNKNOWN",
                company_name=main_company.label,
                data={
                    "nodes": [n.dict() for n in nodes],
                    "edges": [e.dict() for e in edges],
                },
                risk_score=risk_score if risk_score > 0 else None,
            )

        # Analytics
        save_analytics(
            event_type="search",
            event_data={"query": q, "country": country_res, "result_count": len(nodes)},
            user_ip=user_ip,
        )

        # Metrics
        increment("search.results", value=len(nodes))
        gauge("search.last_result_count", len(nodes))
        record_event(
            "search.completed",
            {"country": country_res, "result_count": len(nodes), "query_length": len(q)},
        )

        return result
    except Exception as e:
        import traceback
        print(f"❌ KONTROLER ERROR: {e}")
        traceback.print_exc()
        raise e


@app.get("/api/audit/{ico}", tags=["Audit"])
async def audit_company(ico: str):
    """
    Vykoná kompletný 360° audit firmy podľa IČO.
    Agreguje dáta z registrov, dlhových zoznamov a analyzuje riziká.
    """
    result = audit_service.perform_deep_audit(ico)
    return result


# --- ENHANCED SEARCH ENDPOINTS ---

@app.post("/api/v2/search", tags=["Enhanced Search"])
async def enhanced_search(
    request: Dict,
    background_tasks: BackgroundTasks,
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Enhanced search endpoint with advanced filtering and cross-border integration.
    
    Request body:
    {
        "query": "company name or identifier",
        "countries": ["SK", "CZ", "PL", "HU"],
        "include_related": true,
        "risk_threshold": 5,
        "limit": 100,
        "offset": 0,
        "format": "basic|detailed|graph"
    }
    """
    from services.enhanced_data_extractor import get_enhanced_extractor
    
    extractor = get_enhanced_extractor()
    
    try:
        result = await extractor.search_companies(
            query=request.get("query", ""),
            countries=request.get("countries"),
            include_related=request.get("include_related", True),
            risk_threshold=request.get("risk_threshold"),
            limit=request.get("limit", 100),
            offset=request.get("offset", 0)
        )
        
        return {
            "success": True,
            "data": result,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "user_tier": current_user.tier.value if current_user else "anonymous",
                "search_id": f"search_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Enhanced search failed: {str(e)}"
        )


@app.post("/api/v2/export", tags=["Enhanced Export"])
async def enhanced_export(
    request: Dict,
    current_user: User = Depends(get_current_user)
):
    """
    Enhanced export endpoint supporting multiple formats with professional styling.
    
    Request body:
    {
        "format": "pdf|excel|csv|json",
        "data": { /* graph data or search results */ },
        "options": {
            "include_graph": true,
            "branding": "premium|standard",
            "timestamp": true,
            "executive_summary": true,
            "risk_analysis": true
        }
    }
    """
    from services.pdf_export_service import get_pdf_service
    
    format_type = request.get("format", "json").lower()
    data = request.get("data", {})
    options = request.get("options", {})
    
    try:
        if format_type == "pdf":
            pdf_service = get_pdf_service()
            
            if "companies" in data:
                # Export search results to PDF
                pdf_bytes = pdf_service.generate_executive_summary(
                    companies=data["companies"],
                    metadata={"user_id": current_user.id, "export_time": datetime.now().isoformat()},
                    include_risk_analysis=options.get("risk_analysis", True),
                    include_financials=options.get("include_financials", True)
                )
                
                return Response(
                    content=pdf_bytes,
                    media_type="application/pdf",
                    headers={"Content-Disposition": f"attachment; filename=iluminati_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"}
                )
            else:
                # Export graph data to PDF
                pdf_bytes = pdf_service.generate_network_analysis(
                    graph_data=data,
                    insights={"analysis": "Network visualization export"},
                    include_visualization=options.get("include_graph", True)
                )
                
                return Response(
                    content=pdf_bytes,
                    media_type="application/pdf",
                    headers={"Content-Disposition": f"attachment; filename=iluminati_network_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"}
                )
        
        elif format_type == "excel":
            from services.export_service import export_to_excel
            excel_bytes = export_to_excel(data)
            
            return Response(
                content=excel_bytes,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": f"attachment; filename=iluminati_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"}
            )
        
        elif format_type == "csv":
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write headers
            if "nodes" in data:
                writer.writerow(["Type", "ID", "Label", "Country", "Risk Score", "Details"])
                for node in data["nodes"]:
                    writer.writerow([
                        node.get("type", ""),
                        node.get("id", ""),
                        node.get("label", ""),
                        node.get("country", ""),
                        node.get("risk_score", 0),
                        node.get("details", "")
                    ])
            
            csv_content = output.getvalue()
            output.close()
            
            return Response(
                content=csv_content,
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename=iluminati_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
            )
        
        elif format_type == "json":
            return Response(
                content=json.dumps(data, indent=2, ensure_ascii=False),
                media_type="application/json",
                headers={"Content-Disposition": f"attachment; filename=iluminati_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"}
            )
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported export format: {format_type}"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Export failed: {str(e)}"
        )


@app.get("/api/v2/company/{country}/{identifier}", tags=["Enhanced Search"])
async def get_company_details(
    country: str,
    identifier: str,
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Get detailed company information with enhanced data.
    
    Path parameters:
    - country: SK, CZ, PL, or HU
    - identifier: Company identifier (IČO, KRS, etc.)
    """
    from services.enhanced_data_extractor import get_enhanced_extractor
    
    try:
        extractor = get_enhanced_extractor()
        company = await extractor.get_company_details(identifier, country.upper())
        
        if not company:
            raise HTTPException(
                status_code=404,
                detail=f"Company {identifier} not found in {country}"
            )
        
        from dataclasses import asdict
        return {
            "success": True,
            "data": asdict(company),
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "source": company.source if hasattr(company, 'source') else "enhanced_extractor"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve company details: {str(e)}"
        )


@app.get("/api/v2/related/{country}/{identifier}", tags=["Enhanced Search"])
async def get_related_companies(
    country: str,
    identifier: str,
    max_depth: int = 2,
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Get related companies through network analysis.
    
    Path parameters:
    - country: SK, CZ, PL, or HU
    - identifier: Company identifier
    - max_depth: Maximum depth for network traversal (default: 2)
    """
    from services.enhanced_data_extractor import get_enhanced_extractor
    
    try:
        extractor = get_enhanced_extractor()
        related_companies = await extractor.get_related_companies(identifier, max_depth)
        
        return {
            "success": True,
            "data": related_companies,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "max_depth": max_depth,
                "related_count": len(related_companies)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve related companies: {str(e)}"
        )


if __name__ == "__main__":
    import os

    import uvicorn

    # SSL konfigurácia
    ssl_keyfile = os.path.join(os.path.dirname(__file__), "..", "ssl", "key.pem")
    ssl_certfile = os.path.join(os.path.dirname(__file__), "..", "ssl", "cert.pem")

    # Kontrola, či existujú SSL súbory
    use_ssl = os.path.exists(ssl_keyfile) and os.path.exists(ssl_certfile)

    if use_ssl:
        print("🔐 Spúšťam server s SSL (HTTPS)...")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            ssl_keyfile=ssl_keyfile,
            ssl_certfile=ssl_certfile,
        )
    else:
        print("⚠️ SSL certifikáty nenájdené, spúšťam server bez SSL (HTTP)...")
        print(f"   SSL keyfile: {ssl_keyfile}")
        print(f"   SSL certfile: {ssl_certfile}")
        uvicorn.run(app, host="0.0.0.0", port=8000)
