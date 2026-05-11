"""
PowerShoring Analytics — Asynchronous Celery Task Declarations
Maps computational-heavy functions for offload execution.
"""
import logging
import base64
from etl.worker import celery_app
from etl.pipeline import ingest_shapefile_to_db

logger = logging.getLogger(__name__)

@celery_app.task(name="etl.process_shapefile_upload", bind=True, max_retries=3)
def task_process_shapefile_upload(self, base64_data: str, target_name: str, layer_key: str):
    """
    Background worker responsible for converting the upload binary 
    from client into PostGIS spatial relational structure.
    """
    try:
        logger.info(f"[ETL Task] Starting ingestion for {target_name}...")
        
        # Decode file passing (for heavy operations consider using Cloud Storage pre-sign URLs)
        file_bytes = base64.b64decode(base64_data)
        
        # Run core synchronous GeoPandas pipeline
        results = ingest_shapefile_to_db(file_bytes, target_name, layer_key)
        
        logger.info(f"[ETL Task] Successfully completed {target_name}. Rows: {results['features_count']}")
        return results
        
    except Exception as exc:
        logger.error(f"[ETL Task] Crash observed during ingestion: {exc}")
        # Auto retry mechanism for database deadlock glitches
        raise self.retry(exc=exc, countdown=10)


@celery_app.task(name="etl.precalculate_spatial_analytics", bind=True)
def task_precalculate_spatial_analytics(self, engine_type: str = "postgis"):
    """
    HYBRID GEOSPATIAL PRE-FETCH ENGINE
    Provides two scalable implementation modes chosen via `engine_type` parameter:
      1. 'postgis' -> High Performance Push-down (C++ native indexes) [DEFAULT]
      2. 'pandas'  -> In-memory computational algebra (Shapely/Python GIL)
    """
    import httpx
    import redis
    import json
    import pandas as pd
    import geopandas as gpd
    from sqlalchemy import text
    from core.config import settings
    from core.database import get_sync_engine

    logger.info(f"🚀 Triggering Anticipatory Pre-calc Engine using Mode: [{engine_type.upper()}]")
    engine = get_sync_engine()
    analytics_report = []

    try:
        # --- PHASE 1: Universal External Data Fetching ---
        epe_url = "https://gisepeprd2.epe.gov.br/arcgis/rest/services/WebMapEPE/Sistema_Transmissao/MapServer/0/query"
        params = {
            "where": "1=1", "outFields": "*", "f": "geojson", "returnGeometry": "true",
            "resultRecordCount": 800
        }
        
        logger.info("[1/3] Fetching External Raw Stream...")
        with httpx.Client(verify=False, timeout=60.0) as client:
             response = client.get(epe_url, params=params)
             response.raise_for_status()
             epe_geojson = response.json()
        
        # Prepare GeoDataFrame basis used by both execution modes
        lines_gdf = gpd.GeoDataFrame.from_features(epe_geojson, crs="EPSG:4326")
        lines_gdf = lines_gdf[lines_gdf.is_valid]

        # --- BRANCHING: DUAL-MODE EXECUTION ARCHITECTURE ---
        if engine_type.lower() == "postgis":
            logger.info("[2/3] [MODE: POSTGIS] Pushing to relational and firing spatial indices...")
            
            # Prep target persistence
            lines_gdf['source'] = 'webmap'
            lines_gdf['category'] = 'linha_transmissao'
            lines_gdf['name'] = lines_gdf.get('NOME', 'Desconhecido')
            lines_gdf = lines_gdf.rename_geometry('geom')
            final_gdf = lines_gdf[['source', 'category', 'name', 'geom']].copy()
            
            # Mirror Sync
            with engine.connect() as conn:
                conn.execute(text("DELETE FROM epe_data WHERE source = 'webmap' AND category = 'linha_transmissao'"))
                conn.commit()
            
            final_gdf.to_postgis(name="epe_data", con=engine, if_exists="append", index=False)

            # Execute DB-native spatial algebra
            spatial_query = text("""
                SELECT c.id, c.name, COUNT(e.id), ST_AsGeoJSON(ST_Collect(e.geom))::json
                FROM clusters c
                INNER JOIN epe_data e ON ST_DWithin(c.geom, e.geom, 0.45)
                WHERE e.category = 'linha_transmissao'
                GROUP BY c.id, c.name;
            """)
            with engine.connect() as conn:
                result = conn.execute(spatial_query).fetchall()
                for row in result:
                    analytics_report.append({
                        "cluster_id": row[0], "cluster_name": row[1],
                        "nearby_infrastructure_count": int(row[2]), "lines_network": row[3]
                    })

        elif engine_type.lower() == "pandas":
            logger.info("[2/3] [MODE: PANDAS] Loading local clusters to RAM for local compute...")
            
            # Load Clusters from DB into Memory
            clusters_gdf = gpd.read_postgis(
                sql="SELECT id, name, geom FROM clusters", 
                con=engine, geom_col='geom', crs="EPSG:4326"
            )
            
            # Apply computational buffer vector in Python RAM
            clusters_gdf['geometry'] = clusters_gdf.geometry.buffer(0.45)
            
            # Local Coordinate Join (CPU/GIL Limited)
            joined = gpd.sjoin(lines_gdf, clusters_gdf, how='inner', predicate='intersects')
            
            # Format consistently with PostGIS output structure
            for cluster_id in joined['id'].unique():
                c_data = joined[joined['id'] == cluster_id]
                analytics_report.append({
                    "cluster_id": cluster_id,
                    "cluster_name": c_data.iloc[0]['name'],
                    "nearby_infrastructure_count": len(c_data),
                    "lines_network": c_data.__geo_interface__ # Python Native GeoJSON stream
                })
        
        else:
            raise ValueError(f"Unsupported engine type requested: {engine_type}")

        # --- PHASE 3: Unified Cache Delivery ---
        logger.info(f"[3/3] Normalizing output ({len(analytics_report)} clusters resolved) -> Hydrating Redis.")
        
        cache_key = "geo_cache:infrastructure_intersections"
        r = redis.from_url(settings.REDIS_URL)
        
        payload = {
            "source": "Multi-Engine Anticipatory Platform",
            "generated_at": pd.Timestamp.now().isoformat(),
            "compute_engine": engine_type.upper(),
            "results": analytics_report
        }
        
        r.set(cache_key, json.dumps(payload), ex=86400)
        logger.info(f"✅ CACHE SUCCESS. Mode {engine_type} computation safely finalized.")
        
        return {"status": "success", "mode_used": engine_type, "records": len(analytics_report)}

    except Exception as e:
        logger.error(f"❌ Engine Task Failed (Mode: {engine_type}): {str(e)}")
        raise
