"""
Enhanced Data Extraction Service for ILUMINATI SYSTEM
Multi-layer caching strategy with cross-border register integration
"""

import asyncio
import logging
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict
from enum import Enum
from functools import lru_cache

import aiohttp
from bs4 import BeautifulSoup
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert

from services.cache import get_cache_key, set_cache, get_cache
from services.database import get_db_session, CompanyCache
from services.export_service import export_to_excel
from services.sk_orsr_provider import get_orsr_provider
from services.hu_nav import get_nav_provider
from services.pl_krs import get_krs_provider
from services.pl_ceidg import get_ceidg_provider
from services.pl_biala_lista import get_biala_lista_provider

logger = logging.getLogger(__name__)

class CountryCode(str, Enum):
    SK = "SK"
    CZ = "CZ"
    PL = "PL"
    HU = "HU"

class DataQuality(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"

class RelationshipType(str, Enum):
    OWNED_BY = "OWNED_BY"
    MANAGED_BY = "MANAGED_BY"
    LOCATED_AT = "LOCATED_AT"
    HAS_DEBT = "HAS_DEBT"
    RELATED_TO = "RELATED_TO"

@dataclass
class EnhancedCompanyData:
    identifier: str
    name: str
    country: CountryCode
    address: str
    postal_code: str
    city: str
    region: str
    district: str
    legal_form: str
    executives: List[str]
    shareholders: List[str]
    founded: str
    status: str
    dic: str
    ic_dph: str
    risk_score: float
    financial_data: Optional[Dict]
    virtual_seat: bool
    source: str
    last_updated: str
    data_quality: DataQuality
    related_companies: List[str]
    country_specific_data: Dict[str, Any]

@dataclass
class RelationshipData:
    source_id: str
    target_id: str
    type: RelationshipType
    weight: float
    confidence: float
    source: str
    verified: bool
    cross_border: bool
    countries_involved: List[CountryCode]

class EnhancedDataExtractor:
    """
    Enhanced data extraction with multi-layer caching and cross-border integration.
    Implements a 3-tier caching strategy: Hot (Redis), Warm (Database), Cold (Live).
    """
    
    def __init__(self):
        self.redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.session = aiohttp.ClientSession()
        self.cache_ttls = {
            'hot': timedelta(hours=12),    # Redis cache
            'warm': timedelta(days=7),     # Database cache
            'cold': timedelta(days=30)     # Live scraping minimum interval
        }
        
        # Initialize providers
        self.providers = {
            CountryCode.SK: get_orsr_provider(),
            CountryCode.CZ: None,  # Will be initialized on demand
            CountryCode.PL: None,  # Will be initialized on demand
            CountryCode.HU: None,  # Will be initialized on demand
        }

    def _get_stable_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate a stable MD5 cache key instead of using non-deterministic hash()."""
        data = {
            "prefix": prefix,
            "args": args,
            "kwargs": {k: v for k, v in sorted(kwargs.items())}
        }
        # Convert enums to values for serialization
        def enum_to_str(obj):
            if isinstance(obj, Enum):
                return obj.value
            if isinstance(obj, list):
                return [enum_to_str(x) for x in obj]
            return obj
            
        stable_json = json.dumps(enum_to_str(data), sort_keys=True)
        return f"{prefix}_{hashlib.md5(stable_json.encode()).hexdigest()}"
    
    async def search_companies(
        self, 
        query: str, 
        countries: Optional[List[CountryCode]] = None,
        include_related: bool = True,
        risk_threshold: Optional[float] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Enhanced search across multiple countries with intelligent caching.
        
        Args:
            query: Search query (company name or identifier)
            countries: List of countries to search in
            include_related: Include related companies in results
            risk_threshold: Filter by minimum risk score
            limit: Maximum number of results
            offset: Pagination offset
            
        Returns:
            Dict with search results and metadata
        """
        if not countries:
            countries = [CountryCode.SK, CountryCode.CZ, CountryCode.PL, CountryCode.HU]
        
        # Normalize countries to Enums if they are strings
        normalized_countries = []
        for c in countries:
            if isinstance(c, str):
                try:
                    normalized_countries.append(CountryCode(c.upper()))
                except ValueError:
                    logger.warning(f"Invalid country code: {c}")
            else:
                normalized_countries.append(c)
        countries = normalized_countries

        logger.info(f"Searching for '{query}' in countries: {[c.value for c in countries]}")
        
        cache_key = self._get_stable_cache_key("search_combined", query, countries, limit, offset, risk_threshold)
        
        # Search result cache check
        try:
            cached_search = get_cache(cache_key)
            if cached_search:
                logger.info(f"Global cache hit for search: {query}")
                return cached_search
        except Exception as e:
            logger.warning(f"Combined cache lookup failed: {e}")

        # 1. Parallel search by country
        tasks = []
        for country in countries:
            tasks.append(self._search_by_country(query, country))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten and filter results
        all_companies = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Search failed for {countries[i].value if i < len(countries) else 'unknown'}: {result}")
                continue
            if result:
                all_companies.extend(result)
        
        # Apply filters
        if risk_threshold is not None:
            all_companies = [c for c in all_companies if c.risk_score >= risk_threshold]
        
        # Sort by risk score and data quality
        all_companies.sort(key=lambda x: (x.risk_score, x.data_quality.value), reverse=True)
        
        # Apply pagination
        total = len(all_companies)
        paginated_companies = all_companies[offset:offset + limit]
        
        # Convert to dict for caching
        companies_dict = [asdict(company) for company in paginated_companies]
        
        # Create result with metadata
        result = {
            "companies": companies_dict,
            "total": total,
            "facets": self._calculate_facets(all_companies),
            "suggestions": self._generate_suggestions(query, all_companies),
            "execution_time": datetime.now().isoformat(),
            "cache_hit": False,
            "search_params": {
                "query": query,
                "countries": [c.value for c in countries],
                "include_related": include_related,
                "risk_threshold": risk_threshold,
                "limit": limit,
                "offset": offset
            }
        }
        
        # Cache result
        set_cache(cache_key, result, ttl=self.cache_ttls['warm'])
        
        logger.info(f"Search completed: {len(paginated_companies)} results from {total} total")
        return result
    
    async def _search_by_country(self, query: str, country: CountryCode) -> List[EnhancedCompanyData]:
        """Search companies in specific country."""
        # Ensure country is a CountryCode enum
        if isinstance(country, str):
            country = CountryCode(country.upper())
            
        cache_key = self._get_stable_cache_key("search", country.value, query)
        
        # Check cache first
        try:
            cached = get_cache(cache_key)
            if cached:
                logger.debug(f"Cache hit for {country.value}: {query}")
                return [EnhancedCompanyData(**company) for company in cached]
        except Exception as e:
            logger.warning(f"Cache hit failed for {country.value}: {e}")
        
        # Try database
        try:
            companies = await self._search_in_database(query, country)
            if companies:
                logger.debug(f"Database hit for {country.value}: {query}")
                try:
                    set_cache(cache_key, [asdict(c) for c in companies], ttl=self.cache_ttls['warm'])
                except Exception as ce:
                    logger.warning(f"Failed to set cache (DB hit): {ce}")
                return companies
        except Exception as e:
            logger.error(f"Database search failed for {country.value}: {e}")
        
        # Live scraping
        logger.info(f"Live scraping for {country.value}: {query}")
        companies = await self._live_scraping(query, country)
        if companies:
            set_cache(cache_key, [asdict(c) for c in companies], ttl=self.cache_ttls['cold'])
            await self._save_to_database(companies)
        
        return companies
    
    async def _live_scraping(self, query: str, country: CountryCode) -> List[EnhancedCompanyData]:
        """Perform live scraping for specific country."""
        try:
            if country == CountryCode.SK:
                return await self._scrape_orsr(query)
            elif country == CountryCode.CZ:
                return await self._scrape_ares(query)
            elif country == CountryCode.PL:
                return await self._scrape_poland(query)
            elif country == CountryCode.HU:
                return await self._scrape_nav(query)
            return []
        except Exception as e:
            logger.error(f"Live scraping failed for {country.value}: {e}")
            return []
    
    async def _scrape_orsr(self, query: str) -> List[EnhancedCompanyData]:
        """Enhanced ORSR scraping with improved error handling."""
        try:
            cache_key = self._get_stable_cache_key("orsr_live", query)
            # Check cache
            try:
                cached = get_cache(cache_key)
                if cached:
                    return [EnhancedCompanyData(**company) for company in cached]
            except Exception as e:
                logger.warning(f"ORSR cache lookup failed: {e}")
            
            provider = self.providers[CountryCode.SK]
            # provider.lookup_by_ico is NOT async, don't await it
            result = provider.lookup_by_ico(query)
            
            if result:
                company = EnhancedCompanyData(
                    identifier=result.get("ico", ""),
                    name=result.get("name", ""),
                    country=CountryCode.SK,
                    address=result.get("address", ""),
                    postal_code=result.get("postal_code", ""),
                    city=result.get("city", ""),
                    region=result.get("region", ""),
                    district=result.get("district", ""),
                    legal_form=result.get("legal_form", ""),
                    executives=result.get("executives", []),
                    shareholders=result.get("shareholders", []),
                    founded=result.get("founded", ""),
                    status=result.get("status", "Aktívna"),
                    dic=result.get("dic", ""),
                    ic_dph=result.get("ic_dph", ""),
                    risk_score=result.get("risk_score", 0.0),
                    financial_data=result.get("financial_data"),
                    virtual_seat=result.get("virtual_seat", False),
                    source="ORSR",
                    last_updated=datetime.now().isoformat(),
                    data_quality=DataQuality.GOOD,
                    related_companies=[],
                    country_specific_data=result
                )
                # save to database and cache
                set_cache(cache_key, asdict(company), ttl=self.cache_ttls['cold'])
                # _save_to_database is async, so we keep the await there
                await self._save_to_database([company])
                return [company]
            return []
        except Exception as e:
            logger.error(f"ORSR scraping failed: {e}")
            return []
    
    async def _scrape_ares(self, query: str) -> List[EnhancedCompanyData]:
        """Enhanced ARES scraping."""
        try:
            # This would integrate with existing ARES provider
            # For now, return empty list as placeholder
            logger.info(f"ARES scraping for: {query}")
            return []
        except Exception as e:
            logger.error(f"ARES scraping failed: {e}")
            return []
    
    async def _scrape_poland(self, query: str) -> List[EnhancedCompanyData]:
        """Enhanced Poland scraping (KRS + CEIDG + Biała Lista)."""
        try:
            companies = []
            
            # Try KRS first
            krs_provider = get_krs_provider()
            fetch_krs = krs_provider.get("fetch_function")
            if fetch_krs:
                krs_result = fetch_krs(query) # Synchronous
                if krs_result:
                    companies.append(self._convert_to_enhanced_company(krs_result, CountryCode.PL, "KRS"))
            
            # Try CEIDG
            ceidg_provider = get_ceidg_provider()
            fetch_ceidg = ceidg_provider.get("fetch_function")
            if fetch_ceidg:
                ceidg_result = fetch_ceidg(query) # Synchronous
                if ceidg_result:
                    companies.append(self._convert_to_enhanced_company(ceidg_result, CountryCode.PL, "CEIDG"))
            
            return companies
        except Exception as e:
            logger.error(f"Poland scraping failed: {e}")
            return []
    
    async def _scrape_nav(self, query: str) -> List[EnhancedCompanyData]:
        """Enhanced NAV scraping."""
        try:
            provider = get_nav_provider()
            fetch_nav = provider.get("fetch_function")
            if fetch_nav:
                result = fetch_nav(query) # Synchronous
                if result:
                    company = self._convert_to_enhanced_company(result, CountryCode.HU, "NAV")
                    return [company]
            return []
        except Exception as e:
            logger.error(f"NAV scraping failed: {e}")
            return []
    
    def _convert_to_enhanced_company(self, data: Dict, country: CountryCode, source: str) -> EnhancedCompanyData:
        """Convert provider data to EnhancedCompanyData format."""
        return EnhancedCompanyData(
            identifier=data.get("identifier", ""),
            name=data.get("name", ""),
            country=country,
            address=data.get("address", ""),
            postal_code=data.get("postal_code", ""),
            city=data.get("city", ""),
            region=data.get("region", ""),
            district=data.get("district", ""),
            legal_form=data.get("legal_form", ""),
            executives=data.get("executives", []),
            shareholders=data.get("shareholders", []),
            founded=data.get("founded", ""),
            status=data.get("status", "Active"),
            dic=data.get("dic", ""),
            ic_dph=data.get("ic_dph", ""),
            risk_score=data.get("risk_score", 0.0),
            financial_data=data.get("financial_data"),
            virtual_seat=data.get("virtual_seat", False),
            source=source,
            last_updated=datetime.now().isoformat(),
            data_quality=DataQuality.GOOD,
            related_companies=[],
            country_specific_data=data
        )
    
    async def _search_in_database(self, query: str, country: CountryCode) -> List[EnhancedCompanyData]:
        """Search companies in database."""
        try:
            # get_db_session is synchronous, so use it with a standard 'with' block
            with get_db_session() as db:
                if not db:
                    return []
                    
                # Search by name or identifier
                search_pattern = f"%{query}%"
                
                # Use synchronous sqlalchemy query
                result = db.query(CompanyCache).filter(
                    (CompanyCache.country == country.value) &
                    (
                        (CompanyCache.company_name.ilike(search_pattern)) |
                        (CompanyCache.identifier.ilike(search_pattern))
                    )
                ).limit(50).all()
                
                companies = []
                for row in result:
                    if row.company_data:
                        try:
                            # Reconstruct dictionary from JSON column if needed, but anddict handles it
                            company_data = row.company_data
                            if isinstance(company_data, str):
                                company_data = json.loads(company_data)
                            
                            company = EnhancedCompanyData(**company_data)
                            companies.append(company)
                        except Exception as e:
                            logger.error(f"Error parsing company data from DB for {row.identifier}: {e}")
                
                return companies
        except Exception as e:
            logger.error(f"Database search failed: {e}")
            return []
    
    async def _save_to_database(self, companies: List[EnhancedCompanyData]):
        """Save companies to database with enhanced metadata."""
        try:
            with get_db_session() as db:
                if not db:
                    return
                    
                for company in companies:
                    # Check if company already exists
                    existing_company = db.query(CompanyCache).filter(
                        (CompanyCache.identifier == company.identifier) &
                        (CompanyCache.country == company.country.value)
                    ).first()
                    
                    if existing_company:
                        # Update existing
                        existing_company.company_data = asdict(company)
                        existing_company.data_quality = company.data_quality.value
                        existing_company.last_synced_at = datetime.utcnow()
                        existing_company.source = company.source
                        existing_company.company_name = company.name
                    else:
                        # Create new
                        new_company = CompanyCache(
                            identifier=company.identifier,
                            country=company.country.value,
                            company_data=asdict(company),
                            company_name=company.name,
                            data_quality=company.data_quality.value,
                            last_synced_at=datetime.utcnow(),
                            source=company.source
                        )
                        db.add(new_company)
                
                db.commit()
                logger.info(f"Saved {len(companies)} companies to database")
        except Exception as e:
            logger.error(f"Database save failed: {e}")
            # db.rollback() is handled by contextmanager
    
    def _calculate_facets(self, companies: List[EnhancedCompanyData]) -> Dict[str, Any]:
        """Calculate search facets for filtering."""
        facets = {
            "countries": {},
            "legal_forms": {},
            "risk_scores": {
                "min": 0,
                "max": 10,
                "avg": 0
            },
            "data_quality": {}
        }
        
        if not companies:
            return facets
        
        # Country facets
        for company in companies:
            country = company.country.value
            facets["countries"][country] = facets["countries"].get(country, 0) + 1
        
        # Legal form facets
        for company in companies:
            legal_form = company.legal_form or "Unknown"
            facets["legal_forms"][legal_form] = facets["legal_forms"].get(legal_form, 0) + 1
        
        # Risk score statistics
        risk_scores = [c.risk_score for c in companies if c.risk_score is not None]
        if risk_scores:
            facets["risk_scores"]["min"] = min(risk_scores)
            facets["risk_scores"]["max"] = max(risk_scores)
            facets["risk_scores"]["avg"] = round(sum(risk_scores) / len(risk_scores), 2)
        
        # Data quality facets
        for company in companies:
            quality = company.data_quality.value
            facets["data_quality"][quality] = facets["data_quality"].get(quality, 0) + 1
        
        return facets
    
    def _generate_suggestions(self, query: str, companies: List[EnhancedCompanyData]) -> List[str]:
        """Generate search suggestions based on results."""
        suggestions = set()
        
        # Add company names that contain the query
        for company in companies:
            if query.lower() in company.name.lower():
                suggestions.add(company.name)
        
        # Return top 5 suggestions
        return list(suggestions)[:5]
    
    async def get_company_details(self, identifier: str, country: Union[str, CountryCode]) -> Optional[EnhancedCompanyData]:
        """Get detailed company information."""
        # Normalize country to enum
        if isinstance(country, str):
            try:
                country = CountryCode(country.upper())
            except ValueError:
                logger.error(f"Invalid country code: {country}")
                return None
                
        cache_key = self._get_stable_cache_key("company_details", country.value, identifier)
        
        # Check cache
        try:
            cached = get_cache(cache_key)
            if cached:
                return EnhancedCompanyData(**cached)
        except Exception as e:
            logger.warning(f"Failed to get from cache: {e}")
        
        # Try database
        try:
            with get_db_session() as db:
                if db:
                    company_row = db.query(CompanyCache).filter(
                        (CompanyCache.identifier == identifier) &
                        (CompanyCache.country == country.value)
                    ).first()
                    
                    if company_row and company_row.company_data:
                        try:
                            # Parse JSON if it's a string
                            company_data = company_row.company_data
                            if isinstance(company_data, str):
                                company_data = json.loads(company_data)
                                
                            company = EnhancedCompanyData(**company_data)
                            # Update cache in background
                            set_cache(cache_key, asdict(company), ttl=self.cache_ttls['warm'])
                            return company
                        except Exception as e:
                            logger.error(f"Error parsing cached company data: {e}")
        except Exception as e:
            logger.error(f"Database lookup failed: {e}")
        
        # Live lookup - providers are currently synchronous
        if country == CountryCode.SK:
            try:
                provider = self.providers[CountryCode.SK]
                # provider.lookup_by_ico is synchronous
                result = provider.lookup_by_ico(identifier)
                if result:
                    company = self._convert_to_enhanced_company(result, country, "ORSR")
                    # Update cache and DB
                    set_cache(cache_key, asdict(company), ttl=self.cache_ttls['cold'])
                    await self._save_to_database([company])
                    return company
            except Exception as e:
                logger.error(f"Live lookup (SK) failed: {e}")
        
        return None
    
    async def get_related_companies(self, company_id: str, max_depth: int = 2) -> List[EnhancedCompanyData]:
        """Get related companies through network analysis."""
        # This would implement graph traversal logic
        # For now, return empty list as placeholder
        return []
    
    async def export_search_results(
        self, 
        companies: List[Dict], 
        format: str = "excel",
        include_graph: bool = False
    ) -> bytes:
        """Export search results to various formats."""
        if format.lower() == "excel":
            return export_to_excel({"nodes": companies, "edges": []})
        elif format.lower() == "csv":
            # Implement CSV export
            pass
        elif format.lower() == "json":
            # Implement JSON export
            pass
        else:
            raise ValueError(f"Unsupported export format: {format}")

# Global instance
_enhanced_extractor = None

def get_enhanced_extractor() -> EnhancedDataExtractor:
    """Get singleton instance of EnhancedDataExtractor."""
    global _enhanced_extractor
    if _enhanced_extractor is None:
        _enhanced_extractor = EnhancedDataExtractor()
    return _enhanced_extractor