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
    Fetch GeoJSON from cache if available, otherwise iterate ArcGIS PID FeatureServer.
    """
    if layer_key not in settings.ARCGIS_LAYERS:
        available = list(settings.ARCGIS_LAYERS.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Layer '{layer_key}' not found. Available: {available}",
        )

    from sqlalchemy import text
    from core.database import get_sync_engine
    
    # --- FAST PATH: CHECK LOCAL POSTGIS CACHE ---
    engine = get_sync_engine()
    with engine.connect() as conn:
        count = conn.execute(
            text("SELECT count(*) FROM spatial_layers WHERE layer_key = :k"),
            {"k": layer_key}
        ).scalar()
        
        if count > 0:
            # Reconstruct GeoJSON directly inside PostGIS for maximum speed
            sql = text("""
                SELECT jsonb_build_object(
                    'type',     'FeatureCollection',
                    'features', jsonb_agg(features.feature)
                )
                FROM (
                  SELECT jsonb_build_object(
                    'type',       'Feature',
                    'geometry',   ST_AsGeoJSON(geom)::jsonb,
                    'properties', properties
                  ) AS feature
                  FROM spatial_layers
                  WHERE layer_key = :k
                ) AS features
            """)
            res = conn.execute(sql, {"k": layer_key}).scalar()
            
            return {
                "layer": layer_key,
                "feature_count": count,
                "source": "Fast-Path PostGIS Local Cache",
                "geojson": res
            }

    # --- SLOW PATH: FALLBACK TO RECURSIVE ARCGIS FETCH ---
    layer_path = settings.ARCGIS_LAYERS[layer_key]
    url = f"{settings.ARCGIS_BASE_URL}/{layer_path}"
    
    all_features = []
    offset = result_offset
    # Hardcode limit internal iteration for performance safety on first fetch
    MAX_ITERATIONS = 5 
    iterations = 0
    
    client = await get_client()
    
    try:
        while iterations < MAX_ITERATIONS:
            call_url = (
                f"{url}?where={where}&outFields=*&f=geojson"
                f"&resultOffset={offset}&resultRecordCount={result_record_count}"
            )
            
            response = await client.get(call_url)
            response.raise_for_status()
            data = response.json()
            
            feats = data.get("features", [])
            all_features.extend(feats)
            
            # Stop if end of set reached
            if len(feats) < result_record_count:
                break
                
            # Check ESRI Exceeded flag if available
            exceeded = data.get("properties", {}).get("exceededTransferLimit", False)
            if not exceeded and len(feats) < result_record_count:
                 break
                 
            offset += result_record_count
            iterations += 1

        final_geojson = {
            "type": "FeatureCollection",
            "features": all_features
        }
        
        return {
            "layer": layer_key,
            "feature_count": len(all_features),
            "source": "PID ArcGIS FeatureServer (Aggregated)",
            "geojson": final_geojson,
        }

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
