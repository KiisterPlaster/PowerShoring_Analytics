# Estratégia de Arquitetura de Dados & Integrações Multiprotocolo

Este documento especifica as regras de conexão, bibliotecas e padrões de indexação para fontes não-ArcGIS mandatórias no PowerShoring Analytics.

## 📊 1. Fontes Estatísticas e Governamentais

### A. IBGE / SIDRA (API de Dados Agregados v3)

- **Mecanismo**: Utilização da biblioteca Python `sidrapy`.
- **Padrão de Consumo**:

  ```python
  import sidrapy
  # Exemplo de consumo (PAM/PEVS)
  data = sidrapy.get_table(table_code="TABELA", territorial_level="NIVEL", ibge_code="CODIGO", variable="VARIAVEL")
  ```

- **Destino**: Ingestão em lotes no PostgreSQL para cache/cruzamento com clusters espaciais.

### B. ANP (Portal de Dados Abertos)

- **Mecanismo**: Requisições REST via `httpx` ou `requests` direcionadas aos endpoints JSON/Swagger do Governo.
- **Formato**: Parser dinâmico para UTF-8 e tratamento de separadores decimais PT-BR antes do carregamento.

---

## 🌎 2. Camada Geoespacial & Banco de Dados

### A. PostGIS + GIST (Camada de Persistência)

- **Engine**: SQLAlchemy + GeoAlchemy2 + `psycopg2`.
- **Conexão**: `postgresql://{user}:{pass}@{host}:{port}/{db}`
- **Otimização Espacial**: Aplicação compulsória de índices **GiST** em todas as tabelas geométricas para operações de `ST_Within`, `ST_Contains` e `ST_Distance` rápidas.
  - Comando padrão: `CREATE INDEX idx_geom_tabela ON tabela USING GIST (geom);`

### B. Motores Geoespaciais (GEOS & Shapely)

- Processamento de Geometrias em baixo nível (C++) através da biblioteca **Shapely** e bindings de **GEOS** para validação topológica dos Shapefiles/GeoJSONs ingeridos.

---

## 🛠️ 3. Bibliotecas de Processamento & Análise

### A. GeoPandas & Pyogrio

- **Performance**: Uso mandatário do motor `pyogrio` para acelerar a leitura de arquivos vetoriais complexos (I/O acelerado).
- **Interoperabilidade PostGIS**:

  ```python
  import geopandas as gpd
  from sqlalchemy import create_engine
  engine = create_engine('postgresql:///...')
  
  # Leitura direta otimizada
  gdf = gpd.read_postgis("SELECT * FROM camada_geo", engine, geom_col='geom')
  # Escrita otimizada
  gdf.to_postgis("nova_camada", engine, if_exists='replace')
  ```

---

## 🛰️ 4. MapBiomas (Integração Avançada)

### A. WMS / WFS (Web Map Services)

- Conexão via servidor GeoServer MapBiomas para entrega direta ao frontend em visualizações de raster/camadas temáticas dinâmicas sem baixar dados brutos.
- **Bibliotecas**: `OWSLib` no backend para consulta de metadados.

### B. Google Earth Engine (GEE)

- Integração programática via biblioteca `ee` do Python para processamento em nuvem de rasters massivos de cobertura e uso da terra históricos.
