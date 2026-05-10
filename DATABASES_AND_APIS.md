# Mapa de Integração de Bancos de Dados e APIs — PowerShoring Analytics

> **ESTRATÉGIA DE DADOS:** Este projeto integra múltiplas origens de dados geoespaciais e tabulares, operando de forma híbrida entre consumo de APIs REST diretas, conexões com banco de dados relacional geográfico e processamento ETL de Big Data em memória. **Nenhum dado é mockado.**

---

## 1. Fontes Estatísticas e Governamentais (REST APIs)

### 📊 A. ANP — Agência Nacional do Petróleo, Gás Natural e Biocombustíveis
Acesso a metadados e downloads diretos de combustíveis e biorrefinarias (Etanol, Biodiesel, Biometano).
- **Método:** Requisições REST via `httpx` (async) direcionadas aos endpoints JSON/Swagger do Portal Brasileiro de Dados Abertos (padrão CKAN).
- **Endpoint Metadados:** `https://dados.gov.br/api/3/action/package_show?id=...`
- **Pipeline ETL:** Scripts Python baixam CSV/XML em URLs diretas, com:
  - Parser de encoding Windows-1252 → UTF-8.
  - Normalização de separadores decimais PT-BR (vírgula → ponto).
  - Validação de campos obrigatórios antes da carga no PostGIS.

### 📈 B. IBGE / SIDRA — Sistema de Recuperação Automática (API v3)
Coleta programática de dados econômicos, populacionais e agropecuários (PAM, PEVS, PIB Municipal).
- **Método:** API de Dados Agregados v3 (terminologia OLAP: variáveis, classificações, categorias).
- **Biblioteca Python:** `sidrapy` — interface nativa para consultas granulares por níveis territoriais (N1 a N6).
- **Snippet:**
  ```python
  import sidrapy
  # PAM - Produção Agrícola Municipal
  data = sidrapy.get_table(
      table_code="1419",
      territorial_level="1",
      ibge_territorial_code="all",
      period="last 12"
  )
  ```
- **Tabelas-Alvo:** PIB per capita municipal, emprego formal, escolaridade, PAM (lavouras), PEVS (silvicultura).

### 🌐 C. Fontes Externas Complementares
| Fonte | Método de Acesso | Dados Chave |
|:---|:---|:---|
| **CONAB** | Portal de Informações Agropecuárias (download CSV) | Estimativas de safra, resíduos agropecuários |
| **IBÁ** | Relatórios (download PDF/XLSX) | Florestas plantadas, produção celulose |
| **World Bank Open Data** | REST API (`https://api.worldbank.org/v2/`) | PIB, Gini, IED, indicadores sociais |
| **IRENA** | Data Portal (download CSV) | Capacidade renovável global, custos |
| **World Steel Association** | Dados via portal (parcial restrito) | Produção siderúrgica global |
| **Instituto Aço Brasil** | Relatórios estatísticos | Produção, consumo, capacidade siderúrgica |
| **Observatório do Código Florestal** | Portal web (dados geoespaciais) | Implementação do Código Florestal |
| **Observatório Sebrae** | Dashboards interativos + download | Dados econômicos setoriais/territoriais |
| **Terrabrasilis (INPE)** | Portal web + API de tiles | PRODES, DETER (vegetação nativa) |
| **BDiA (IBGE)** | Portal web (download shapefiles) | Geologia, Geomorfologia, Pedologia, Vegetação |
| **Atlas Nacional Digital (IBGE)** | Portal interativo | Mapas socioeconômicos integrados |
| **EPE — BEN** | Download publicação anual | Balanço Energético Nacional |
| **EPE — Webmap** | Portal interativo geoespacial | Usinas, linhas de transmissão, subestações |
| **SIGA/SIGEL (ANEEL)** | Power BI público + dados abertos | Parque gerador, capacidade instalada |

---

## 2. Camadas Geoespaciais em Tempo Real (ArcGIS REST)

### 🛰️ A. ESRI ArcGIS — Camadas Base PID (Reverse Engineered)
Conexão nativa com as FeatureLayers oficiais da plataforma PID.
- **Método:** Chamadas REST HTTP GET.
- **Base URL:** `https://services6.arcgis.com/I9CTS4kjOw8Dsslu/arcgis/rest/services/`
- **Payload padrão:** `?where=1=1&outFields=*&f=geojson`
- **Consumo:** Frontend (MapLibre GL) e Backend (httpx/aiohttp para cache).
- **Referência completa:** Ver `PID_REAL_APIS.md`

