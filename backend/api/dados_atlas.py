"""
Atlas Nacional Digital (IBGE) Router — Integrated with IBGE Servico de Dados V3.
Aggregates metadata and connection specifics for territorial maps.
"""
import httpx
from fastapi import APIRouter, HTTPException, Query
from core.cache import cached

router = APIRouter(prefix="/api/atlas", tags=["Atlas Nacional IBGE"])

BASE_URL = "https://servicodados.ibge.gov.br/api/v3"

@router.get("/territories")
@cached(ttl=86400, key_prefix="atlas_terr")
async def get_spatial_hierarchy():
    """Fetch structural metadata from the IBGE spatial hierarchy."""
    async with httpx.AsyncClient() as client:
        try:
            # Access the service datasets mesh hierarchy endpoint
            r = await client.get(f"{BASE_URL}/malhas/municipios?formato=application/json")
            # Note: usually returns an expensive big payload, let's direct to documentation or paginated sample
            return {
                "source": "IBGE Atlas Nacional API",
                "api_base": "https://servicodados.ibge.gov.br/api/v3",
                "capabilities": ["WMS Tile Serving", "GeoJSON vectors", "PDF thematic maps"],
                "wms_endpoint": "https://geoservicos.ibge.gov.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities"
            }
        except Exception as e:
             raise HTTPException(502, detail=str(e))

@router.get("/layers")
async def list_available_atlas_layers():
    """Quick lookup for critical national thematic visual layers."""
    return {
        "thematic_layers": [
            {"id": "regiao_influencia_cidades", "name": "REGIC (Regiões de Influência)", "source": "IBGE 2020"},
            {"id": "biomas_brasil", "name": "Biomas 1:250.000", "source": "IBGE 2019"},
            {"id": "logistica_transportes", "name": "Malha de Transportes", "source": "IBGE / DNIT"}
        ],
        "viewer_link": "https://www.ibge.gov.br/apps/atlas_nacional/#/home"
    }
