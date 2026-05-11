"""
Real cluster data from the Atlas do Futuro Industrial do Brasil 2025.
This is NOT mocked data — these are the official clusters identified in the Atlas.
"""

CLUSTERS_DATA: list[dict] = [
    {
        "id": "norte-belem",
        "name": "Cluster Norte — Belém / Barcarena",
        "region": "Norte",
        "state": "PA",
        "lat": -1.4558,
        "lng": -48.5024,
        "port": "Porto de Vila do Conde (Barcarena)",
        "vocations": [
            "Alumínio de baixo carbono",
            "Bioeconomia amazônica",
            "Processamento de minerais críticos",
        ],
        "energy_sources": [
            "Hidrelétrica (Tucuruí, Belo Monte)",
            "Biomassa florestal",
            "Potencial eólico em expansão",
        ],
        "critical_minerals": ["Bauxita/Alumínio", "Manganês", "Cobre", "Nióbio"],
        "hydrogen_potential": "Médio — base hidrelétrica viabiliza eletrólise verde a custo competitivo",
        "description": (
            "Vocação para a produção de alumínio de baixo carbono e bioeconomia amazônica, "
            "com forte base de eletricidade renovável e potencial para expansão de geração eólica. "
            "O Porto de Vila do Conde viabiliza exportação de commodities verdes."
        ),
    },
    {
        "id": "nordeste-pecem",
        "name": "Cluster Nordeste — Pecém (CE)",
        "region": "Nordeste",
        "state": "CE",
        "lat": -3.5322,
        "lng": -38.7883,
        "port": "Porto do Pecém (CIPP)",
        "vocations": [
            "Aço verde (H2-DRI)",
            "Cimento de baixo carbono",
            "Vidro sustentável",
            "Hub de Hidrogênio Verde",
        ],
        "energy_sources": [
            "Eólica onshore (abundante)",
            "Solar fotovoltaica",
            "Hub H2V integrado",
        ],
        "critical_minerals": ["Silício metálico", "Calcário", "Ferro-esponja (importado)"],
        "hydrogen_potential": (
            "Altíssimo — 41% das iniciativas de H2 do Brasil concentradas no Ceará. "
            "O CIPP já abriga projetos-piloto de hidrogênio verde com parceiros internacionais."
        ),
        "description": (
            "Estratégico para indústrias de aço, cimento e vidro, integrado diretamente a um "
            "robusto hub de hidrogênio de baixa emissão de carbono. "
            "66,7% das iniciativas de H2 do Brasil estão no Nordeste."
        ),
    },
    {
        "id": "nordeste-camacari",
        "name": "Cluster Nordeste — Camaçari (BA)",
        "region": "Nordeste",
        "state": "BA",
        "lat": -12.6996,
        "lng": -38.3247,
        "port": "Porto de Aratu / Porto de Salvador",
        "vocations": [
            "Química verde (e-metanol, amônia verde)",
            "Fertilizantes sustentáveis",
            "Transformação de minerais críticos",
        ],
        "energy_sources": [
            "Eólica onshore",
            "Solar fotovoltaica",
            "Gás natural (transição)",
        ],
        "critical_minerals": ["Terras-raras", "Cobre", "Grafite", "Silício"],
        "hydrogen_potential": (
            "Alto — integração com projetos de H2 visa substituir insumos fósseis na "
            "produção de e-metanol e amônia verde, com forte apoio logístico portuário."
        ),
        "description": (
            "Maior complexo industrial e petroquímico do Nordeste. Polo focado na indústria "
            "química verde e na transformação de minerais críticos, suportado por malha "
            "ferroviária e portos estratégicos como o de Aratu."
        ),
    },
    {
        "id": "centro-oeste",
        "name": "Cluster Centro-Oeste — Agro-Industrial",
        "region": "Centro-Oeste",
        "state": "GO/MT/MS",
        "lat": -15.7801,
        "lng": -47.9292,
        "port": "Escoamento via ferrovias (Ferrovia Norte-Sul) até Itaqui/Santos",
        "vocations": [
            "Biometano a partir de resíduos agropecuários",
            "SAF (Combustível Sustentável de Aviação)",
            "Etanol 2G",
            "Bioenergia integrada",
        ],
        "energy_sources": [
            "Solar fotovoltaica (alta irradiação)",
            "Biomassa (resíduos de soja, milho, cana)",
            "Biogás/biometano",
        ],
        "critical_minerals": ["Nióbio (Goiás — maior reserva global)", "Níquel"],
        "hydrogen_potential": "Médio — foco principal em biocombustíveis, não em eletrólise",
        "description": (
            "Focado na integração agropecuária para a produção de biometano a partir de resíduos, "
            "fornecendo combustível renovável para as indústrias químicas, cimenteiras e de alimentos. "
            "Brasil possui 55-60 milhões de hectares aptos para biomassa sustentável via "
            "recuperação de pastagens degradadas."
        ),
    },
    {
        "id": "sul-rs",
        "name": "Cluster Sul — Porto Alegre / Rio Grande (RS)",
        "region": "Sul",
        "state": "RS",
        "lat": -30.0346,
        "lng": -51.2177,
        "port": "Porto de Rio Grande / Porto de Paranaguá",
        "vocations": [
            "Indústria diversificada",
            "Biogás e biometano",
            "Eólica offshore",
            "Substituição de carvão mineral",
        ],
        "energy_sources": [
            "Eólica onshore e offshore (enorme potencial)",
            "Biogás (resíduos agropecuários)",
            "Hidrelétrica",
        ],
        "critical_minerals": ["Carvão (em transição para abandono)", "Cobre"],
        "hydrogen_potential": (
            "Alto no longo prazo — potencial eólico offshore cria condições estruturais "
            "para produção em larga escala de H2 verde, substituindo termelétricas a carvão."
        ),
        "description": (
            "Focado na indústria diversa aliada ao enorme potencial eólico onshore e offshore "
            "e produção de biogás. A transição justa aqui visa substituir o carvão mineral "
            "das termelétricas por fontes renováveis, gerando empregos verdes."
        ),
    },
    {
        "id": "sudeste-sp",
        "name": "Cluster Sudeste — São Paulo",
        "region": "Sudeste",
        "state": "SP",
        "lat": -23.5505,
        "lng": -46.6333,
        "port": "Porto de Santos",
        "vocations": [
            "Bioenergia e etanol",
            "Inovação e P&D",
            "SAF (hub de aviação sustentável)",
            "Indústria automotiva (eletrificação)",
        ],
        "energy_sources": [
            "Bioenergia (cana-de-açúcar — 16,9% da matriz)",
            "Solar distribuída",
            "Hidrelétrica",
        ],
        "critical_minerals": ["Silício", "Lítio (processamento)"],
        "hydrogen_potential": "Médio — foco em biocombustíveis e SAF mais que em H2 direto",
        "description": (
            "Reúne bioenergia, etanol e inovação. O Porto de Santos é o maior da América Latina. "
            "O estado concentra P&D para SAF e eletrificação de frotas, "
            "sendo polo de referência para a transição da mobilidade sustentável."
        ),
    },
    {
        "id": "sudeste-mg",
        "name": "Cluster Sudeste — Minas Gerais",
        "region": "Sudeste",
        "state": "MG",
        "lat": -19.9167,
        "lng": -43.9345,
        "port": "Escoamento via EFVM até Porto de Tubarão (ES)",
        "vocations": [
            "Mineração sustentável",
            "Aço verde",
            "Processamento de lítio",
            "Polissilício fotovoltaico",
        ],
        "energy_sources": [
            "Hidrelétrica",
            "Solar fotovoltaica",
            "Biomassa (carvão vegetal de florestas plantadas)",
        ],
        "critical_minerals": [
            "Lítio (Vale do Lítio — 7º global)",
            "Nióbio",
            "Grafite",
            "Terras-raras (3º produtor global)",
            "Ferro (2º produtor mundial)",
        ],
        "hydrogen_potential": (
            "Alto — Centro de Hidrogênio Verde de Itajubá como projeto-piloto. "
            "Potencial para descarbonizar siderurgia via H2-DRI."
        ),
        "description": (
            "Rotas de baixo carbono para mineração e aço. O Vale do Lítio é estratégico "
            "para baterias. O polissilício feito aqui gera 6x menos emissões que na China. "
            "Forte base de minerais críticos para a transição energética global."
        ),
    },
    {
        "id": "sudeste-es",
        "name": "Cluster Sudeste — Espírito Santo",
        "region": "Sudeste",
        "state": "ES",
        "lat": -20.3155,
        "lng": -40.3128,
        "port": "Porto de Tubarão / Porto de Vitória",
        "vocations": [
            "Diversificação industrial para exportação",
            "Pelotização de minério (baixo carbono)",
            "Celulose e papel",
        ],
        "energy_sources": [
            "Hidrelétrica",
            "Solar",
            "Gás natural (transição)",
        ],
        "critical_minerals": ["Ferro (pelotização)", "Grafite"],
        "hydrogen_potential": "Médio — potencial ligado à descarbonização da pelotização",
        "description": (
            "Forte diversificação industrial para exportação. O Porto de Tubarão é um "
            "dos maiores do mundo para minério de ferro. Foco em pelotização de baixo "
            "carbono e indústria de celulose sustentável."
        ),
    },
    {
        "id": "sudeste-rj",
        "name": "Cluster Sudeste — Rio de Janeiro",
        "region": "Sudeste",
        "state": "RJ",
        "lat": -22.9068,
        "lng": -43.1729,
        "port": "Porto de Sepetiba (Itaguaí) / Porto do Rio",
        "vocations": [
            "Petroquímica em transição verde",
            "Siderurgia de baixo carbono",
            "Eólica offshore",
            "CCUS (captura de carbono)",
        ],
        "energy_sources": [
            "Gás natural (transição)",
            "Eólica offshore (em planejamento)",
            "Pré-sal (geração de receita para investimento verde)",
        ],
        "critical_minerals": ["Ferro", "Manganês"],
        "hydrogen_potential": (
            "Alto — combustível-chave para consolidar a transição da petroquímica "
            "e siderurgia fluminense no médio/longo prazo."
        ),
        "description": (
            "Integração estratégica da cadeia de petróleo e gás com vetores verdes. "
            "O hidrogênio de baixo carbono é visto como combustível-chave para "
            "consolidar a transição energética das indústrias pesadas fluminenses."
        ),
    },
]


