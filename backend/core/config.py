"""PowerShoring Analytics — Core Configuration"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # --- App ---
    APP_NAME: str = "PowerShoring Analytics API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # --- Database (PostGIS) ---
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://powershoring:powershoring@localhost:5432/powershoring_db"
    )

    # --- Redis ---
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # --- ArcGIS PID ---
    ARCGIS_BASE_URL: str = (
        "https://services6.arcgis.com/I9CTS4kjOw8Dsslu/arcgis/rest/services"
    )
    ARCGIS_QUERY_PARAMS: str = "?where=1%3D1&outFields=*&f=geojson"

    # --- OpenAI ---
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")

    # --- Firebase ---
    FIREBASE_BUCKET: str = os.getenv("FIREBASE_BUCKET", "")

    # --- CORS ---
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

    # --- ArcGIS Layer Registry (from PID_REAL_APIS.md) ---
    ARCGIS_LAYERS: dict[str, str] = {
        # --- Ambiental & Fundiario ---
        "unidades_conservacao": "Unidades_Conservacao/FeatureServer/0/query",
        "terras_indigenas": "Terras_Indigenas/FeatureServer/0/query",
        "terras_quilombolas": "Terras_Quilombolas/FeatureServer/0/query",
        "pastagens_inter": "areas_potenciais_inter/FeatureServer/0/query",
        "pastagens_severa": "areas_potenciais_severa/FeatureServer/0/query",
        
        # --- Infraestrutura (Logística) ---
        "portos": "Infraestruturas_WFL1/FeatureServer/0/query",
        "aeroportos": "Infraestruturas_WFL1/FeatureServer/1/query",
        "estradas": "Infraestruturas_WFL1/FeatureServer/2/query",
        "hidrovias": "Infraestruturas_WFL1/FeatureServer/3/query",
        "ferrovias": "Infraestruturas_WFL1/FeatureServer/4/query",
        "instalacoes_portuarias": "Instala%C3%A7%C3%B5es_Portu%C3%A1rias/FeatureServer/0/query",
        
        # --- Minerais Críticos & Terras Raras ---
        "minerais_criticos": "Minerais_Criticos/FeatureServer/0/query",
        "terras_raras": "Minerais_de_Transi%C3%A7%C3%A3o/FeatureServer/0/query",  # Target layer for critical elements
        
        # --- Matriz Energética (Energias Limpas) ---
        "hubs_h2": "Hubs_H2/FeatureServer/1/query",
        "solar_uv_existente": "Solar_UFV_existente/FeatureServer/1/query",  # Confirmed Layer 1
        "solar_uv_planejada": "Solar_UFV_planejada/FeatureServer/1/query",  # Confirmed Layer 1
        "eolica_existente": "E%C3%B3lica_Existente/FeatureServer/1/query",
        "eolica_planejada": "E%C3%B3lica_planejada/FeatureServer/1/query",
        
        # Hidrelétricas (PCH, UHE, CGH)
        "hidro_pch_existente": "Hidrel%C3%A9trica_PCH_existente/FeatureServer/1/query",
        "hidro_uhe_existente": "Hidrel%C3%A9trica_UHE_existente/FeatureServer/1/query",
        "hidro_cgh_existente": "Hidroel%C3%A9trica_CGH_existente/FeatureServer/1/query",
        
        # Outros & Sistemas
        "biomassa_existentes": "Biomassa_existentes/FeatureServer/1/query",
        "biomassa_planejada": "Biomassa_planejada/FeatureServer/1/query",
        "biometano_comercial": "Biometano_Comercial_/FeatureServer/0/query",
        "sistemas_isolados": "Sistemas_Isolados/FeatureServer/1/query",
    }


settings = Settings()
