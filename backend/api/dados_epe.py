"""
EPE (Empresa de Pesquisa Energética) Data Router — Proxy for WebMap REST API.
Consumes actual FeatureServer/MapServer from EPE.
"""
import httpx
from fastapi import APIRouter, HTTPException, Query
from core.cache import cached

router = APIRouter(prefix="/api/epe", tags=["EPE"])

EPE_ARCGIS_BASE = "https://gisepeprd2.epe.gov.br/arcgis/rest/services"

# Known Layer Folders in EPE GIS
LAYER_MAPPING = {
    "usinas": "WebMapEPE/Usinas_Existentes/MapServer/0",
    "linhas": "WebMapEPE/Sistema_Transmissao/MapServer/0",
    "subestacoes": "WebMapEPE/Subestacoes/MapServer/0",
    "geracao_distribuida": "WebMapEPE/Geracao_Distribuida/MapServer/0"
}

@router.get("/layers")
async def list_layers():
    """Return available EPE geo layers shortcuts."""
    return {
        "available_shortcuts": list(LAYER_MAPPING.keys()),
        "base_url": EPE_ARCGIS_BASE
    }

@router.get("/query/{shortcut}")
@cached(ttl=3600, key_prefix="epe_gis")
async def query_epe_layer(
    shortcut: str,
    where: str = Query("1=1", description="SQL filter clause"),
    out_fields: str = Query("*", description="Comma-separated fields")
):
    """Proxy dynamic query to EPE ArcGIS Server."""
    if shortcut not in LAYER_MAPPING:
        raise HTTPException(status_code=404, detail="Shortcut mapping not defined")
    
    service_path = LAYER_MAPPING[shortcut]
    url = f"{EPE_ARCGIS_BASE}/{service_path}/query"
    
    params = {
        "where": where,
        "outFields": out_fields,
        "f": "geojson",
        "resultRecordCount": 100,
        "returnGeometry": "true"
    }
    
    async with httpx.AsyncClient(verify=False) as client: # EPE often has cert caveats
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"EPE ArcGIS Server Error: {str(e)}")

@router.get("/ben")
@cached(ttl=86400, key_prefix="epe_ben")
async def get_ben_summary():
    """Shortcut metadata regarding Balanço Energético Nacional availability."""
    return {
        "source": "EPE - Balanço Energético Nacional",
        "type": "Yearly Publication",
        "open_data_portal": "https://www.epe.gov.br/dados-abertos",
        "note": "Data parsed via bulk file load into PowerShoring database."
    }
