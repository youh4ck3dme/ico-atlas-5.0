# Code Samples: Enhanced Data Extraction & Visualization Tool

## 1. Enhanced Data Extraction Service

### Backend: Multi-Layer Caching Strategy

```python
# backend/services/enhanced_data_extractor.py
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

import aiohttp
from bs4 import BeautifulSoup
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from services.cache import get_cache_key, set_cache, get_cache
from services.database import get_db_session, CompanyCache
from services.export_service import export_to_pdf, export_to_excel

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

class EnhancedDataExtractor:
    """Enhanced data extraction with multi-layer caching and cross-border integration."""
    
    def __init__(self):
        self.redis = Redis(host='localhost', port=6379, db=0)
        self.session = aiohttp.ClientSession()
        self.cache_ttls = {
            'hot': timedelta(hours=12),
            'warm': timedelta(days=7),
            'cold': timedelta(days=30)
        }
    
    async def search_companies(self, query: str, countries: List[CountryCode] = None) -> List[EnhancedCompanyData]:
        """Enhanced search across multiple countries with intelligent caching."""
        if not countries:
            countries = [CountryCode.SK, CountryCode.CZ, CountryCode.PL, CountryCode.HU]
        
        tasks = []
        for country in countries:
            tasks.append(self._search_by_country(query, country))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten and filter results
        all_companies = []
        for result in results:
            if isinstance(result, Exception):
                logging.error(f"Search failed for country: {result}")
                continue
            all_companies.extend(result)
        
        # Sort by risk score and data quality
        all_companies.sort(key=lambda x: (x.risk_score, x.data_quality.value), reverse=True)
        
        return all_companies
    
    async def _search_by_country(self, query: str, country: CountryCode) -> List[EnhancedCompanyData]:
        """Search companies in specific country."""
        cache_key = f"search_{country}_{query}"
        
        # Check cache first
        cached = await get_cache(cache_key)
        if cached:
            return cached
        
        # Try database
        companies = await self._search_in_database(query, country)
        if companies:
            await set_cache(cache_key, companies, ttl=self.cache_ttls['warm'])
            return companies
        
        # Live scraping
        companies = await self._live_scraping(query, country)
        if companies:
            await set_cache(cache_key, companies, ttl=self.cache_ttls['cold'])
            await self._save_to_database(companies)
        
        return companies
    
    async def _live_scraping(self, query: str, country: CountryCode) -> List[EnhancedCompanyData]:
        """Perform live scraping for specific country."""
        if country == CountryCode.SK:
            return await self._scrape_orsr(query)
        elif country == CountryCode.CZ:
            return await self._scrape_ares(query)
        elif country == CountryCode.PL:
            return await self._scrape_krs(query)
        elif country == CountryCode.HU:
            return await self._scrape_nav(query)
        return []
    
    async def _scrape_orsr(self, query: str) -> List[EnhancedCompanyData]:
        """Enhanced ORSR scraping with improved error handling."""
        try:
            url = f"https://www.orsr.sk/hladaj_ico.asp?ICO={query}&SID=0"
            async with self.session.get(url) as response:
                if response.status != 200:
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Parse company data
                companies = []
                # ... parsing logic with enhanced error handling
                
                return companies
        except Exception as e:
            logging.error(f"ORSR scraping failed: {e}")
            return []
    
    async def _save_to_database(self, companies: List[EnhancedCompanyData]):
        """Save companies to database with enhanced metadata."""
        async with get_db_session() as db:
            for company in companies:
                cache_entry = CompanyCache(
                    identifier=company.identifier,
                    country=company.country,
                    company_data=company.__dict__,
                    data_quality=company.data_quality,
                    last_synced_at=datetime.utcnow(),
                    source=company.source
                )
                db.add(cache_entry)
            await db.commit()

# Usage example
async def main():
    extractor = EnhancedDataExtractor()
    companies = await extractor.search_companies("Agrofert", [CountryCode.SK, CountryCode.CZ])
    for company in companies:
        print(f"{company.name} ({company.country}): Risk Score {company.risk_score}")
```

## 2. Luxury Design System

### Frontend: Premium Styling Components

