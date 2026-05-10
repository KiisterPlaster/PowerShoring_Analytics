"""
PowerShoring Analytics — ETL Pipeline Routines
Handles the IO flow from uploaded geometries into Postgres/PostGIS tables.
"""
import logging
import tempfile
import os
import zipfile
import geopandas as gpd
from sqlalchemy import text

from core.database import get_sync_engine
from etl.validators import validate_shapefile_archive, validate_crs

logger = logging.getLogger(__name__)

def ingest_shapefile_to_db(file_bytes: bytes, table_name: str, layer_key: str) -> dict:
    """
    Takes raw archive bytes, extracts, loads into GeoPandas, ensures EPSG:4326, 
    and streams directly into the PostGIS database 'spatial_layers' store.
    """
    is_valid, msg = validate_shapefile_archive(file_bytes)
    if not is_valid:
        raise ValueError(f"Archive Validation Failed: {msg}")

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
        
        # Standardize coordinates to WGS84
        if gdf.crs is None:
            gdf.set_crs("EPSG:4326", inplace=True)
        elif gdf.crs.to_epsg() != 4326:
            gdf = gdf.to_crs("EPSG:4326")

        # Final checks
        row_count = len(gdf)
        
        # Use global sync connection for to_postgis
        engine = get_sync_engine()
        
        # Clean geometry just in case
        gdf = gdf[gdf.geometry.notnull()]
        
        # Save it as a separate dynamically named geometry table 
        # OR write into main central `spatial_layers` table
        # For demonstration logic we populate a distinct table:
        table_sanitized = f"ext_{table_name.lower().replace('-', '_')}"
        gdf.to_postgis(name=table_sanitized, con=engine, if_exists="replace", index=False)
        
        # Force GIST indexing
        with engine.connect() as conn:
            conn.execute(text(f"CREATE INDEX IF NOT EXISTS idx_{table_sanitized}_geom ON {table_sanitized} USING GIST (geometry);"))
            conn.commit()

        return {
            "success": True,
            "table_created": table_sanitized,
            "features_count": row_count,
            "crs": "EPSG:4326"
        }
