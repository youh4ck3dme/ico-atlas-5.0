/**
 * ORSR Lookup Service - Uses ILUMINATI Backend API v2
 * Backend running at http://localhost:8000
 * 
 * API Endpoints:
 * - POST /api/v2/search - Enhanced search with countries filter
 * - GET /api/v2/company/{country}/{ico} - Company details
 * - GET /api/search?q={query}&country={country} - Legacy search
 */

const API_BASE = 'http://localhost:8000';
const DEMO_USER = {
    username: 'test_automation@example.com',
    password: 'TestPassword123!'
};

/**
 * Get valid auth token (from storage or auto-login)
 */
const getAuthToken = async () => {
    // 1. Try local storage
    let token = localStorage.getItem('access_token');

    // Validate token expiry (simple check)
    if (token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            if (payload.exp * 1000 > Date.now()) {
                return token;
            }
        } catch (e) {
            // Invalid token format, proceed to re-authenticate
            console.warn('Invalid token in localStorage, re-authenticating.');
        }
    }

    // 2. Auto-login fallback for seamless demo
    try {
        console.log('Authenticating as demo user...');

        // Try to register first (silently ignore if exists)
        try {
            await fetch(`${API_BASE}/api/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: DEMO_USER.username,
                    password: DEMO_USER.password,
                    full_name: 'Frontend Automation User'
                })
            });
        } catch (e) {
            // User likely exists, proceed to login
        }

        // Login
        const response = await fetch(`${API_BASE}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(DEMO_USER)
        });

        if (response.ok) {
            const data = await response.json();
            token = data.access_token;
            localStorage.setItem('access_token', token);
            return token;
        }
    } catch (e) {
        console.error('Demo auth failed:', e);
    }
    return null;
};

/**
 * Format IČO with leading zeros if needed
 */
export const formatIco = (ico) => {
    const cleaned = ico.replace(/\s/g, '').replace(/\D/g, '');
    return cleaned.padStart(8, '0');
};

/**
 * Validate IČO format
 */
export const isValidIco = (ico) => {
    const cleaned = ico.replace(/\s/g, '').replace(/\D/g, '');
    return cleaned.length >= 6 && cleaned.length <= 8;
};

/**
 * Enhanced search using v2 API
 * Supports: SK (ORSR, ZRSR, RUZ), CZ (ARES), PL (KRS), HU (NAV)
 */
export const searchCompanies = async (query, countries = ['SK']) => {
    try {
        const token = await getAuthToken();
        const headers = {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        };

        // Try v2 API first
        const response = await fetch(`${API_BASE}/api/v2/search`, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                query: query,
                countries: countries,
                include_related: true,
                risk_threshold: 0,
                limit: 10,
                format: 'detailed'
            })
        });

        if (response.ok) {
            const data = await response.json();
            return transformV2Response(data);
        }

        // Fallback to legacy API
        return await searchCompaniesLegacy(query, countries[0] || 'SK');
    } catch (error) {
        console.error('Search API error:', error);
        // Try legacy as fallback
        return await searchCompaniesLegacy(query, countries[0] || 'SK');
    }
};

/**
 * Legacy search (fallback)
 */
const searchCompaniesLegacy = async (query, country = 'SK') => {
    try {
        // Request graph=1 to get full relations (Illuminati Graph Service)
        const response = await fetch(`${API_BASE}/api/search?q=${encodeURIComponent(query)}&country=${country}&graph=1`);

        if (!response.ok) return null;

        const data = await response.json();
        return transformLegacyResponse(data);
    } catch (error) {
        console.error('Legacy search error:', error);
        return null;
    }
};

/**
 * Transform company by IČO lookup
 */
export const lookupByIco = async (ico, country = 'SK') => {
    // ... (unchanged, just context for match)
    const formattedIco = formatIco(ico);
    // ...
};

/**
 * Transform v2 API response
 */
const transformV2Response = (data) => {
    // ... (unchanged)
};

/**
 * Transform legacy API response
 */
const transformLegacyResponse = (data) => {
    // 1. Check for backend GraphResponse (Illuminati V1)
    if (data && data.nodes && data.edges) {
        // Extract main company from nodes for company list view if needed
        const companies = data.nodes
            .filter(n => n.type === 'company' && n.ico) // Filter only valid company nodes
            .map(node => ({
                ico: node.ico,
                name: node.label,
                address: node.details, // Address is often in details or linked node
                // Map other fields as best effort
                status: 'Aktívna',
                country: node.country || 'SK'
            }));

        return {
            companies: companies, // Fallback list
            graphData: { nodes: data.nodes, edges: data.edges },
            facets: {},
            total: companies.length
        };
    }

    // 2. Fallback to old structure
    let companies = [];

    if (Array.isArray(data)) {
        companies = data;
    } else if (data.companies) {
        companies = data.companies;
    } else if (data.results) {
        companies = data.results;
    } else if (data.data) {
        companies = Array.isArray(data.data) ? data.data : [data.data];
    } else if (data.ico || data.identifier) {
        companies = [data];
    }

    return {
        companies: companies.map(transformApiCompany),
        graphData: null,
        facets: {},
        total: companies.length
    };
};

