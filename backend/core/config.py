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
        # Ambiental & Fundiario
        "unidades_conservacao": "Unidades_Conservacao/FeatureServer/0/query",
        "terras_indigenas": "Terras_Indigenas/FeatureServer/0/query",
        "terras_quilombolas": "Terras_Quilombolas/FeatureServer/0/query",
        "pastagens_inter": "areas_potenciais_inter/FeatureServer/0/query",
        "pastagens_severa": "areas_potenciais_severa/FeatureServer/0/query",
        # Infraestrutura (Infraestruturas_WFL1 multi-layer)
        "portos": "Infraestruturas_WFL1/FeatureServer/0/query",
        "aeroportos": "Infraestruturas_WFL1/FeatureServer/1/query",
        "estradas": "Infraestruturas_WFL1/FeatureServer/2/query",
        "hidrovias": "Infraestruturas_WFL1/FeatureServer/3/query",
        "ferrovias": "Infraestruturas_WFL1/FeatureServer/4/query",
        # Energia
        "hubs_h2": "Hubs_H2/FeatureServer/1/query",
        "minerais_criticos": "Minerais_Criticos/FeatureServer/0/query",
        "solar_uv_existente": "Solar_UFV/FeatureServer/0/query",
        "solar_uv_planejada": "Solar_UFV/FeatureServer/1/query",
    }


settings = Settings()
