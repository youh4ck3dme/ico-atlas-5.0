# Technical Specifications: Enhanced Data Extraction & Visualization Tool

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  React 18 + TypeScript                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  Dashboard UI   │  │  Graph Viewer   │  │  Export Tools   │  │
│  │                 │  │                 │  │                 │  │
│  │ • Executive     │  │ • Force-Directed│  │ • PDF Export    │  │
│  │   Overview      │  │   Graph         │  │ • Excel Export  │  │
│  │ • Risk Metrics  │  │ • Real-time     │  │ • CSV Export    │  │
│  │ • Search        │  │   Animations    │  │ • JSON Export   │  │
│  │ • Filters       │  │ • Micro-        │  │ • Professional  │  │
│  │ • Premium UI    │  │   Interactions  │  │   Templates     │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  State Management: Zustand/Redux Toolkit                        │
│  Styling: Tailwind CSS + Custom Design System                   │
│  Charts: D3.js + react-force-graph-2d                           │
│  PDF: jsPDF + HTML2Canvas                                       │
│  Excel: SheetJS (xlsx)                                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP/HTTPS + WebSocket
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI + Python 3.10+                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  API Gateway    │  │  Data Services  │  │  Export Service │  │
│  │                 │  │                 │  │                 │  │
│  │ • Authentication│  │ • ORSR (SK)     │  │ • PDF Generation│  │
│  │ • Rate Limiting │  │ • ARES (CZ)     │  │ • Excel Export  │  │
│  │ • Validation    │  │ • KRS (PL)      │  │ • CSV Export    │  │
│  │ • Middleware    │  │ • NAV (HU)      │  │ • Template Mgmt │  │
│  │ • CORS          │  │ • Caching       │  │ • Professional  │  │
│  │ • Logging       │  │ • Normalization │  │   Styling       │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  Task Queue: Celery + Redis                                     │
│  Caching: Redis (Multi-layer)                                   │
│  Monitoring: Prometheus + Grafana                               │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Database Queries
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│  PostgreSQL + TimescaleDB                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  Company Data   │  │  Relationships  │  │  Audit Logs    │  │
│  │                 │  │                 │  │                 │  │
│  │ • Basic Info    │  │ • Ownership     │  │ • Access Logs   │  │
│  │ • Financials    │  │ • Management    │  │ • Export Logs   │  │
│  │ • Risk Scores   │  │ • Location      │  │ • Error Logs    │  │
│  │ • Metadata      │  │ • Debt          │  │ • Performance   │  │
│  │ • Timestamps    │  │ • Cross-border  │  │ • User Activity │  │
│  │ • Source Info   │  │ • Complex Paths │  │ • System Health │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  Redis Cache: Multi-layer strategy                              │
│  • Layer 1: 12 hours (Hot data)                                 │
│  • Layer 2: 7 days (Warm data)                                  │
│  • Layer 3: Live scraping (Cold data)                           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ External API Calls
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL INTEGRATIONS                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Slovak ORSR   │  │   Czech ARES    │  │   Polish KRS    │  │
│  │                 │  │                 │  │                 │  │
│  │ • Live Scraping │  │ • Official API  │  │ • Multi-source  │  │
│  │ • Company Data  │  │ • Real-time     │  │ • Aggregation   │  │
│  │ • Risk Analysis │  │ • Validation    │  │ • Normalization │  │
│  │ • Historical    │  │ • Rate Limits   │  │ • Caching       │  │
│  │   Data          │  │ • Error Handling│  │ • Quality Check │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ Hungarian NAV   │  │  Stripe API     │  │  CDN Services   │  │
│  │                 │  │                 │  │                 │  │
│  │ • Tax Data      │  │ • Payments      │  │ • Static Assets │  │
│  │ • Real-time     │  │ • Subscriptions │  │ • Performance   │  │
│  │ • Compliance    │  │ • Webhooks      │  │ • Global Access │  │
│  │ • Validation    │  │ • Security      │  │ • Caching       │  │
│  │ • Integration   │  │ • Analytics     │  │ • Monitoring    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Models

### 1. Company Data Model