/**
 * Transform API company to unified format
 * Maps all possible field names from different API versions
 */
const transformApiCompany = (data) => {
    if (!data) return null;

    return {
        // Identifiers
        ico: data.ico || data.identifier || '',
        dic: data.dic || '',
        icDph: data.ic_dph || data.icdph || data.icDph || '',

        // Basic info
        name: data.name || data.nazov || data.obchodne_meno || 'Neznáma firma',
        legalForm: data.legal_form || data.pravna_forma || data.legalForm || '',
        status: data.status || data.stav || 'Aktívna',
        founded: data.founded || data.datum_zalozenia || data.datumVzniku || '',

        // Address
        address: data.address || data.adresa || data.sidlo || '',
        city: data.city || data.mesto || '',
        postalCode: data.postal_code || data.psc || '',
        region: data.region || '',
        district: data.district || '',
        country: data.country || 'SK',

        // People
        executives: data.executives || data.konatelia || data.statutarny_organ || [],
        shareholders: data.shareholders || data.spolocnici || [],

        // Financial
        revenue: data.revenue || data.trzby || null,
        profit: data.profit || data.zisk || null,
        employees: data.employees || data.pocet_zamestnancov || null,
        financialData: data.financial_data || data.financialData || null,

        // Risk & Quality
        riskScore: data.risk_score || data.riskScore || calculateRiskScore(data),
        virtualSeat: data.virtual_seat || data.virtualSeat || detectVirtualSeat(data.address || data.adresa || ''),
        dataQuality: data.data_quality || data.dataQuality || 'fair',

        // Relations
        relatedCompanies: data.related_companies || data.relatedCompanies || [],

        // Meta
        source: data.source || 'API',
        lastUpdated: data.last_updated || new Date().toISOString(),
        countrySpecificData: data.country_specific_data || {}
    };
};

/**
 * Calculate risk score
 */
const calculateRiskScore = (data) => {
    let score = 2;

    const status = (data.status || data.stav || '').toLowerCase();
    if (status.includes('likvidác') || status.includes('zrušen') || status.includes('konkurz')) score += 5;

    if (data.employees === 0 || data.pocet_zamestnancov === 0) score += 1;
    if (detectVirtualSeat(data.address || data.adresa || '')) score += 2;
    if (data.revenue === 0 || data.trzby === 0) score += 1;
    if ((data.profit || data.zisk || 0) < 0) score += 1;

    return Math.min(10, Math.max(0, score));
};

/**
 * Detect virtual seat
 */
const detectVirtualSeat = (address) => {
    const indicators = ['TOWER', 'BUSINESS CENTER', 'VIRTUAL', 'COWORKING', 'REGUS', 'SPACES', 'WEHUB'];
    return indicators.some(ind => (address || '').toUpperCase().includes(ind));
};

/**
 * Transform company to graph format for visualization
 */
export const companyToGraphData = (company) => {
    if (!company) return { nodes: [], edges: [] };

    const nodes = [];
    const edges = [];
    const companyId = `company-${company.ico}`;

    // Central company node with all data
    nodes.push({
        id: companyId,
        label: company.name,
        type: 'company',
        // All company fields
        ...company
    });

    // Address node
    if (company.address) {
        const addressId = `address-${company.ico}`;
        nodes.push({
            id: addressId,
            label: company.city || company.address.substring(0, 25),
            type: 'address',
            details: company.address,
            postalCode: company.postalCode,
            virtual_seat: company.virtualSeat
        });
        edges.push({ source: companyId, target: addressId, type: 'LOCATED_AT' });
    }

    // Executive nodes
    (company.executives || []).forEach((exec, i) => {
        const name = typeof exec === 'string' ? exec : (exec.meno || exec.name || `Konateľ ${i + 1}`);
        const execId = `person-exec-${i}-${company.ico}`;
        nodes.push({ id: execId, label: name, type: 'person', details: 'Konateľ' });
        edges.push({ source: companyId, target: execId, type: 'MANAGED_BY' });
    });

    // Shareholder nodes
    (company.shareholders || []).forEach((sh, i) => {
        const name = typeof sh === 'string' ? sh : (sh.meno || sh.name || `Spoločník ${i + 1}`);
        const existing = nodes.find(n => n.label === name && n.type === 'person');

        if (existing) {
            edges.push({ source: companyId, target: existing.id, type: 'OWNED_BY' });
        } else {
            const shId = `person-sh-${i}-${company.ico}`;
            nodes.push({ id: shId, label: name, type: 'person', details: 'Spoločník' });
            edges.push({ source: companyId, target: shId, type: 'OWNED_BY' });
        }
    });

    // Related companies
    (company.relatedCompanies || []).forEach((rel, i) => {
        const relName = typeof rel === 'string' ? rel : (rel.name || `Related ${i + 1}`);
        const relId = `company-related-${i}-${company.ico}`;
        nodes.push({ id: relId, label: relName, type: 'company', risk_score: 0 });
        edges.push({ source: companyId, target: relId, type: 'RELATED_TO' });
    });

    return { nodes, edges };
};

export default {
    lookupByIco,
    searchCompanies,
    formatIco,
    isValidIco,
    companyToGraphData
};
