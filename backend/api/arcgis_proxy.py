"""
ArcGIS Proxy Router — Consumes PID FeatureServer endpoints in real-time.
Proxies requests to services6.arcgis.com and returns GeoJSON to the frontend.
"""
import httpx
from fastapi import APIRouter, HTTPException, Query

from core.config import settings
from core.clusters_data import LAYER_CATALOG

router = APIRouter(prefix="/api/layers", tags=["ArcGIS Layers"])

# Shared async HTTP client
_client: httpx.AsyncClient | None = None


async def get_client() -> httpx.AsyncClient:
    """Lazy-init a shared httpx async client."""
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=60.0)
    return _client


async def close_client():
    """Explicitly close the shared httpx client on shutdown to prevent leaks."""
    global _client
    if _client is not None and not _client.is_closed:
        await _client.aclose()


@router.get("/catalog")
async def list_available_layers():
    """Return metadata about all available map layers."""
    return {"layers": LAYER_CATALOG}


@router.get("/{layer_key}")
async def get_layer_geojson(
    layer_key: str,
    result_offset: int = Query(0, ge=0, description="Pagination offset"),
    result_record_count: int = Query(2000, ge=1, le=5000, description="Max features"),
    where: str = Query("1=1", description="SQL WHERE clause for filtering"),
):
    """
    Fetch GeoJSON from a specific ArcGIS FeatureServer layer.
    Uses the PID's real ESRI endpoints (reverse-engineered).
    """
    if layer_key not in settings.ARCGIS_LAYERS:
        available = list(settings.ARCGIS_LAYERS.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Layer '{layer_key}' not found. Available: {available}",
        )

    layer_path = settings.ARCGIS_LAYERS[layer_key]
    url = (
        f"{settings.ARCGIS_BASE_URL}/{layer_path}"
        f"?where={where}"
        f"&outFields=*"
        f"&resultOffset={result_offset}"
        f"&resultRecordCount={result_record_count}"
        f"&f=geojson"
    )

    client = await get_client()
    try:
        response = await client.get(url)
        response.raise_for_status()
        geojson = response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"ArcGIS returned error: {exc.response.text[:500]}",
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to connect to ArcGIS: {str(exc)}",
        )

    feature_count = len(geojson.get("features", []))
    return {
        "layer": layer_key,
        "feature_count": feature_count,
        "source": "PID ArcGIS FeatureServer (real-time)",
        "geojson": geojson,
    }
