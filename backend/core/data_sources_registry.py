"""
Registro Central de Fontes de Dados — BANCO_DADOS_PID.md Compliance

Mapeia TODAS as 20 fontes obrigatorias do documento docs/BANCO_DADOS_PID.md
com URLs, tipo de conexao, formato de dados e status de integracao.

Referencia: docs/BANCO_DADOS_PID.md
"""

# Cada entrada corresponde a uma fonte listada no BANCO_DADOS_PID.md
# Ordem: exatamente como aparece no documento original
PID_DATA_SOURCES: list[dict] = [
    # ====== 1. BDiA - Banco de Informacoes Ambientais (IBGE) ======
    {
        "id": "bdia",
        "name": "BDiA - Banco de Informacoes Ambientais",
        "organization": "IBGE",
        "description": (
            "Colecao de bases tematicas de recursos naturais do territorio nacional "
            "(Geologia, Geomorfologia, Pedologia, Vegetacao) na escala 1:250.000."
        ),
        "url": "https://bdiaweb.ibge.gov.br/#/home",
        "api_url": "https://bdiaweb.ibge.gov.br/api",
        "connection_type": "REST API (JSON) + Download SHP/GeoJSON",
        "data_format": "GeoJSON / Shapefile",
        "integration_router": "/api/ibge",
        "integration_method": "GeoPandas read_file() para shapefiles baixados",
    },
    # ====== 2. MapBiomas ======
    {
        "id": "mapbiomas",
        "name": "MapBiomas",
        "organization": "MapBiomas (Rede Multi-institucional)",
        "description": (
            "Rede global que monitora transformacoes na cobertura e uso da terra. "
            "Base de dados espaciais mais detalhada de uso da terra no Brasil."
        ),
        "url": "https://brasil.mapbiomas.org/",
        "api_url": "https://ic.imagery1.arcgis.com/arcgis/rest/services/MapBiomas/ImageServer",
        "connection_type": "ArcGIS ImageServer REST + WMS/WFS GeoServer + Google Earth Engine",
        "data_format": "Raster (ImageServer) / GeoJSON (WFS) / Tiles (WMS)",
        "integration_router": "/api/mapbiomas",
        "integration_method": "httpx async GET para ImageServer REST API",
    },
    # ====== 3. TerraBrasilis (INPE) ======
    {
        "id": "terrabrasilis",
        "name": "TerraBrasilis",
        "organization": "INPE",
        "description": (
            "Plataforma web do INPE para dados do PRODES e DETER - "
            "monitoramento de desmatamento e vegetacao nativa."
        ),
        "url": "https://terrabrasilis.dpi.inpe.br/",
        "api_url": "https://terrabrasilis.dpi.inpe.br/api/v1",
        "connection_type": "REST API (JSON) + WMS/WFS",
        "data_format": "GeoJSON / Shapefile / WMS tiles",
        "integration_router": "/api/terrabrasilis",
        "integration_method": "httpx async GET para REST API + OGC WMS",
    },
    # ====== 4. PEVS - Producao da Extracao Vegetal e da Silvicultura ======
    {
        "id": "pevs",
        "name": "PEVS - Producao da Extracao Vegetal e da Silvicultura",
        "organization": "IBGE",
        "description": (
            "Estatisticas sobre exploracao dos recursos florestais. "
            "Quantidade e valor da producao de extracao vegetal e silvicultura por municipio."
        ),
        "url": "https://www.ibge.gov.br/estatisticas/economicas/agricultura-e-pecuaria/9105-producao-da-extracao-vegetal-e-da-silvicultura.html",
        "api_url": "https://apisidra.ibge.gov.br/values/t/289",
        "connection_type": "SIDRA API v3 (REST/OLAP) via sidrapy",
        "data_format": "JSON (tabular OLAP)",
        "integration_router": "/api/ibge/pevs",
        "integration_method": "sidrapy.get_table(table_code='289')",
    },
    # ====== 5. PAM - Producao Agricola Municipal ======
    {
        "id": "pam",
        "name": "PAM - Producao Agricola Municipal",
        "organization": "IBGE",
        "description": (
            "Pesquisa anual dos principais produtos das lavouras temporarias e permanentes. "
            "Importancia economica e social na pauta de exportacoes e cesta basica."
        ),
        "url": "https://www.ibge.gov.br/estatisticas/economicas/agricultura-e-pecuaria/9117-producao-agricola-municipal-culturas-temporarias-e-permanentes.html",
        "api_url": "https://apisidra.ibge.gov.br/values/t/1419",
        "connection_type": "SIDRA API v3 (REST/OLAP) via sidrapy",
        "data_format": "JSON (tabular OLAP)",
        "integration_router": "/api/ibge/pam",
        "integration_method": "sidrapy.get_table(table_code='1419')",
    },
    # ====== 6. SIDRA - Sistema IBGE de Recuperacao Automatica ======
    {
        "id": "sidra",
        "name": "SIDRA - Sistema IBGE de Recuperacao Automatica",
        "organization": "IBGE",
        "description": (
            "Plataforma online do IBGE para acessar, consultar e extrair "
            "dados estatisticos oficiais (economicos, demograficos e sociais)."
        ),
        "url": "https://sidra.ibge.gov.br/",
        "api_url": "https://apisidra.ibge.gov.br/",
        "connection_type": "REST API v3 (OLAP) via sidrapy",
        "data_format": "JSON (tabular OLAP com variaveis, classificacoes, categorias)",
        "integration_router": "/api/ibge",
        "integration_method": "sidrapy.get_table() com parametros OLAP",
    },
    # ====== 7. CONAB - Portal de Informacoes Agropecuarias ======
    {
        "id": "conab",
        "name": "CONAB - Portal de Informacoes Agropecuarias",
        "organization": "CONAB",
        "description": (
            "Dados e analises sobre o setor agropecuario brasileiro. "
            "Dashboards interativos e bases de dados para download."
        ),
        "url": "https://portaldeinformacoes.conab.gov.br/produtos-360.html",
        "api_url": "https://portaldeinformacoes.conab.gov.br/api",
        "connection_type": "REST API (JSON) + Download CSV/XLSX",
        "data_format": "JSON / CSV / XLSX",
        "integration_router": "/api/external/conab",
        "integration_method": "httpx async GET + pandas read_csv/read_excel",
    },
    # ====== 8. IBA - Industria Brasileira de Arvores ======
    {
        "id": "iba",
        "name": "IBA - Industria Brasileira de Arvores",
        "organization": "IBA",
        "description": (
            "Dados sobre setor de florestas plantadas: producao, area plantada, "
            "consumo e indicadores economicos."
        ),
        "url": "https://iba.org/publicacoes/",
        "api_url": None,
        "connection_type": "Download PDF/XLSX (publicacoes anuais)",
        "data_format": "PDF / XLSX",
        "integration_router": "/api/external/iba",
        "integration_method": "Download manual + pandas read_excel para dados tabulares",
    },
    # ====== 9. Atlas Nacional Digital do Brasil ======
    {
        "id": "atlas_nacional",
        "name": "Atlas Nacional Digital do Brasil",
        "organization": "IBGE",
        "description": (
            "Mapas e visualizacoes geoespaciais sobre populacao, economia, "
            "infraestrutura e meio ambiente do territorio brasileiro."
        ),
        "url": "https://www.ibge.gov.br/apps/atlas_nacional/#/home",
        "api_url": "https://servicodados.ibge.gov.br/api/v3/",
        "connection_type": "REST API IBGE v3 (JSON) + WMS tiles",
        "data_format": "JSON / WMS tiles / GeoJSON",
        "integration_router": "/api/ibge",
        "integration_method": "httpx async GET para API IBGE + WMS tiles no frontend",
    },
    # ====== 10. EPE - WebMap Interativo do Sistema Energetico ======
    {
        "id": "epe_webmap",
        "name": "EPE - WebMap Interativo do Sistema Energetico Brasileiro",
        "organization": "EPE (Empresa de Pesquisa Energetica)",
        "description": (
            "Visualizacao geoespacial de usinas, linhas de transmissao, "
            "subestacoes e recursos energeticos com filtros tematicos."
        ),
        "url": "https://gisepeprd2.epe.gov.br/WebMapEPE/",
        "api_url": "https://gisepeprd2.epe.gov.br/arcgis/rest/services",
        "connection_type": "ArcGIS REST API (FeatureServer/MapServer)",
        "data_format": "GeoJSON / FeatureLayer",
        "integration_router": "/api/external/epe",
        "integration_method": "httpx async GET para ArcGIS REST (mesmo padrao do PID)",
    },
    # ====== 11. BEN - Balanco Energetico Nacional ======
    {
        "id": "ben",
        "name": "BEN - Balanco Energetico Nacional",
        "organization": "EPE",
        "description": (
            "Publicacao anual sobre oferta e consumo de energia. "
            "Producao, transformacao, importacao, exportacao e uso final."
        ),
        "url": "https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/balanco-energetico-nacional-bem",
        "api_url": "https://www.epe.gov.br/dados-abertos/",
        "connection_type": "Download XLSX/CSV + REST API dados abertos",
        "data_format": "XLSX / CSV / PDF",
        "integration_router": "/api/external/epe",
        "integration_method": "httpx download + pandas read_excel para series historicas",
    },
    # ====== 12. Painel Dinamico de Produtores de Etanol (ANP) ======
    {
        "id": "anp_etanol",
        "name": "Painel Dinamico de Produtores de Etanol",
        "organization": "ANP",
        "description": (
            "Informacoes sobre unidades produtoras de etanol: localizacao, "
            "capacidade produtiva, materia-prima e situacao operacional."
        ),
        "url": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/paineis-dinamicos-da-anp/paineis-e-mapa-dinamicos-de-produtores-de-combustiveis-e-derivados/painel-dinamico-de-produtores-de-etanol",
        "api_url": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos",
        "connection_type": "Download CSV/XLSX (bases do painel) + CKAN API",
        "data_format": "CSV / XLSX",
        "integration_router": "/api/anp",
        "integration_method": "httpx download CSV + pandas (encoding Windows-1252)",
    },
    # ====== 13. Painel Dinamico de Produtores de Biodiesel (ANP) ======
    {
        "id": "anp_biodiesel",
        "name": "Painel Dinamico de Produtores de Biodiesel",
        "organization": "ANP",
        "description": (
            "Informacoes sobre unidades produtoras de biodiesel: localizacao, "
            "capacidade autorizada, materia-prima e situacao operacional."
        ),
        "url": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/paineis-dinamicos-da-anp/paineis-e-mapa-dinamicos-de-produtores-de-combustiveis-e-derivados/painel-dinamico-de-produtores-de-biodiesel",
        "api_url": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos",
        "connection_type": "Download CSV/XLSX (bases do painel) + CKAN API",
        "data_format": "CSV / XLSX",
        "integration_router": "/api/anp",
        "integration_method": "httpx download CSV + pandas (encoding Windows-1252)",
    },
    # ====== 14. Painel Dinamico de Produtores de Biometano (ANP) ======
    {
        "id": "anp_biometano",
        "name": "Painel Dinamico de Produtores de Biometano",
        "organization": "ANP",
        "description": (
            "Informacoes sobre unidades produtoras de biometano: localizacao, "
            "capacidade de producao, origem do biogas e situacao operacional."
        ),
        "url": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/paineis-dinamicos-da-anp/paineis-e-mapa-dinamicos-de-produtores-de-combustiveis-e-derivados/painel-dinamico-de-produtores-de-biometano",
        "api_url": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos",
        "connection_type": "Download CSV/XLSX (bases do painel) + CKAN API",
        "data_format": "CSV / XLSX",
        "integration_router": "/api/anp",
        "integration_method": "httpx download CSV + pandas (encoding Windows-1252)",
    },
    # ====== 15. SIGA - Sistema de Informacoes de Geracao da ANEEL ======
    {
        "id": "siga_aneel",
        "name": "SIGA - Sistema de Informacoes de Geracao da ANEEL",
        "organization": "ANEEL",
        "description": (
            "Dados sobre parque gerador de energia eletrica: usinas em operacao "
            "e planejamento, localizacao, capacidade instalada, fonte de geracao."
        ),
        "url": "https://app.powerbi.com/view?r=eyJrIjoiNjc4OGYyYjQtYWM2ZC00YjllLWJlYmEtYzdkNTQ1MTc1NjM2IiwidCI6IjQwZDZmOWI4LWVjYTctNDZhMi05MmQ0LWVhNGU5YzAxNzBlMSIsImMiOjR9",
        "api_url": "https://dadosabertos.aneel.gov.br/api/3/action",
        "connection_type": "CKAN REST API (JSON) — dadosabertos.aneel.gov.br",
        "data_format": "JSON / CSV",
        "integration_router": "/api/external/aneel",
        "integration_method": "httpx async GET para CKAN API da ANEEL",
    },
    # ====== 16. Observatorio Setorial Territorial do Sebrae ======
    {
        "id": "sebrae",
        "name": "Observatorio Setorial Territorial do Sebrae",
        "organization": "SEBRAE",
        "description": (
            "Dados economicos, setoriais e territoriais com dashboards interativos. "
            "Acesso as bases de dados para download."
        ),
        "url": "https://observatorio.sebrae.com.br/",
        "api_url": None,
        "connection_type": "Download CSV/XLSX (bases dos dashboards)",
        "data_format": "CSV / XLSX / PDF",
        "integration_router": "/api/external/sebrae",
        "integration_method": "Download manual + pandas read_csv/read_excel",
    },
    # ====== 17. Observatorio do Codigo Florestal ======
    {
        "id": "codigo_florestal",
        "name": "Observatorio do Codigo Florestal",
        "organization": "Observatorio do Codigo Florestal",
        "description": (
            "Dados e indicadores sobre implementacao do Codigo Florestal no Brasil. "
            "Dashboards interativos e bases de dados."
        ),
        "url": "https://observatorioflorestal.org.br/",
        "api_url": None,
        "connection_type": "Download CSV/GeoJSON + WMS",
        "data_format": "CSV / GeoJSON / WMS",
        "integration_router": "/api/external/florestal",
        "integration_method": "httpx download + GeoPandas read_file para dados espaciais",
    },
    # ====== 18. Instituto Aco Brasil ======
    {
        "id": "aco_brasil",
        "name": "Instituto Aco Brasil",
        "organization": "Instituto Aco Brasil",
        "description": (
            "Estatisticas de producao, consumo e capacidade do setor siderurgico. "
            "Essencial para analise de aco verde e descarbonizacao industrial."
        ),
        "url": "https://www.acobrasil.org.br/site/",
        "api_url": None,
        "connection_type": "Download PDF/XLSX (publicacoes setoriais)",
        "data_format": "PDF / XLSX",
        "integration_router": "/api/external/aco_brasil",
        "integration_method": "Download manual + pandas read_excel para series historicas",
    },
    # ====== 19. World Bank Open Data ======
    {
        "id": "world_bank",
        "name": "World Bank Open Data",
        "organization": "World Bank",
        "description": (
            "Dados globais abertos sobre economia, desenvolvimento e indicadores sociais. "
            "Ferramentas de visualizacao e bases para download."
        ),
        "url": "https://data.worldbank.org/",
        "api_url": "https://api.worldbank.org/v2/",
        "connection_type": "REST API v2 (JSON/XML) — parametros: country, indicator, date",
        "data_format": "JSON / XML / CSV",
        "integration_router": "/api/external/worldbank",
        "integration_method": "httpx async GET para API v2 com filtros por pais/indicador",
    },
    # ====== 20. IRENA - International Renewable Energy Agency ======
    {
        "id": "irena",
        "name": "IRENA - International Renewable Energy Agency",
        "organization": "IRENA",
        "description": (
            "Dados globais sobre energias renovaveis: capacidade instalada, geracao, "
            "custos, investimentos e emprego. Monitoramento da transicao energetica."
        ),
        "url": "https://www.irena.org/Data",
        "api_url": "https://pxweb.irena.org/pxweb/en/IRENASTAT/",
        "connection_type": "PxWeb REST API (JSON) + Download CSV/XLSX",
        "data_format": "JSON (PxWeb) / CSV / XLSX",
        "integration_router": "/api/external/irena",
        "integration_method": "httpx async POST para PxWeb API com query JSON",
    },
    # ====== 21. World Steel Association ======
    {
        "id": "world_steel",
        "name": "World Steel Association",
        "organization": "World Steel Association",
        "description": (
            "Dados globais sobre producao, consumo e comercio de aco. "
            "Series por pais e periodo (parcialmente restritos)."
        ),
        "url": "https://worldsteel.org/data/",
        "api_url": None,
        "connection_type": "Download CSV/XLSX (parcialmente restrito)",
        "data_format": "CSV / XLSX / PDF",
        "integration_router": "/api/external/worldsteel",
        "integration_method": "Download manual + pandas read_excel (dados publicos)",
    },
]


def get_source_by_id(source_id: str) -> dict | None:
    """Lookup a data source by its ID."""
    for source in PID_DATA_SOURCES:
        if source["id"] == source_id:
            return source
    return None


def get_sources_by_org(organization: str) -> list[dict]:
    """Filter data sources by organization name."""
    return [s for s in PID_DATA_SOURCES if organization.lower() in s["organization"].lower()]
