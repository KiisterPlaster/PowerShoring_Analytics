"""
MapBiomas Integration Router — Access to land use/cover data.

Connection Strategies:
  1. ArcGIS ImageServer (PID) — raster tiles via REST
  2. WMS/WFS (GeoServer)    — standard OGC protocols
  3. Google Earth Engine     — earthengine-api (optional, requires auth)
  4. Direct download         — CSV/GeoJSON from MapBiomas workspace

Primary: Uses the PID's ArcGIS ImageServer endpoint (no auth required)
"""
import httpx
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/mapbiomas", tags=["MapBiomas - Uso do Solo"])

_client: httpx.AsyncClient | None = None


async def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=60.0)
    return _client


# ========================================================
# MapBiomas via PID ArcGIS ImageServer (primary connection)
# ========================================================
MAPBIOMAS_IMAGESERVER = (
    "https://ic.imagery1.arcgis.com/arcgis/rest/services/MapBiomas/ImageServer"
)

CO2_IMAGESERVER = (
    "https://tiledimageservices.arcgis.com/jIL9msH9OI208GCb/arcgis/rest/services"
    "/Global_Anthropogenic_CO2_Emissions_2018__tiled_/ImageServer"
)


@router.get("/info")
async def get_mapbiomas_info():
    """
    Get MapBiomas ImageServer metadata.
    Connection: ArcGIS REST API (JSON) — no authentication required.
    """
    client = await _get_client()
    try:
        response = await client.get(f"{MAPBIOMAS_IMAGESERVER}?f=json")
        response.raise_for_status()
        data = response.json()

        return {
            "source": "MapBiomas via PID ArcGIS ImageServer",
            "connection_type": "ArcGIS REST API (ImageServer)",
            "service_url": MAPBIOMAS_IMAGESERVER,
            "name": data.get("name", "MapBiomas"),
            "description": data.get("description", ""),
            "spatial_reference": data.get("spatialReference", {}),
            "extent": data.get("extent", {}),
            "band_count": data.get("bandCount", 0),
            "pixel_type": data.get("pixelType", ""),
            "raster_functions": [
                rf.get("name", "") for rf in data.get("rasterFunctionInfos", [])
            ],
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error connecting to MapBiomas ImageServer: {str(exc)}",
        )


@router.get("/identify")
async def identify_land_use(
    lat: float = Query(-14.235, description="Latitude"),
    lng: float = Query(-51.925, description="Longitude"),
    year: int = Query(2022, ge=1985, le=2023, description="Year of land use data"),
):
    """
    Identify land use/cover class at a specific point.
    Uses MapBiomas ImageServer identify endpoint.
    Connection: ArcGIS REST API identify operation.
    """
    client = await _get_client()
    try:
        url = f"{MAPBIOMAS_IMAGESERVER}/identify"
        params = {
            "geometry": f'{{"x":{lng},"y":{lat}}}',
            "geometryType": "esriGeometryPoint",
            "returnGeometry": "false",
            "returnCatalogItems": "false",
            "f": "json",
        }
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            "source": "MapBiomas ImageServer (identify)",
            "connection_type": "ArcGIS REST API",
            "coordinates": {"lat": lat, "lng": lng},
            "year": year,
            "pixel_value": data.get("value", "N/A"),
            "properties": data.get("properties", {}),
            "catalog_items": data.get("catalogItems", {}),
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error identifying land use: {str(exc)}",
        )


# ========================================================
# CO2 Emissions via PID ArcGIS ImageServer
# ========================================================
@router.get("/co2/info")
async def get_co2_info():
    """
    Get CO2 emissions raster metadata.
    Connection: ArcGIS TiledImageServer REST API.
    """
    client = await _get_client()
    try:
        response = await client.get(f"{CO2_IMAGESERVER}?f=json")
        response.raise_for_status()
        data = response.json()

        return {
            "source": "Global Anthropogenic CO2 Emissions 2018 (PID)",
            "connection_type": "ArcGIS TiledImageServer REST API",
            "service_url": CO2_IMAGESERVER,
            "name": data.get("name", "CO2 Emissions"),
            "description": data.get("description", ""),
            "spatial_reference": data.get("spatialReference", {}),
            "extent": data.get("extent", {}),
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error connecting to CO2 ImageServer: {str(exc)}",
        )


# ========================================================
# MapBiomas via WMS/WFS (GeoServer — secondary connection)
# ========================================================
MAPBIOMAS_WMS = "https://mapbiomas.org/geoserver/mapbiomas/wms"
MAPBIOMAS_WFS = "https://mapbiomas.org/geoserver/mapbiomas/wfs"


@router.get("/wms/capabilities")
async def get_wms_capabilities():
    """
    Get MapBiomas WMS capabilities.
    Connection: OGC WMS GetCapabilities (XML/JSON)
    Used in: QGIS integration, frontend tile layers.
    """
    client = await _get_client()
    try:
        params = {
            "service": "WMS",
            "version": "1.1.1",
            "request": "GetCapabilities",
        }
        response = await client.get(MAPBIOMAS_WMS, params=params)
        # WMS returns XML — we just report availability
        return {
            "source": "MapBiomas GeoServer (WMS)",
            "connection_type": "OGC WMS Protocol",
            "wms_url": MAPBIOMAS_WMS,
            "wfs_url": MAPBIOMAS_WFS,
            "status": "available" if response.status_code == 200 else "unavailable",
            "usage_note": (
                "WMS tiles can be consumed directly by Leaflet/MapLibre. "
                "WFS returns GeoJSON for vector analysis."
            ),
            "leaflet_integration": (
                f"L.tileLayer.wms('{MAPBIOMAS_WMS}', "
                "{ layers: 'mapbiomas:coverage', format: 'image/png', transparent: true })"
            ),
        }
    except Exception as exc:
        return {
            "source": "MapBiomas GeoServer (WMS)",
            "status": "unavailable",
            "error": str(exc),
        }


# ========================================================
# Connection Summary
# ========================================================
@router.get("/connections")
async def list_mapbiomas_connections():
    """Document all MapBiomas connection methods available."""
    return {
        "connections": [
            {
                "method": "ArcGIS ImageServer (PID)",
                "url": MAPBIOMAS_IMAGESERVER,
                "protocol": "REST API (JSON)",
                "auth": "None (public)",
                "status": "primary",
                "data_type": "Raster (land use/cover classification)",
            },
            {
                "method": "ArcGIS TiledImageServer (CO2)",
                "url": CO2_IMAGESERVER,
                "protocol": "REST API (JSON)",
                "auth": "None (public)",
                "status": "primary",
                "data_type": "Raster (CO2 emissions grid)",
            },
            {
                "method": "WMS (GeoServer)",
                "url": MAPBIOMAS_WMS,
                "protocol": "OGC WMS 1.1.1",
                "auth": "None (public)",
                "status": "secondary",
                "data_type": "Tile layer (use in Leaflet)",
            },
            {
                "method": "WFS (GeoServer)",
                "url": MAPBIOMAS_WFS,
                "protocol": "OGC WFS 2.0",
                "auth": "None (public)",
                "status": "secondary",
                "data_type": "Vector (GeoJSON features)",
            },
            {
                "method": "Google Earth Engine",
                "url": "https://earthengine.google.com/",
                "protocol": "earthengine-api (Python)",
                "auth": "Google Cloud credentials required",
                "status": "optional",
                "data_type": "Multi-temporal raster analysis",
                "note": "Requires: pip install earthengine-api && earthengine authenticate",
            },
        ]
    }