```typescript
// frontend/src/styles/design-system.ts
import { createGlobalStyle } from 'styled-components';

export const designTokens = {
  colors: {
    primary: {
      gold: '#D4AF37',
      platinum: '#E5E4E2',
      black: '#0A0A0A',
      charcoal: '#1A1A2E',
      navy: '#0B4EA2',
    },
    secondary: {
      ruby: '#EF4444',
      emerald: '#34D399',
      sapphire: '#60A5FA',
      amber: '#FBBF24',
    },
    text: {
      primary: '#FFFFFF',
      secondary: '#D1D5DB',
      muted: '#9CA3AF',
    },
    background: {
      primary: '#0A0A0A',
      secondary: '#1A1A2E',
      tertiary: '#16213E',
      glass: 'rgba(26, 26, 46, 0.8)',
    },
    border: {
      primary: '#D4AF37',
      secondary: '#374151',
      glass: 'rgba(212, 175, 55, 0.3)',
    },
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px',
  },
  typography: {
    fontFamily: {
      heading: "'Playfair Display', serif",
      body: "'Inter', sans-serif",
      mono: "'JetBrains Mono', monospace",
    },
    fontSize: {
      xs: '12px',
      sm: '14px',
      md: '16px',
      lg: '18px',
      xl: '24px',
      xxl: '32px',
      xxxl: '48px',
    },
    fontWeight: {
      light: 300,
      normal: 400,
      medium: 500,
      bold: 700,
      black: 900,
    },
  },
  shadows: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.3)',
    md: '0 4px 6px rgba(0, 0, 0, 0.3)',
    lg: '0 10px 15px rgba(0, 0, 0, 0.3)',
    xl: '0 20px 25px rgba(0, 0, 0, 0.4)',
    gold: '0 0 20px rgba(212, 175, 55, 0.5)',
  },
  animations: {
    fast: '150ms ease-in-out',
    normal: '300ms ease-in-out',
    slow: '500ms ease-in-out',
  },
};

export const GlobalStyle = createGlobalStyle`
  :root {
    --color-gold: ${designTokens.colors.primary.gold};
    --color-platinum: ${designTokens.colors.primary.platinum};
    --color-black: ${designTokens.colors.primary.black};
    --color-charcoal: ${designTokens.colors.primary.charcoal};
    --color-navy: ${designTokens.colors.primary.navy};
    
    --color-ruby: ${designTokens.colors.secondary.ruby};
    --color-emerald: ${designTokens.colors.secondary.emerald};
    --color-sapphire: ${designTokens.colors.secondary.sapphire};
    --color-amber: ${designTokens.colors.secondary.amber};
    
    --color-text-primary: ${designTokens.colors.text.primary};
    --color-text-secondary: ${designTokens.colors.text.secondary};
    --color-text-muted: ${designTokens.colors.text.muted};
    
    --bg-primary: ${designTokens.colors.background.primary};
    --bg-secondary: ${designTokens.colors.background.secondary};
    --bg-tertiary: ${designTokens.colors.background.tertiary};
    --bg-glass: ${designTokens.colors.background.glass};
    
    --border-primary: ${designTokens.colors.border.primary};
    --border-secondary: ${designTokens.colors.border.secondary};
    --border-glass: ${designTokens.colors.border.glass};
    
    --shadow-sm: ${designTokens.shadows.sm};
    --shadow-md: ${designTokens.shadows.md};
    --shadow-lg: ${designTokens.shadows.lg};
    --shadow-xl: ${designTokens.shadows.xl};
    --shadow-gold: ${designTokens.shadows.gold};
    
    --font-family-heading: ${designTokens.typography.fontFamily.heading};
    --font-family-body: ${designTokens.typography.fontFamily.body};
    --font-family-mono: ${designTokens.typography.fontFamily.mono};
    
    --font-size-xs: ${designTokens.typography.fontSize.xs};
    --font-size-sm: ${designTokens.typography.fontSize.sm};
    --font-size-md: ${designTokens.typography.fontSize.md};
    --font-size-lg: ${designTokens.typography.fontSize.lg};
    --font-size-xl: ${designTokens.typography.fontSize.xl};
    --font-size-xxl: ${designTokens.typography.fontSize.xxl};
    --font-size-xxxl: ${designTokens.typography.fontSize.xxxl};
    
    --font-weight-light: ${designTokens.typography.fontWeight.light};
    --font-weight-normal: ${designTokens.typography.fontWeight.normal};
    --font-weight-medium: ${designTokens.typography.fontWeight.medium};
    --font-weight-bold: ${designTokens.typography.fontWeight.bold};
    --font-weight-black: ${designTokens.typography.fontWeight.black};
    
    --animation-fast: ${designTokens.animations.fast};
    --animation-normal: ${designTokens.animations.normal};
    --animation-slow: ${designTokens.animations.slow};
  }

  * {
    box-sizing: border-box;
  }

  body {
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    color: var(--color-text-primary);
    font-family: var(--font-family-body);
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-family-heading);
    font-weight: var(--font-weight-bold);
    line-height: 1.2;
    margin: 0 0 1rem 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  }

  /* Premium button styling */
  .btn-premium {
    background: linear-gradient(135deg, var(--color-gold), var(--color-platinum));
    border: 2px solid var(--border-glass);
    color: var(--color-black);
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: var(--font-weight-bold);
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: var(--shadow-gold);
    transition: all var(--animation-normal);
    position: relative;
    overflow: hidden;
  }

  .btn-premium:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-xl);
    filter: brightness(1.1);
  }

  .btn-premium::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left var(--animation-slow);
  }

  .btn-premium:hover::before {
    left: 100%;
  }
