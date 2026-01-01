# Mermaid Architecture Diagrams

## System Architecture Overview

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[React 18 + TypeScript]
        B[Dashboard UI]
        C[Graph Viewer]
        D[Export Tools]
        E[State Management]
        F[Styling System]
        
        A --> B
        A --> C
        A --> D
        A --> E
        A --> F
    end
    
    subgraph "Backend Layer"
        G[FastAPI + Python 3.10+]
        H[API Gateway]
        I[Data Services]
        J[Export Service]
        K[Task Queue]
        L[Caching Layer]
        
        G --> H
        G --> I
        G --> J
        G --> K
        G --> L
    end
    
    subgraph "Data Layer"
        M[PostgreSQL + TimescaleDB]
        N[Redis Cache]
        O[Company Data]
        P[Relationships]
        Q[Audit Logs]
        
        M --> O
        M --> P
        M --> Q
        N --> O
        N --> P
    end
    
    subgraph "External Integrations"
        R[Slovak ORSR]
        S[Czech ARES]
        T[Polish KRS]
        U[Hungarian NAV]
        V[Stripe API]
        W[CDN Services]
        
        R --> I
        S --> I
        T --> I
        U --> I
        V --> J
        W --> F
    end
    
    B --> G
    C --> G
    D --> G
    H --> I
    H --> J
    I --> M
    I --> N
    J --> M
```

## Data Flow Diagram

```mermaid
sequenceDiagram
    participant User as User
    participant Frontend as Frontend
    participant Backend as Backend
    participant Cache as Redis Cache
    participant DB as PostgreSQL
    participant ORSR as ORSR API
    participant ARES as ARES API
    participant KRS as KRS API
    participant NAV as NAV API
    
    User->>Frontend: Search Company
    Frontend->>Backend: API Request
    Backend->>Cache: Check Cache
    Cache-->>Backend: Cache Miss
    Backend->>DB: Check Database
    DB-->>Backend: DB Miss
    Backend->>ORSR: Live Scraping
    Backend->>ARES: Live Scraping
    Backend->>KRS: Live Scraping
    Backend->>NAV: Live Scraping
    ORSR-->>Backend: Company Data
    ARES-->>Backend: Company Data
    KRS-->>Backend: Company Data
    NAV-->>Backend: Company Data
    Backend->>DB: Store Data
    Backend->>Cache: Store Cache
    Backend-->>Frontend: Response
    Frontend-->>User: Display Results
```

## Enhanced Data Extraction Pipeline

```mermaid
flowchart TD
    A[User Request] --> B{Cache Check}
    B -->|Hit| C[Return Cached Data]
    B -->|Miss| D{Database Check}
    D -->|Hit| E{Data Fresh?}
    D -->|Miss| F[Live Scraping]
    E -->|Yes| G[Return DB Data]
    E -->|No| F
    F --> H[ORSR Scraping]
    F --> I[ARES Scraping]
    F --> J[KRS Scraping]
    F --> K[NAV Scraping]
    H --> L[Data Normalization]
    I --> L
    J --> L
    K --> L
    L --> M[Store in Database]
    L --> N[Store in Cache]
    M --> O[Return Data]
    N --> O
    G --> O
    C --> O
    
    style A fill:#e1f5fe
    style C fill:#c8e6c9
    style O fill:#fff3e0
    style F fill:#ffcdd2
```

## Graph Visualization Architecture

```mermaid
graph LR
    subgraph "Data Layer"
        A[Company Data] --> B[Relationship Data]
        B --> C[Graph Nodes]
        B --> D[Graph Edges]
    end
    
    subgraph "Processing Layer"
        C --> E[Node Processing]
        D --> F[Edge Processing]
        E --> G[Force Layout]
        F --> G
        G --> H[Physics Simulation]
    end
    
    subgraph "Visualization Layer"
        H --> I[Canvas Rendering]
        H --> J[SVG Rendering]
        I --> K[Interactive Graph]
        J --> K
        K --> L[Export Options]
    end
    
    subgraph "Interaction Layer"
        K --> M[Zoom & Pan]
        K --> N[Node Selection]
        K --> O[Filtering]
        K --> P[Real-time Updates]
    end
    
    style A fill:#e3f2fd
    style B fill:#e8f5e8
    style K fill:#fff3e0
    style L fill:#fce4ec
```

## Export Pipeline Architecture

```mermaid
flowchart TD
    A[User Request] --> B{Export Format}
    B -->|PDF| C[PDF Generation]
    B -->|Excel| D[Excel Generation]
    B -->|CSV| E[CSV Generation]
    B -->|JSON| F[JSON Generation]
    
    C --> G[Template Loading]
    D --> H[Worksheet Creation]
    E --> I[CSV Formatting]
    F --> J[JSON Serialization]
    
    G --> K[Data Processing]
    H --> K
    I --> K
    J --> K
    
    K --> L[Professional Styling]
    L --> M[File Generation]
    M --> N[Download Link]
    N --> O[User Download]
    
    style A fill:#e1f5fe
    style K fill:#fff3e0
    style O fill:#c8e6c9
```

## Security Architecture

```mermaid
graph TB
    subgraph "External Layer"
        A[User Browser] --> B[HTTPS/TLS 1.3]
        B --> C[Load Balancer]
    end
    
    subgraph "Application Layer"
        C --> D[API Gateway]
        D --> E[Authentication Service]
        D --> F[Rate Limiting]
        D --> G[CORS Validation]
        
        E --> H[JWT Validation]
        H --> I[Authorization Check]
        I --> J[Business Logic]
    end
    
    subgraph "Data Layer"
        J --> K[Database Access]
        J --> L[Cache Access]
        K --> M[PostgreSQL]
        L --> N[Redis]
        
        M --> O[Data Encryption]
        N --> P[Secure Cache]
    end
    
    subgraph "Monitoring Layer"
        J --> Q[Audit Logging]
        J --> R[Security Monitoring]
        Q --> S[Log Aggregation]
        R --> T[Alert System]
    end
    
    style A fill:#e3f2fd
    style J fill:#fff3e0
    style M fill:#e8f5e8
    style S fill:#fce4ec
```

## Performance Optimization Architecture

```mermaid
graph LR
    subgraph "Frontend Optimizations"
        A[Code Splitting] --> B[Lazy Loading]
        B --> C[Virtualization]
        C --> D[Image Optimization]
        D --> E[Bundle Optimization]
    end
    
    subgraph "Backend Optimizations"
        F[Database Indexing] --> G[Query Optimization]
        G --> H[Caching Strategy]
        H --> I[Background Processing]
        I --> J[Load Balancing]
    end
    
    subgraph "Infrastructure"
        K[CDN] --> L[Static Assets]
        M[Redis Cluster] --> N[High Performance Cache]
        O[Database Replication] --> P[Read Scaling]
    end
    
    subgraph "Monitoring"
        Q[Performance Metrics] --> R[Alerting]
        R --> S[Auto-scaling]
    end
    
    style A fill:#e1f5fe
    style F fill:#fff3e0
    style K fill:#e8f5e8
    style Q fill:#fce4ec
```

These Mermaid diagrams provide visual representations of the enhanced data extraction and visualization tool architecture, showing the relationships between components, data flows, and system interactions.