```typescript
interface Company {
  // Primary Identifier
  id: string;                    // UUID
  identifier: string;           // IČO/KRS/Adószám
  country: CountryCode;         // SK/CZ/PL/HU
  
  // Basic Information
  name: string;                 // Obchodné meno
  legal_form: string;           // Právna forma
  status: string;               // Aktívna/Likvidácia/Konkurz
  founded: string;              // YYYY-MM-DD
  last_updated: string;         // ISO 8601
  
  // Address Information
  address: string;              // Full address
  postal_code: string;          // PSČ
  city: string;
  region: string;               // Kraj
  district: string;             // Okres
  virtual_seat?: boolean;       // Virtual office flag
  
  // Financial Information
  dic: string;                  // DIČ
  ic_dph: string;               // IČ DPH
  financial_data?: FinancialData;
  
  // Risk Assessment
  risk_score: number;           // 0-10
  risk_factors: RiskFactor[];   // Detailed risk factors
  last_risk_assessment: string; // ISO 8601
  
  // Relationships
  executives: string[];         // Management
  shareholders: string[];       // Ownership
  related_companies: string[];  // Cross-border links
  
  // Source & Metadata
  source: string;               // Register source
  source_url?: string;          // Original source URL
  data_quality: DataQuality;    // Quality score
  scraped_at?: string;          // Scraping timestamp
  validated_at?: string;        // Validation timestamp
}
```

### 2. Relationship Data Model

```typescript
interface Relationship {
  id: string;                   // UUID
  source_id: string;            // Source company ID
  target_id: string;            // Target company/person ID
  type: RelationshipType;       // OWNED_BY/MANAGED_BY/etc.
  weight: number;               // Relationship strength
  confidence: number;           // 0-1 confidence score
  
  // Temporal Information
  start_date?: string;          // YYYY-MM-DD
  end_date?: string;            // YYYY-MM-DD
  active: boolean;              // Current status
  
  // Source Information
  source: string;               // Register source
  source_url?: string;          // Original source URL
  verified: boolean;            // Verification status
  verified_at?: string;         // Verification timestamp
  
  // Cross-border Information
  cross_border: boolean;        // Cross-border relationship
  countries_involved: string[]; // Countries in relationship
}
```

### 3. Graph Node Model

```typescript
interface GraphNode {
  id: string;                   // Unique node ID
  label: string;                // Display label
  type: NodeType;               // company/person/address/debt
  country: CountryCode;
  
  // Visual Properties
  size: number;                 // Node size
  color: string;                // Node color
  shape: NodeShape;             // circle/rectangle/etc.
  opacity: number;              // Transparency
  
  // Data Properties
  data: any;                    // Raw data object
  connections: number;          // Number of connections
  centrality: number;           // Centrality measure
  
  // Position (for force-directed layout)
  x?: number;                   // X coordinate
  y?: number;                   // Y coordinate
  vx?: number;                  // X velocity
  vy?: number;                  // Y velocity
  
  // State Properties
  selected: boolean;            // Selection state
  highlighted: boolean;         // Highlight state
  collapsed: boolean;           // Collapsed state
}
```

### 4. Graph Edge Model

```typescript
interface GraphEdge {
  id: string;                   // Unique edge ID
  source: string;               // Source node ID
  target: string;               // Target node ID
  type: EdgeType;               // Relationship type
  
  // Visual Properties
  color: string;                // Edge color
  width: number;                // Edge width
  style: EdgeStyle;             // solid/dashed/dotted
  opacity: number;              // Transparency
  
  // Data Properties
  weight: number;               // Edge weight
  label?: string;               // Edge label
  direction: boolean;           // Directed/undirected
  
  // Source Information
  source: string;               // Register source
  confidence: number;           // Confidence score
  verified: boolean;            // Verification status
}
```

## API Specifications

### 1. Enhanced Search API

```typescript
// Request
interface SearchRequest {
  query: string;                // Company name or identifier
  countries?: CountryCode[];    // Filter by countries
  include_related?: boolean;    // Include related companies
  risk_threshold?: number;      // Filter by risk score
  limit?: number;               // Result limit
  offset?: number;              // Pagination offset
  format?: 'basic' | 'detailed' | 'graph'; // Response format
}

// Response
interface SearchResponse {
  results: Company[];
  total: number;
  facets: SearchFacets;
  suggestions: string[];
  execution_time: number;       // ms
  cache_hit: boolean;
}
```

### 2. Graph API