`;
```

## 3. Enhanced Force-Directed Graph

### Frontend: Interactive Network Visualization

```typescript
// frontend/src/components/EnhancedForceGraph.tsx
import React, { useRef, useState, useCallback, useEffect, memo } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { 
  Building2, User, MapPin, AlertTriangle, 
  ZoomIn, ZoomOut, RotateCcw, Download, 
  Eye, EyeOff, Filter, Search 
} from 'lucide-react';

interface GraphNode {
  id: string;
  label: string;
  type: 'company' | 'person' | 'address' | 'debt';
  country: string;
  risk_score: number;
  size: number;
  color: string;
  details: any;
  connections: number;
  selected: boolean;
  highlighted: boolean;
}

interface GraphEdge {
  source: string;
  target: string;
  type: string;
  weight: number;
  color: string;
}

interface EnhancedForceGraphProps {
  data: {
    nodes: GraphNode[];
    edges: GraphEdge[];
  };
  onNodeClick?: (node: GraphNode) => void;
  onNodeHover?: (node: GraphNode | null) => void;
  height?: number;
  width?: number;
}

const EnhancedForceGraph: React.FC<EnhancedForceGraphProps> = ({
  data,
  onNodeClick,
  onNodeHover,
  height = 600,
  width = 800
}) => {
  const fgRef = useRef<any>();
  const [filters, setFilters] = useState({
    showCompanies: true,
    showPersons: true,
    showAddresses: true,
    showDebts: true,
    minRiskScore: 0,
    maxRiskScore: 10
  });
  const [searchQuery, setSearchQuery] = useState('');
  const [isFullscreen, setIsFullscreen] = useState(false);

  // Node styling
  const getNodeColor = useCallback((node: GraphNode) => {
    if (node.highlighted) return '#FFD700'; // Gold for highlighted
    if (node.selected) return '#FFFFFF'; // White for selected
    
    switch (node.type) {
      case 'company':
        return node.risk_score > 7 ? '#EF4444' : '#D4AF37'; // Red for high risk, Gold for normal
      case 'person':
        return '#60A5FA'; // Blue
      case 'address':
        return '#34D399'; // Green
      case 'debt':
        return '#F87171'; // Red
      default:
        return '#D4AF37';
    }
  }, []);

  const getNodeSize = useCallback((node: GraphNode) => {
    let baseSize = 8;
    if (node.type === 'company') baseSize = 12;
    if (node.type === 'debt') baseSize = 10;
    if (node.selected) baseSize += 4;
    if (node.highlighted) baseSize += 2;
    return baseSize + (node.connections * 0.5);
  }, []);

  const getNodeCanvasObject = useCallback((node: GraphNode, ctx: CanvasRenderingContext2D, globalScale: number) => {
    const label = node.label;
    const fontSize = 12 / globalScale;
    ctx.font = `${fontSize}px Inter`;
    const textWidth = ctx.measureText(label).width;
    const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2);
    
    // Draw node
    ctx.beginPath();
    ctx.arc(node.x, node.y, getNodeSize(node), 0, 2 * Math.PI, false);
    ctx.fillStyle = getNodeColor(node);
    ctx.fill();
    
    // Draw glow effect for high-risk nodes
    if (node.risk_score > 7) {
      ctx.shadowColor = '#EF4444';
      ctx.shadowBlur = 10;
    } else if (node.type === 'company') {
      ctx.shadowColor = '#D4AF37';
      ctx.shadowBlur = 5;
    }
    
    // Draw label
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#FFFFFF';
    ctx.fillText(label, node.x, node.y + 20);
    
    ctx.shadowBlur = 0;
  }, [getNodeSize, getNodeColor]);

  // Edge styling
  const getEdgeColor = useCallback((edge: GraphEdge) => {
    switch (edge.type) {
      case 'OWNED_BY': return '#D4AF37';
      case 'MANAGED_BY': return '#60A5FA';
      case 'LOCATED_AT': return '#34D399';
      case 'HAS_DEBT': return '#EF4444';
      default: return '#D4AF37';
    }
  }, []);

  // Filter data
  const filteredData = React.useMemo(() => {
    const filteredNodes = data.nodes.filter(node => {
      // Type filter
      if (node.type === 'company' && !filters.showCompanies) return false;
      if (node.type === 'person' && !filters.showPersons) return false;
      if (node.type === 'address' && !filters.showAddresses) return false;
      if (node.type === 'debt' && !filters.showDebts) return false;
      
      // Risk score filter
      if (node.risk_score < filters.minRiskScore || node.risk_score > filters.maxRiskScore) return false;
      
      // Search filter
      if (searchQuery && !node.label.toLowerCase().includes(searchQuery.toLowerCase())) return false;
      
      return true;
    });

    const filteredEdges = data.edges.filter(edge => {
      const sourceNode = filteredNodes.find(n => n.id === edge.source);
      const targetNode = filteredNodes.find(n => n.id === edge.target);
      return sourceNode && targetNode;
    });

    return { nodes: filteredNodes, edges: filteredEdges };
  }, [data, filters, searchQuery]);

  // Toolbar component
  const Toolbar = () => (
    <div className="absolute top-4 right-4 z-10 flex flex-col gap-2 bg-black/50 backdrop-blur-md p-4 rounded-xl border border-gold/30">
      {/* Zoom controls */}
      <div className="flex gap-2">
        <button
          onClick={() => fgRef.current?.zoom(1.5, 200)}
          className="p-2 bg-gold/20 border border-gold/30 rounded-lg text-gold hover:bg-gold/40 transition-all"
          title="Zoom In"
        >
          <ZoomIn size={18} />
        </button>
        <button
          onClick={() => fgRef.current?.zoom(0.75, 200)}
          className="p-2 bg-gold/20 border border-gold/30 rounded-lg text-gold hover:bg-gold/40 transition-all"
          title="Zoom Out"
        >
          <ZoomOut size={18} />
        </button>
        <button
          onClick={() => fgRef.current?.zoomToFit(400)}
          className="p-2 bg-gold/20 border border-gold/30 rounded-lg text-gold hover:bg-gold/40 transition-all"
          title="Fit to Screen"
        >
          <RotateCcw size={18} />
        </button>
      </div>

      {/* Export controls */}
      <div className="flex gap-2">
        <button
          onClick={() => {
            // Export logic
            const canvas = fgRef.current?.getGraphCanvas();
            if (canvas) {
              const link = document.createElement('a');
              link.download = 'network-graph.png';
              link.href = canvas.toDataURL('image/png');
              link.click();
            }
          }}
          className="p-2 bg-emerald/20 border border-emerald/30 rounded-lg text-emerald hover:bg-emerald/40 transition-all"
          title="Export PNG"
        >
          <Download size={18} />
        </button>
      </div>

      {/* Filter controls */}
      <div className="flex gap-2">
        <button
          onClick={() => setFilters(prev => ({ ...prev, showCompanies: !prev.showCompanies }))}
          className={`p-2 border rounded-lg transition-all ${
            filters.showCompanies ? 'bg-gold/20 border-gold/30 text-gold' : 'bg-gray/20 border-gray/30 text-gray'
          }`}
          title="Toggle Companies"
        >
          <Building2 size={18} />
        </button>
        <button
          onClick={() => setFilters(prev => ({ ...prev, showPersons: !prev.showPersons }))}
          className={`p-2 border rounded-lg transition-all ${
            filters.showPersons ? 'bg-sapphire/20 border-sapphire/30 text-sapphire' : 'bg-gray/20 border-gray/30 text-gray'
          }`}
          title="Toggle Persons"
        >
          <User size={18} />
        </button>
        <button
          onClick={() => setFilters(prev => ({ ...prev, showDebts: !prev.showDebts }))}
          className={`p-2 border rounded-lg transition-all ${
            filters.showDebts ? 'bg-ruby/20 border-ruby/30 text-ruby' : 'bg-gray/20 border-gray/30 text-gray'
          }`}
          title="Toggle Debts"
        >
          <AlertTriangle size={18} />
        </button>
      </div>
    </div>
  );

  return (
    <div className="relative border-2 border-gold/30 rounded-xl bg-gradient-to-br from-black via-charcoal to-navy shadow-2xl overflow-hidden">
      {/* Search bar */}
      <div className="absolute top-4 left-4 z-10 bg-black/50 backdrop-blur-md p-3 rounded-lg border border-gold/30">
        <div className="flex items-center gap-2">
          <Search size={18} className="text-gold" />
          <input
            type="text"
            placeholder="Search nodes..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="bg-transparent text-white placeholder-gray-400 border-none outline-none"
          />
        </div>
      </div>

      {/* Toolbar */}
      <Toolbar />

      {/* Graph */}
      <ForceGraph2D
        ref={fgRef}
        graphData={filteredData}
        nodeLabel={(node) => `${node.label}\n${node.type} • Risk: ${node.risk_score}/10`}
        nodeColor={getNodeColor}
        nodeVal={getNodeSize}
        nodeCanvasObject={getNodeCanvasObject}
        nodeRelSize={6}
        linkColor={(link) => getEdgeColor(link as any)}
        linkWidth={2}
        linkDirectionalArrowLength={6}
        linkDirectionalArrowRelPos={1}
        linkCurvature={0.25}
        onNodeClick={(node) => onNodeClick?.(node as GraphNode)}
        onNodeHover={(node) => onNodeHover?.(node as GraphNode | null)}
        cooldownTicks={100}
        onEngineStop={() => {
          if (fgRef.current) {
            fgRef.current.zoomToFit(400);
          }
        }}
        backgroundColor="transparent"
        width={width}
        height={height}
        d3VelocityDecay={0.6} // Smoother animations
        d3Force="charge" // Better node separation
      />
    </div>
  );
};

export default memo(EnhancedForceGraph);
```