### 🌳 B. MapBiomas — Cobertura de Terra
| Canal | Método | Uso |
|:---|:---|:---|
| **Visual (Mapa)** | WMS/WFS via GeoServer (`OWSLib`) | Raster/camadas temáticas no frontend |
| **Processamento** | Google Earth Engine (`earthengine-api`) | Análise massiva de cobertura histórica |
| **ArcGIS ImageServer** | REST (tiles) | `https://ic.imagery1.arcgis.com/.../MapBiomas/ImageServer` |

---

## 3. Camada de Banco de Dados e Armazenamento

### 🐘 A. PostgreSQL + Extensão PostGIS
Banco geográfico para persistência de dados processados pelo ETL e inputs administrativos.
- **Driver Sync:** `psycopg2-binary`
- **Driver Async:** `asyncpg` (para rotas FastAPI assíncronas)
- **ORM:** SQLAlchemy 2.0 + GeoAlchemy2
- **URI:** `postgresql://usuario:senha@host:5432/powershoring_db`

### ⚡ B. Indexação Espacial — GiST (Generalized Search Tree)
Aplicação **compulsória** de índices GiST R-Tree em todas as tabelas geométricas.
- **Operações otimizadas:** `ST_Within`, `ST_Contains`, `ST_Distance`, `ST_Intersects`
- **Criação padrão:**
  ```sql
  CREATE INDEX idx_geom_localidades ON tabela USING GIST (geom_coluna);
  ANALYZE tabela;
  ```

### 🔥 C. Firebase Storage
Object storage para arquivos brutos carregados pelo módulo Admin de Ingestão Dinâmica.
- **Validação de Upload:** Verificação de Magic Numbers (assinatura binária) antes de aceitar o arquivo.
- **Formatos aceitos:** `.csv`, `.xlsx`, `.shp` (+ `.shx`, `.dbf`, `.prj`), `.geojson`

### ⚡ D. Redis
Broker de mensagens para filas Celery de processamento assíncrono ETL.

---

## 4. Motores de Processamento Geoespacial (Backend Python)

### 🛠️ A. GEOS (Geometry Engine Open Source)
Motor C++ para operações topológicas (interseção, união, buffer, validação).
- **Binding:** Chamado implicitamente via `Shapely`.
- **Validação:** Previne persistência de geometrias inválidas (auto-interseções) no PostGIS.

### 🐼 B. GeoPandas + Pyogrio (Motor Principal)
Manipulação de DataFrames espaciais e cálculos vetoriais.
- **Motor de I/O:** `pyogrio` (5-10x mais rápido que `fiona` para Shapefiles massivos).
- **Leitura PostGIS:**
  ```python
  import geopandas as gpd
  from sqlalchemy import create_engine
  engine = create_engine("postgresql://...")
  gdf = gpd.read_postgis("SELECT * FROM camada_geo", engine, geom_col="geom")
  ```
- **Escrita PostGIS:**
  ```python
  gdf.to_postgis("nova_camada", engine, if_exists="replace")
  ```
- **Leitura de Shapefiles:**
  ```python
  gdf = gpd.read_file("arquivo.shp", engine="pyogrio")
  ```

### 🚀 C. Dask + Dask-GeoPandas (Big Data / Paralelismo)
Computação distribuída para spatial joins massivos nos Workers Celery.
- **Estratégia:** Divisão de geometrias em chunks espaciais.
- **Snippet:**
  ```python
  import dask_geopandas as dg
  gf = dg.from_geopandas(gdf, npartitions=4)
  results = gf.sjoin(limites_municipais, predicate="intersects").compute()
  ```

---

## 5. Dependências Python (requirements.txt parcial)

```txt
# Web Framework
fastapi
uvicorn[standard]

# HTTP Client (async)
httpx

# Database
psycopg2-binary
asyncpg
sqlalchemy[asyncio]>=2.0
geoalchemy2

# Geospatial
geopandas
pyogrio
shapely>=2.0
dask-geopandas

# Data
pandas
sidrapy
openpyxl

# Task Queue
celery[redis]
redis

# Firebase
firebase-admin

# AI
openai

# MapBiomas (opcional)
earthengine-api
OWSLib
```
