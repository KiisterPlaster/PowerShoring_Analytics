-- ============================================================
-- PowerShoring Analytics — PostGIS Schema Initialization
-- Executes on first container boot via docker-entrypoint-initdb.d
-- ============================================================

-- Enable PostGIS extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ============================================================
-- 1. CLUSTERS INDUSTRIAIS (Atlas do Futuro Industrial 2025)
-- ============================================================
CREATE TABLE IF NOT EXISTS clusters (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    region VARCHAR(50) NOT NULL,
    state VARCHAR(10) NOT NULL,
    port VARCHAR(200),
    vocations TEXT[],
    energy_sources TEXT[],
    critical_minerals TEXT[],
    hydrogen_potential TEXT,
    description TEXT,
    geom GEOMETRY(Point, 4326),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_clusters_geom ON clusters USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_clusters_region ON clusters (region);
CREATE INDEX IF NOT EXISTS idx_clusters_state ON clusters (state);

-- ============================================================
-- 2. CAMADAS GEOESPACIAIS (ArcGIS PID + fontes externas)
-- ============================================================
CREATE TABLE IF NOT EXISTS spatial_layers (
    id SERIAL PRIMARY KEY,
    layer_key VARCHAR(100) UNIQUE NOT NULL,
    source VARCHAR(100) NOT NULL,
    display_name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    geom GEOMETRY(Geometry, 4326),
    properties JSONB DEFAULT '{}',
    fetched_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_spatial_layers_geom ON spatial_layers USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_spatial_layers_key ON spatial_layers (layer_key);
CREATE INDEX IF NOT EXISTS idx_spatial_layers_category ON spatial_layers (category);
CREATE INDEX IF NOT EXISTS idx_spatial_layers_props ON spatial_layers USING GIN (properties);

-- ============================================================
-- 3. DADOS IBGE / SIDRA (PIB, PAM, PEVS, BDiA)
-- ============================================================
CREATE TABLE IF NOT EXISTS ibge_data (
    id SERIAL PRIMARY KEY,
    source_table VARCHAR(20) NOT NULL,       -- e.g. '5938', '1419', '289'
    source_name VARCHAR(100) NOT NULL,       -- e.g. 'PIB Municipal', 'PAM', 'PEVS'
    territorial_level VARCHAR(5) NOT NULL,   -- '1'=Brasil, '2'=UF, '3'=Municipio
    ibge_code VARCHAR(20),
    period VARCHAR(20),
    variable_code VARCHAR(20),
    variable_name VARCHAR(200),
    value NUMERIC,
    unit VARCHAR(50),
    municipality_name VARCHAR(200),
    state_code VARCHAR(5),
    raw_data JSONB DEFAULT '{}',
    fetched_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ibge_source ON ibge_data (source_table);
CREATE INDEX IF NOT EXISTS idx_ibge_territory ON ibge_data (territorial_level, ibge_code);
CREATE INDEX IF NOT EXISTS idx_ibge_period ON ibge_data (period);
CREATE INDEX IF NOT EXISTS idx_ibge_state ON ibge_data (state_code);

-- ============================================================
-- 4. DADOS ANP (Petroleo, Gas, Biocombustiveis, Reservas)
-- ============================================================
CREATE TABLE IF NOT EXISTS anp_data (
    id SERIAL PRIMARY KEY,
    dataset_key VARCHAR(50) NOT NULL,        -- 'producao_petroleo', 'biocombustiveis', etc.
    uf VARCHAR(5),
    period VARCHAR(20),
    product VARCHAR(100),
    value NUMERIC,
    unit VARCHAR(50),
    raw_data JSONB DEFAULT '{}',
    fetched_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_anp_dataset ON anp_data (dataset_key);
CREATE INDEX IF NOT EXISTS idx_anp_uf ON anp_data (uf);
CREATE INDEX IF NOT EXISTS idx_anp_period ON anp_data (period);

-- ============================================================
-- 5. MAPBIOMAS (Uso e Cobertura do Solo)
-- ============================================================
CREATE TABLE IF NOT EXISTS mapbiomas_data (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    land_use_class INTEGER,
    land_use_name VARCHAR(200),
    area_ha NUMERIC,
    municipality_code VARCHAR(20),
    state VARCHAR(5),
    biome VARCHAR(50),
    geom GEOMETRY(Geometry, 4326),
    raw_data JSONB DEFAULT '{}',
    fetched_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_mapbiomas_geom ON mapbiomas_data USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_mapbiomas_year ON mapbiomas_data (year);
CREATE INDEX IF NOT EXISTS idx_mapbiomas_state ON mapbiomas_data (state);

-- ============================================================
-- 6. TERRABRASILIS / INPE (Desmatamento PRODES/DETER)
-- ============================================================
CREATE TABLE IF NOT EXISTS terrabrasilis_data (
    id SERIAL PRIMARY KEY,
    program VARCHAR(20) NOT NULL,            -- 'PRODES' or 'DETER'
    year INTEGER,
    state VARCHAR(5),
    municipality VARCHAR(200),
    area_km2 NUMERIC,
    biome VARCHAR(50),
    geom GEOMETRY(Geometry, 4326),
    raw_data JSONB DEFAULT '{}',
    fetched_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_terra_geom ON terrabrasilis_data USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_terra_program ON terrabrasilis_data (program);
CREATE INDEX IF NOT EXISTS idx_terra_year ON terrabrasilis_data (year);

-- ============================================================
-- 7. EPE (Sistema Energetico + BEN)
-- ============================================================
CREATE TABLE IF NOT EXISTS epe_data (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,             -- 'webmap', 'ben'
    category VARCHAR(100),                   -- 'usina', 'linha_transmissao', 'subestacao'
    name VARCHAR(300),
    energy_type VARCHAR(100),
    capacity_mw NUMERIC,
    state VARCHAR(5),
    geom GEOMETRY(Geometry, 4326),
    raw_data JSONB DEFAULT '{}',
    fetched_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_epe_geom ON epe_data USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_epe_source ON epe_data (source);
CREATE INDEX IF NOT EXISTS idx_epe_type ON epe_data (energy_type);

-- ============================================================
-- 8. ANEEL / SIGA (Geracao Eletrica)
-- ============================================================
CREATE TABLE IF NOT EXISTS aneel_data (
    id SERIAL PRIMARY KEY,
    plant_name VARCHAR(300),
    plant_type VARCHAR(100),                 -- 'UHE', 'PCH', 'EOL', 'UFV', 'UTE'
    fuel_source VARCHAR(100),
    capacity_kw NUMERIC,
    status VARCHAR(50),                      -- 'Operacao', 'Construcao', 'Outorgada'
    state VARCHAR(5),
    municipality VARCHAR(200),
    geom GEOMETRY(Point, 4326),
    raw_data JSONB DEFAULT '{}',
    fetched_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_aneel_geom ON aneel_data USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_aneel_type ON aneel_data (plant_type);
CREATE INDEX IF NOT EXISTS idx_aneel_status ON aneel_data (status);
CREATE INDEX IF NOT EXISTS idx_aneel_state ON aneel_data (state);

-- ============================================================
-- 9. CONAB (Agropecuaria)
-- ============================================================
CREATE TABLE IF NOT EXISTS conab_data (
    id SERIAL PRIMARY KEY,
    product VARCHAR(100) NOT NULL,
    harvest_year VARCHAR(20),
    state VARCHAR(5),
    area_planted_ha NUMERIC,
    production_tons NUMERIC,
    yield_kg_ha NUMERIC,
    raw_data JSONB DEFAULT '{}',
    fetched_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_conab_product ON conab_data (product);
CREATE INDEX IF NOT EXISTS idx_conab_state ON conab_data (state);

-- ============================================================
-- 10. DADOS INTERNACIONAIS (World Bank, IRENA, World Steel)
-- ============================================================
CREATE TABLE IF NOT EXISTS international_data (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,             -- 'world_bank', 'irena', 'world_steel'
    indicator_code VARCHAR(100),
    indicator_name VARCHAR(300),
    country_code VARCHAR(10),
    country_name VARCHAR(100),
    year INTEGER,
    value NUMERIC,
    unit VARCHAR(50),
    raw_data JSONB DEFAULT '{}',
    fetched_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_intl_source ON international_data (source);
CREATE INDEX IF NOT EXISTS idx_intl_country ON international_data (country_code);
CREATE INDEX IF NOT EXISTS idx_intl_indicator ON international_data (indicator_code);
CREATE INDEX IF NOT EXISTS idx_intl_year ON international_data (year);

-- ============================================================
-- 11. ETL JOBS LOG (Pipeline tracking)
-- ============================================================
CREATE TABLE IF NOT EXISTS etl_jobs (
    id SERIAL PRIMARY KEY,
    job_id UUID DEFAULT gen_random_uuid(),
    source VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',    -- 'pending', 'running', 'success', 'failed'
    records_processed INTEGER DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_etl_status ON etl_jobs (status);
CREATE INDEX IF NOT EXISTS idx_etl_source ON etl_jobs (source);

-- ============================================================
-- 12. CACHE TABLE (API responses cache)
-- ============================================================
CREATE TABLE IF NOT EXISTS api_cache (
    cache_key VARCHAR(500) PRIMARY KEY,
    response_data JSONB NOT NULL,
    source VARCHAR(100) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cache_expires ON api_cache (expires_at);
CREATE INDEX IF NOT EXISTS idx_cache_source ON api_cache (source);

-- ============================================================
-- Insert initial cluster data with geometry
-- ============================================================
INSERT INTO clusters (id, name, region, state, port, vocations, energy_sources, critical_minerals, hydrogen_potential, description, geom) VALUES
('norte-belem', 'Cluster Norte — Belém / Barcarena', 'Norte', 'PA', 'Porto de Vila do Conde (Barcarena)', ARRAY['Alumínio de baixo carbono','Bioeconomia amazônica','Processamento de minerais críticos'], ARRAY['Hidrelétrica (Tucuruí, Belo Monte)','Biomassa florestal','Potencial eólico em expansão'], ARRAY['Bauxita/Alumínio','Manganês','Cobre','Nióbio'], 'Médio — base hidrelétrica viabiliza eletrólise verde a custo competitivo', 'Vocação para produção de alumínio de baixo carbono e bioeconomia amazônica.', ST_SetSRID(ST_MakePoint(-48.5024, -1.4558), 4326)),
('nordeste-pecem', 'Cluster Nordeste — Pecém (CE)', 'Nordeste', 'CE', 'Porto do Pecém (CIPP)', ARRAY['Aço verde (H2-DRI)','Cimento de baixo carbono','Hub de Hidrogênio Verde'], ARRAY['Eólica onshore','Solar fotovoltaica','Hub H2V integrado'], ARRAY['Silício metálico','Calcário','Ferro-esponja'], 'Altíssimo — 41% das iniciativas de H2 do Brasil no Ceará', 'Estratégico para aço, cimento e vidro integrado a hub de hidrogênio.', ST_SetSRID(ST_MakePoint(-38.7883, -3.5322), 4326)),
('nordeste-camacari', 'Cluster Nordeste — Camaçari (BA)', 'Nordeste', 'BA', 'Porto de Aratu / Porto de Salvador', ARRAY['Química verde','Fertilizantes sustentáveis','Transformação de minerais críticos'], ARRAY['Eólica onshore','Solar fotovoltaica','Gás natural (transição)'], ARRAY['Terras-raras','Cobre','Grafite','Silício'], 'Alto — integração com projetos de H2 para e-metanol e amônia verde', 'Maior complexo industrial e petroquímico do Nordeste.', ST_SetSRID(ST_MakePoint(-38.3247, -12.6996), 4326)),
('centro-oeste', 'Cluster Centro-Oeste — Agro-Industrial', 'Centro-Oeste', 'GO/MT/MS', 'Ferrovia Norte-Sul até Itaqui/Santos', ARRAY['Biometano','SAF','Etanol 2G','Bioenergia integrada'], ARRAY['Solar fotovoltaica','Biomassa','Biogás/biometano'], ARRAY['Nióbio (Goiás)','Níquel'], 'Médio — foco em biocombustíveis', 'Integração agropecuária para biometano a partir de resíduos.', ST_SetSRID(ST_MakePoint(-47.9292, -15.7801), 4326)),
('sul-rs', 'Cluster Sul — Porto Alegre / Rio Grande (RS)', 'Sul', 'RS', 'Porto de Rio Grande / Porto de Paranaguá', ARRAY['Indústria diversificada','Biogás e biometano','Eólica offshore'], ARRAY['Eólica onshore e offshore','Biogás','Hidrelétrica'], ARRAY['Carvão (transição)','Cobre'], 'Alto no longo prazo — potencial eólico offshore', 'Indústria diversa com enorme potencial eólico offshore.', ST_SetSRID(ST_MakePoint(-51.2177, -30.0346), 4326)),
('sudeste-sp', 'Cluster Sudeste — São Paulo', 'Sudeste', 'SP', 'Porto de Santos', ARRAY['Bioenergia e etanol','Inovação e P&D','SAF','Eletrificação automotiva'], ARRAY['Bioenergia (cana)','Solar distribuída','Hidrelétrica'], ARRAY['Silício','Lítio (processamento)'], 'Médio — foco em biocombustíveis e SAF', 'Bioenergia, etanol e inovação. Porto de Santos é o maior da América Latina.', ST_SetSRID(ST_MakePoint(-46.6333, -23.5505), 4326)),
('sudeste-mg', 'Cluster Sudeste — Minas Gerais', 'Sudeste', 'MG', 'EFVM até Porto de Tubarão (ES)', ARRAY['Mineração sustentável','Aço verde','Lítio','Polissilício fotovoltaico'], ARRAY['Hidrelétrica','Solar fotovoltaica','Biomassa (carvão vegetal)'], ARRAY['Lítio','Nióbio','Grafite','Terras-raras','Ferro'], 'Alto — Centro de Hidrogênio Verde de Itajubá', 'Vale do Lítio estratégico para baterias. Polissilício com 6x menos emissões.', ST_SetSRID(ST_MakePoint(-43.9345, -19.9167), 4326)),
('sudeste-es', 'Cluster Sudeste — Espírito Santo', 'Sudeste', 'ES', 'Porto de Tubarão / Porto de Vitória', ARRAY['Pelotização (baixo carbono)','Celulose e papel'], ARRAY['Hidrelétrica','Solar','Gás natural (transição)'], ARRAY['Ferro (pelotização)','Grafite'], 'Médio — ligado à descarbonização da pelotização', 'Porto de Tubarão — um dos maiores do mundo para minério de ferro.', ST_SetSRID(ST_MakePoint(-40.3128, -20.3155), 4326)),
('sudeste-rj', 'Cluster Sudeste — Rio de Janeiro', 'Sudeste', 'RJ', 'Porto de Sepetiba (Itaguaí)', ARRAY['Petroquímica em transição','Siderurgia baixo carbono','Eólica offshore','CCUS'], ARRAY['Gás natural (transição)','Eólica offshore','Pré-sal'], ARRAY['Ferro','Manganês'], 'Alto — combustível-chave para transição petroquímica', 'Integração da cadeia de petróleo e gás com vetores verdes.', ST_SetSRID(ST_MakePoint(-43.1729, -22.9068), 4326))
ON CONFLICT (id) DO NOTHING;

-- ============================================================
-- Verification
-- ============================================================
DO $$
BEGIN
    RAISE NOTICE '=== PowerShoring Analytics — Schema Initialized ===';
    RAISE NOTICE 'PostGIS version: %', PostGIS_Version();
    RAISE NOTICE 'Tables created: clusters, spatial_layers, ibge_data, anp_data, mapbiomas_data, terrabrasilis_data, epe_data, aneel_data, conab_data, international_data, etl_jobs, api_cache';
    RAISE NOTICE 'GiST indexes: 7 spatial indexes created';
    RAISE NOTICE 'Clusters seeded: 9 industrial clusters with geometry';
END $$;