## 4. Professional PDF Export

### Backend: PDF Generation Service

```python
# backend/services/pdf_export_service.py
from datetime import datetime
from typing import Dict, List, Optional
import logging

from jinja2 import Template
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from services.export_service import export_to_excel

class PDFExportService:
    """Professional PDF export service with bank-grade templates."""
    
    def __init__(self):
        self.font_config = FontConfiguration()
        self.templates = {
            'executive_summary': self._load_template('executive_summary.html'),
            'company_profile': self._load_template('company_profile.html'),
            'network_analysis': self._load_template('network_analysis.html'),
            'risk_assessment': self._load_template('risk_assessment.html'),
        }
    
    def _load_template(self, template_name: str) -> Template:
        """Load HTML template for PDF generation."""
        template_path = f"templates/pdf/{template_name}"
        with open(template_path, 'r', encoding='utf-8') as f:
            return Template(f.read())
    
    def generate_executive_summary(self, companies: List[Dict], metadata: Dict) -> bytes:
        """Generate executive summary PDF."""
        html_content = self.templates['executive_summary'].render(
            companies=companies,
            metadata=metadata,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_companies=len(companies),
            high_risk_companies=len([c for c in companies if c.get('risk_score', 0) > 7]),
            total_investment=metadata.get('total_investment', 0)
        )
        
        return self._render_pdf(html_content, 'executive_summary')
    
    def generate_company_profile(self, company_data: Dict, relationships: List[Dict]) -> bytes:
        """Generate detailed company profile PDF."""
        html_content = self.templates['company_profile'].render(
            company=company_data,
            relationships=relationships,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return self._render_pdf(html_content, 'company_profile')
    
    def generate_network_analysis(self, graph_data: Dict, insights: Dict) -> bytes:
        """Generate network analysis PDF with embedded graph."""
        html_content = self.templates['network_analysis'].render(
            graph_data=graph_data,
            insights=insights,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return self._render_pdf(html_content, 'network_analysis')
    
    def generate_risk_assessment(self, companies: List[Dict], risk_factors: Dict) -> bytes:
        """Generate professional risk assessment PDF."""
        html_content = self.templates['risk_assessment'].render(
            companies=companies,
            risk_factors=risk_factors,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            risk_summary=self._calculate_risk_summary(companies)
        )
        
        return self._render_pdf(html_content, 'risk_assessment')
    
    def _render_pdf(self, html_content: str, document_type: str) -> bytes:
        """Render HTML content to PDF with professional styling."""
        try:
            # Create HTML document
            html = HTML(string=html_content, base_url='.')
            
            # Professional CSS styling
            css = CSS(string=self._get_professional_css())
            
            # Render PDF
            pdf_bytes = html.write_pdf(stylesheets=[css], font_config=self.font_config)
            
            logging.info(f"Generated {document_type} PDF: {len(pdf_bytes)} bytes")
            return pdf_bytes
            
        except Exception as e:
            logging.error(f"PDF generation failed: {e}")
            raise
    
    def _get_professional_css(self) -> str:
        """Return professional CSS styling for PDF documents."""
        return """
            @page {
                size: A4;
                margin: 2cm;
                @top-center {
                    content: "ILUMINATI SYSTEM - Executive Intelligence";
                    font-family: "Playfair Display", serif;
                    font-size: 12pt;
                    color: #D4AF37;
                }
                @bottom-center {
                    content: "Confidential - For Authorized Use Only";
                    font-family: "Inter", sans-serif;
                    font-size: 8pt;
                    color: #666;
                }
            }
            
            body {
                font-family: "Inter", sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
            }
            
            h1, h2, h3, h4, h5, h6 {
                font-family: "Playfair Display", serif;
                color: #0B4EA2;
                margin-top: 0;
                margin-bottom: 1rem;
            }
            
            h1 {
                font-size: 24pt;
                border-bottom: 2px solid #D4AF37;
                padding-bottom: 10px;
                color: #D4AF37;
            }
            
            h2 {
                font-size: 18pt;
                color: #0B4EA2;
                border-left: 4px solid #D4AF37;
                padding-left: 15px;
            }
            
            .header {
                text-align: center;
                margin-bottom: 2rem;
                padding: 2rem;
                background: linear-gradient(135deg, #0A0A0A, #1A1A2E);
                color: white;
                border-radius: 8px;
            }
            
            .company-name {
                font-size: 28pt;
                font-weight: bold;
                color: #D4AF37;
                margin-bottom: 0.5rem;
            }
            
            .risk-score {
                font-size: 48pt;
                font-weight: bold;
                color: #EF4444;
                margin: 1rem 0;
            }
            
            .risk-indicator {
                display: inline-block;
                width: 20px;
                height: 20px;
                border-radius: 50%;
                background-color: #EF4444;
                margin-right: 8px;
            }
            
            .table {
                width: 100%;
                border-collapse: collapse;
                margin: 1rem 0;
            }
            
            .table th, .table td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            
            .table th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            
            .table tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            
            .chart-container {
                width: 100%;
                height: 400px;
                margin: 1rem 0;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            
            .footer-note {
                font-size: 8pt;
                color: #666;
                margin-top: 2rem;
                font-style: italic;
            }
            
            .signature {
                margin-top: 3rem;
                text-align: right;
            }
            
            .watermark {
                position: fixed;
                bottom: 0;
                right: 0;
                opacity: 0.1;
                font-size: 120pt;
                font-weight: bold;
                color: #D4AF37;
                transform: rotate(-45deg);
                pointer-events: none;
            }
        """
    
    def _calculate_risk_summary(self, companies: List[Dict]) -> Dict:
        """Calculate risk summary statistics."""
        total_companies = len(companies)
        high_risk = len([c for c in companies if c.get('risk_score', 0) > 7])
        medium_risk = len([c for c in companies if 4 < c.get('risk_score', 0) <= 7])
        low_risk = len([c for c in companies if c.get('risk_score', 0) <= 4])
        
        avg_risk = sum(c.get('risk_score', 0) for c in companies) / max(total_companies, 1)
        
        return {
            'total_companies': total_companies,
            'high_risk_count': high_risk,
            'medium_risk_count': medium_risk,
            'low_risk_count': low_risk,
            'average_risk_score': round(avg_risk, 2),
            'high_risk_percentage': round((high_risk / max(total_companies, 1)) * 100, 1)
        }

# Usage example
async def export_company_profile(company_id: str):
    pdf_service = PDFExportService()
    
    # Get company data and relationships
    company_data = await get_company_data(company_id)
    relationships = await get_company_relationships(company_id)
    
    # Generate PDF
    pdf_bytes = pdf_service.generate_company_profile(company_data, relationships)
    
    # Save or return PDF
    return pdf_bytes
```

These code samples demonstrate the key components of the enhanced data extraction and visualization tool, showcasing the luxury banking aesthetic, advanced functionality, and professional-grade implementation.