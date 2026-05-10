"""
PowerShoring Analytics — ETL Pipeline Routines
Handles the IO flow from uploaded geometries into Postgres/PostGIS tables.
"""
import logging
import tempfile
import os
import zipfile
import geopandas as gpd
import dask_geopandas
from sqlalchemy import text

from core.database import get_sync_engine
from core.firebase_client import get_firebase_client
from etl.validators import validate_shapefile_archive, validate_crs, sanitize_table_name

logger = logging.getLogger(__name__)

def ingest_shapefile_to_db(file_bytes: bytes, table_name: str, layer_key: str) -> dict:
    """
    Takes raw archive bytes, extracts, loads into GeoPandas, ensures EPSG:4326, 
    and streams directly into the PostGIS database 'spatial_layers' store.
    """
    # 1. Immediate Sanitization of user input identifiers
    safe_name = sanitize_table_name(table_name)
    safe_key = sanitize_table_name(layer_key)
    
    if not safe_name:
        raise ValueError("Invalid table name identifier provided.")

    # 2. Content Deep Scan (Size, Format, Structure, Deflate-Bomb, ZipSlip)
    is_valid, msg = validate_shapefile_archive(file_bytes)
    if not is_valid:
        raise ValueError(f"Archive Security Validation Failed: {msg}")

    # Step 1: Secure persistence in Firebase Storage (Landing Zone) using strictly sanitized paths
    firebase = get_firebase_client()
    firebase_uri = firebase.upload_bytes(file_bytes, f"ingestions/{safe_name}/{safe_key}_upload.zip")
    logger.info(f"Raw file persisted to storage: {firebase_uri}")

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "upload.zip")
        with open(zip_path, "wb") as f:
            f.write(file_bytes)
        
        # Extract
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)
            
        # Find the .shp path
        shp_file = next((os.path.join(tmpdir, f) for f in os.listdir(tmpdir) if f.endswith(".shp")), None)
        if not shp_file:
             raise FileNotFoundError("Shapefile .shp main file missing despite successful extraction.")
        
        # Load via fast pyogrio engine specified in requirements
        gdf = gpd.read_file(shp_file, engine="pyogrio")
        
        # Standardize coordinates to WGS84 via Dask-GeoPandas parallel partitions
        req_partitions = int(os.getenv("DASK_PARTITIONS", "4"))
        # Optimization: Don't partition beyond actual row count to prevent empty task overhead
        n_partitions = min(req_partitions, max(1, len(gdf)))
        logger.info(f"Initializing Dask-GeoPandas distribution with {n_partitions} partitions.")
        
        # Wrap original GDF in Dask partition structure
        ddf = dask_geopandas.from_geopandas(gdf, npartitions=n_partitions)
        
        # Perform geometry sanitization and re-projection lazily
        ddf = ddf[ddf.geometry.notnull()]
        
        if gdf.crs is None:
            logger.warning("Coordinate system unknown. Assuming EPSG:4326.")
            ddf = ddf.set_crs("EPSG:4326")
        elif gdf.crs.to_epsg() != 4326:
            logger.info(f"Transforming dataset to EPSG:4326 natively on parallel nodes.")
            ddf = ddf.to_crs("EPSG:4326")

        # Compute final optimized GeoDataFrame back to memory for database write
        gdf = ddf.compute()
        
        # CRITICAL FIX: Force active geometry column name to 'geometry' to match GIST index query
        current_geom_col = gdf.geometry.name
        if current_geom_col != "geometry":
            logger.info(f"Standardizing geometry column from '{current_geom_col}' to 'geometry'")
            # Rename without breaking the geodataframe metadata binding
            gdf = gdf.rename_geometry("geometry")

        # Final count
        row_count = len(gdf)
        
        # Use global sync connection for to_postgis
        engine = get_sync_engine()
        
        # Save it as a separate dynamically named geometry table using strict whitelist sanitization
        table_sanitized = f"ext_{safe_name}"
        gdf.to_postgis(name=table_sanitized, con=engine, if_exists="replace", index=False)
        
        # Force GIST indexing
        with engine.connect() as conn:
            conn.execute(text(f"CREATE INDEX IF NOT EXISTS idx_{table_sanitized}_geom ON {table_sanitized} USING GIST (geometry);"))
            conn.commit()

        return {
            "success": True,
            "table_created": table_sanitized,
            "features_count": row_count,
            "crs": "EPSG:4326",
            "storage_uri": firebase_uri
        }