```typescript
// Request
interface GraphRequest {
  company_ids: string[];        // Starting companies
  depth?: number;               // Search depth
  relationship_types?: string[]; // Filter by relationship types
  max_nodes?: number;           // Maximum nodes to return
  layout?: 'force' | 'hierarchical' | 'circular'; // Layout type
}

// Response
interface GraphResponse {
  nodes: GraphNode[];
  edges: GraphEdge[];
  metadata: {
    total_nodes: number;
    total_edges: number;
    layout: string;
    execution_time: number;
  };
}
```

### 3. Export API

```typescript
// Request
interface ExportRequest {
  format: 'pdf' | 'excel' | 'csv' | 'json';
  data: any;                    // Data to export
  options: {
    include_graph?: boolean;    // Include graph visualization
    branding?: 'premium' | 'standard'; // Export branding
    timestamp?: boolean;        // Include timestamp
    executive_summary?: boolean; // Include executive summary
    risk_analysis?: boolean;    // Include risk analysis
  };
}

// Response
interface ExportResponse {
  file_url: string;             // Download URL
  file_size: number;            // File size in bytes
  format: string;               // Export format
  generated_at: string;         // ISO 8601 timestamp
}
```

## Performance Specifications

### 1. Response Time Targets

| Operation | Target | Maximum |
|-----------|--------|---------|
| Search API | < 500ms | < 2s |
| Graph Generation | < 1s | < 5s |
| PDF Export | < 10s | < 30s |
| Excel Export | < 5s | < 15s |
| Dashboard Load | < 2s | < 5s |

### 2. Concurrent User Support

| Tier | Concurrent Users | Requests/Second | Data Size |
|------|------------------|-----------------|-----------|
| Free | 100 | 50 | 1000 nodes |
| Pro | 1000 | 500 | 10000 nodes |
| Enterprise | 10000 | 5000 | 100000 nodes |

### 3. Data Volume Limits

| Data Type | Free | Pro | Enterprise |
|-----------|------|-----|------------|
| Companies | 1000 | 10000 | 100000 |
| Relationships | 5000 | 50000 | 500000 |
| Monthly API Calls | 1000 | 10000 | 100000 |
| Export Size | 10MB | 100MB | 1GB |

## Security Specifications

### 1. Authentication & Authorization

```typescript
interface AuthConfig {
  jwt_secret: string;           // JWT secret key
  jwt_expiration: string;       // JWT expiration time
  refresh_token_expiration: string; // Refresh token expiration
  allowed_origins: string[];    // CORS allowed origins
  rate_limit: {
    window: number;             // Time window in seconds
    limit: number;              // Requests per window
    burst: number;              // Burst limit
  };
}
```

### 2. Data Protection

- **Encryption:** AES-256 for sensitive data at rest
- **TLS:** TLS 1.3 for all communications
- **Hashing:** bcrypt for password hashing
- **Token Security:** JWT with refresh token rotation
- **Audit Logging:** Complete activity logging

### 3. Compliance Requirements

- **GDPR:** Data protection and user rights
- **PSD2:** Strong customer authentication
- **ISO 27001:** Information security management
- **SOC 2:** Security and availability controls

## Monitoring & Observability

### 1. Key Metrics

```typescript
interface Metrics {
  // Performance Metrics
  api_response_time: number;    // Average response time
  cache_hit_rate: number;       // Cache hit percentage
  database_query_time: number;  // Average query time
  memory_usage: number;         // Memory usage percentage
  
  // Business Metrics
  active_users: number;         // Daily active users
  search_volume: number;        // Daily search count
  export_volume: number;        // Daily export count
  conversion_rate: number;      // Free to paid conversion
  
  // System Health
  error_rate: number;           // Error rate percentage
  uptime: number;               // System uptime percentage
  cpu_usage: number;            // CPU usage percentage
  disk_usage: number;           // Disk usage percentage
}
```

### 2. Alerting Rules

```typescript
interface AlertRules {
  high_error_rate: {
    threshold: 5;               // 5% error rate
    duration: 300;              // 5 minutes
    severity: 'critical';
  };
  slow_response_time: {
    threshold: 2000;            // 2 seconds
    duration: 600;              // 10 minutes
    severity: 'warning';
  };
  low_cache_hit_rate: {
    threshold: 50;              // 50% cache hit rate
    duration: 1800;             // 30 minutes
    severity: 'warning';
  };
}
```

This technical specification provides comprehensive details for implementing the enhanced data extraction and visualization tool with enterprise-grade performance, security, and monitoring capabilities.