# Layer display metadata for the frontend
LAYER_CATALOG: list[dict] = [
    # Logistica
    {"layer_key": "portos", "display_name": "Portos Organizados", "category": "Logistica", "icon": "anchor"},
    {"layer_key": "instalacoes_portuarias", "display_name": "Instalações Portuárias", "category": "Logistica", "icon": "ship-wheel"},
    {"layer_key": "aeroportos", "display_name": "Aeroportos", "category": "Logistica", "icon": "plane"},
    {"layer_key": "estradas", "display_name": "Estradas Nacionais", "category": "Logistica", "icon": "road"},
    {"layer_key": "hidrovias", "display_name": "Hidrovias", "category": "Logistica", "icon": "ship"},
    {"layer_key": "ferrovias", "display_name": "Ferrovias", "category": "Logistica", "icon": "train"},
    
    # Energia Renovavel
    {"layer_key": "solar_uv_existente", "display_name": "Solar (Existente)", "category": "Energia", "icon": "sun"},
    {"layer_key": "solar_uv_planejada", "display_name": "Solar (Planejada)", "category": "Energia", "icon": "sun-dim"},
    {"layer_key": "eolica_existente", "display_name": "Eólica (Existente)", "category": "Energia", "icon": "wind"},
    {"layer_key": "eolica_planejada", "display_name": "Eólica (Planejada)", "category": "Energia", "icon": "fan"},
    {"layer_key": "hubs_h2", "display_name": "Hubs de Hidrogênio", "category": "Energia", "icon": "flask-conical"},
    
    # Hidroeletricas
    {"layer_key": "hidro_uhe_existente", "display_name": "UHE (Hidro Existente)", "category": "Energia", "icon": "droplets"},
    {"layer_key": "hidro_pch_existente", "display_name": "PCH (Pequenas Centrais)", "category": "Energia", "icon": "droplet"},
    
    # BioEnergia & Outros
    {"layer_key": "biomassa_existentes", "display_name": "Biomassa Existente", "category": "Energia", "icon": "sprout"},
    {"layer_key": "biometano_comercial", "display_name": "Biometano Comercial", "category": "Energia", "icon": "flame"},
    {"layer_key": "sistemas_isolados", "display_name": "Sistemas Isolados", "category": "Energia", "icon": "battery"},
    
    # Recursos & Minerais
    {"layer_key": "minerais_criticos", "display_name": "Minerais Críticos", "category": "Recursos", "icon": "gem"},
    {"layer_key": "terras_raras", "display_name": "Terras Raras", "category": "Recursos", "icon": "mountain"},
    
    # Ambiental
    {"layer_key": "unidades_conservacao", "display_name": "Unidades de Conservação", "category": "Ambiental", "icon": "trees"},
    {"layer_key": "terras_indigenas", "display_name": "Terras Indígenas", "category": "Ambiental", "icon": "tent"},
    {"layer_key": "terras_quilombolas", "display_name": "Terras Quilombolas", "category": "Ambiental", "icon": "home"},
    {"layer_key": "pastagens_inter", "display_name": "Pastagens Degradadas (Inter.)", "category": "Ambiental", "icon": "leaf"},
    {"layer_key": "pastagens_severa", "display_name": "Pastagens Degradadas (Severa)", "category": "Ambiental", "icon": "alert-triangle"},
]
