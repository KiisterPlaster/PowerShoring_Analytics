# Blueprint: PowerShoring Analytics

## Overview
**PowerShoring Analytics** is a strategic decision platform supporting Brazil's green reindustrialization. It maps specific industrial clusters across major ports (Itaqui, Pecém, Suape, Aratu, Sepetiba, Paranaguá, Rio Grande) and coordinates energy, minerals, and logistics data from PID (Plataforma Interativa de Descarbonização) to foster a "Just Transition". 

This blueprint outlines the holistic ecosystem structure (Architecture, Docs, Schemas) required for the Hackathon delivery.

---

## Project Type
**WEB & BACKEND** (Decoupled Distributed Architecture)

---

## Tech Stack

### Frontend
- **Core**: React + TypeScript
- **UI**: Tailwind CSS + Framer Motion (Visual Identity applied)
- **Brand Palette**: `#03254D` (Deep Blue), `#FA441A` (Action Orange), `#BECCCC`, `#F89069`, `#B5446E`, `#F5F749`, `#550C18`, `#4D4E03`.
- **Map Interface**: MapLibre GL / React-Leaflet (Direct ArcGIS FeatureLayer REST Consumption)
- **State**: React Context + TanStack Query

### Backend & ETL
- **Core**: FastAPI (Python)
- **ETL Engine**: Celery Workers + Redis queue (Asynchronous processing)
- **Geospatial**: PostGIS (Natively handles GEOS/C operations)
- **Storage**: Firebase Storage (Object storage for raw files)
- **Geo-Ops**: GeoPandas (Initial ingestion), GDAL/OGR (WGS84 reprojection)

### AI Engine
- **Model**: OpenAI GPT-4o / Claude 3.5 Sonnet API
- **Data Sources**: COMPULSORY consumption of all 20+ sources listed in `docs/BANCO_DADOS_PID.md` (BDiA, MapBiomas, Terrabrasilis, PEVS, PAM, SIDRA, Conab, IBÁ, Atlas, EPE, BEN, ANP, SIGA, Sebrae, Florestal, Aço Brasil, World Bank, IRENA, World Steel).
- **Connection Strategy**: Direct consumption of PID's reverse-engineered ArcGIS FeatureServer APIs (`services6.arcgis.com/I9CTS4kjOw8Dsslu`) combined with standard API endpoints for realtime visualization (NO MOCKS).
- **Logic**: Strict System Prompt Injection including extracted API routes.

---

## Success Criteria
1. Full API connection scaffolding documented and functional (Mocked/Skeleton).
2. Asynchronous Ingestion Module documented with magic numbers verification & PostGIS triggers.
3. Dashboard UI hierarchy and Matchmaker flows drafted by specialized UX agents.
4. Unified documentation suite covering Product Spec, Architecture, UX Strategy, and README.

---

## Directory Strategy (Target Structure)
The project files will be deployed following this root structure:

```text
/
â”œâ”€â”€ README.md                <- [MASTER] Project Vision & Core Quickstart
â”œâ”€â”€ PRODUCT_SPEC.md          <- [PM/PO] PRD, User Stories, Acceptance Criteria
â”œâ”€â”€ ARCHITECTURE.md          <- [ARCHITECT] C4 Layout, API Contracts, ER Diagram
â”œâ”€â”€ UX_STRATEGY.md           <- [UX] Flow Maps, Visual Tokens, Micro-interactions
â”œâ”€â”€ .gitignore
â”œâ”€â”€ /backend
â”‚   â”œâ”€â”€ main.py               <- FastAPI Core
â”‚   â”œâ”€â”€ /api                  <- Routers & Controllers
â”‚   â”œâ”€â”€ /core                 <- Config & AI Logic
â”‚   â”œâ”€â”€ /etl                  <- Ingestion Pipelines & Celery Tasks
â”‚   â””â”€â”€ /models               <- SQLAlchemy & Pydantic (PostGIS-aware)
â”œâ”€â”€ /frontend
â”‚   â”œâ”€â”€ /src
â”‚   â”‚   â”œâ”€â”€ /components       <- UI Kit, MapWrapper, Sidebar
â”‚   â”‚   â”œâ”€â”€ /hooks            <- Data Fetching
â”‚   â”‚   â”œâ”€â”€ /pages            <- Dashboard, Matchmaker, AdminUpload
â”‚   â”‚   â””â”€â”€ /styles           <- Global CSS (Tailwind config)
â”œâ”€â”€ /infrastructure
â”‚   â”œâ”€â”€ docker-compose.yml    <- Spin up PostGIS, Redis, API
â”‚   â””â”€â”€ init.sql              <- GIST Indexes & Schema initialization
â””â”€â”€ /docs                     <- [READONLY] Raw PDFs and Source data
```

---

## Task Breakdown

### Phase 1: Product & UX Definition (Core Requirements)
| ID | Task | Agent | Verification |
| :--- | :--- | :--- | :--- |
| T1.1 | Create `PRODUCT_SPEC.md` consolidating Clusters, Personas & User Stories from `Notas Analisar.md`. | `product-manager` | PRD covers all 7 regional port clusters & "Transição Justa" |
| T1.2 | Create `UX_STRATEGY.md` outlining the Dashboard flow and Matchmaker interface mechanics. | `ux-designer` | Strategy includes "Socratic entry" & map interaction hierarchy |

### Phase 2: Architectural Blueprinting
| ID | Task | Agent | Verification |
| :--- | :--- | :--- | :--- |
| T2.1 | Create `ARCHITECTURE.md` covering the C4 Diagram, DB schema, and API routes. | `documentation-writer` | Must specify WGS84 (EPSG:4326), PostGIS triggers & Magic Number upload logic |
| T2.2 | Generate `infrastructure/init.sql` defining PostGIS spatial indexes (GIST) and baseline tables. | `database-architect` | SQL includes geometry types & spatial indexes |

### Phase 3: Code Scaffolding (Implementation)
| ID | Task | Agent | Verification |
| :--- | :--- | :--- | :--- |
| T3.1 | Create `/backend/main.py` and routers skeleton integrating ETL endpoints. | `backend-specialist` | Uvicorn runs without syntax errors; `/docs` displays endpoints |
| T3.2 | Generate `/backend/etl/pipeline.py` with file validator (UUID, Mime-type) and GeoPandas wrapper. | `backend-specialist` | Functions respect safe upload protocols identified in Gate responses |
| T3.3 | Generate `/frontend` basic layout structure matching UI tokens. | `frontend-specialist` | React scaffold with dynamic tailwind configurations |

---

## Phase X: Final Verification

- **Security Check**: `python .agent/skills/vulnerability-scanner/scripts/security_scan.py .`
- **Architecture Validity**: Confirm no purple/violet hex colors specified in `UX_STRATEGY.md`.
- **Socratic Loop**: Verify both edge case answers were successfully manifested in `ARCHITECTURE.md` & `backend/etl/pipeline.py`.
