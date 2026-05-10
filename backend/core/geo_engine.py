"""
Geospatial Engine — PostGIS + GeoPandas + GEOS/Shapely Integration Module.

Connection Strategies:
  PostGIS:   psycopg2 / SQLAlchemy async engine → postgresql://user:pass@host:5432/db
  GiST:     SQL index creation → CREATE INDEX ... USING GIST (geom_column);
  GeoPandas: read_postgis() / to_postgis() + read_file() for Shapefiles
  GEOS:     Accessed via Shapely Python bindings (shapely.geometry, shapely.ops)

This module provides utility functions for spatial operations used by the ETL
pipeline and the API analytics endpoints.
"""
import logging
from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from core.config import settings

logger = logging.getLogger(__name__)

# ========================================================
# PostGIS Connection (via SQLAlchemy + psycopg2)
# ========================================================
_engine: Engine | None = None


def get_postgis_engine() -> Engine:
    """
    Create or return a cached SQLAlchemy engine connected to PostGIS.
    Connection: postgresql://user:password@host:5432/database
    Driver: psycopg2-binary
    """
    global _engine
    if _engine is None:
        _engine = create_engine(
            settings.DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            echo=settings.DEBUG,
        )
        logger.info(f"[PostGIS] Engine created: {settings.DATABASE_URL.split('@')[-1]}")
    return _engine


def verify_postgis_connection() -> dict:
    """
    Verify PostGIS is installed and return version info.
    Tests: PostgreSQL version, PostGIS version, GEOS version (via PostGIS).
    """
    engine = get_postgis_engine()
    try:
        with engine.connect() as conn:
            pg_version = conn.execute(text("SELECT version();")).scalar()
            postgis_version = conn.execute(text("SELECT PostGIS_Full_Version();")).scalar()
            srid_count = conn.execute(
                text("SELECT COUNT(*) FROM spatial_ref_sys;")
            ).scalar()
            return {
                "status": "connected",
                "postgresql_version": pg_version,
                "postgis_version": postgis_version,
                "spatial_ref_systems": srid_count,
                "connection_string": settings.DATABASE_URL.split("@")[-1],
            }
    except Exception as exc:
        return {
            "status": "unavailable",
            "error": str(exc),
            "note": "PostGIS not running. Start with: docker-compose up -d postgis",
        }


# ========================================================
# GiST Index Management
# ========================================================
def ensure_gist_index(table_name: str, geom_column: str = "geom") -> str:
    """
    Create a GiST spatial index on a PostGIS table if it doesn't exist.
    GiST (Generalized Search Tree) is the standard index for spatial queries.

    SQL: CREATE INDEX IF NOT EXISTS idx_{table}_geom
         ON {table} USING GIST ({geom_column});
    """
    index_name = f"idx_{table_name}_{geom_column}"
    sql = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} USING GIST ({geom_column});"
    engine = get_postgis_engine()
    try:
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()
            logger.info(f"[GiST] Index '{index_name}' ensured on {table_name}.{geom_column}")
            return f"GiST index '{index_name}' created/verified"
    except Exception as exc:
        logger.warning(f"[GiST] Index creation failed: {exc}")
        return f"GiST index failed: {exc}"


# ========================================================
# GeoPandas Integration (read_postgis / read_file)
# ========================================================
def read_geodata_from_postgis(
    sql_or_table: str,
    geom_col: str = "geom",
    crs: str = "EPSG:4326",
) -> Any:
    """
    Read geospatial data from PostGIS into a GeoDataFrame.

    Connection: Uses SQLAlchemy engine (psycopg2 driver)
    Method: geopandas.read_postgis()

    Args:
        sql_or_table: SQL query string or table name
        geom_col: Name of the geometry column
        crs: Coordinate Reference System

    Returns:
        GeoDataFrame with geometry and attributes
    """
    import geopandas as gpd

    engine = get_postgis_engine()
    query = sql_or_table if sql_or_table.strip().upper().startswith("SELECT") else f"SELECT * FROM {sql_or_table}"

    gdf = gpd.read_postgis(
        sql=query,
        con=engine,
        geom_col=geom_col,
        crs=crs,
    )
    logger.info(f"[GeoPandas] Loaded {len(gdf)} features from PostGIS")
    return gdf


def write_geodata_to_postgis(
    gdf: Any,
    table_name: str,
    if_exists: str = "replace",
) -> str:
    """
    Write a GeoDataFrame to PostGIS.

    Connection: Uses SQLAlchemy engine
    Method: geopandas.GeoDataFrame.to_postgis()

    After writing, automatically creates a GiST index for spatial queries.
    """
    engine = get_postgis_engine()
    gdf.to_postgis(
        name=table_name,
        con=engine,
        if_exists=if_exists,
        index=True,
    )
    ensure_gist_index(table_name)
    logger.info(f"[GeoPandas] Wrote {len(gdf)} features to PostGIS table '{table_name}'")
    return f"Written {len(gdf)} features to '{table_name}' with GiST index"


def read_shapefile(filepath: str, crs: str = "EPSG:4326") -> Any:
    """
    Read a Shapefile or GeoPackage into a GeoDataFrame.

    Engine: Pyogrio (faster) or Fiona (fallback)
    Formats: .shp, .gpkg, .geojson, .kml

    Used for: MapBiomas Shapefiles, ANP spatial data, IBGE malha municipal.
    """
    import geopandas as gpd

    gdf = gpd.read_file(filepath, engine="pyogrio")
    if gdf.crs is None:
        gdf = gdf.set_crs(crs)
    elif str(gdf.crs) != crs:
        gdf = gdf.to_crs(crs)
    logger.info(f"[GeoPandas] Read {len(gdf)} features from {filepath}")
    return gdf


# ========================================================
# GEOS via Shapely — Geometry Operations
# ========================================================
def spatial_analysis_buffer(
    gdf: Any,
    distance_km: float,
    geom_col: str = "geometry",
) -> Any:
    """
    Create buffer zones around features using GEOS engine.

    Library: Shapely (Python bindings for GEOS C++ library)
    Method: GeoSeries.buffer()

    Use case: "Find all ports within 50km of a proposed industrial site"
    """
    import geopandas as gpd

    # Project to metric CRS for accurate distance calculation (SIRGAS 2000 / UTM)
    gdf_proj = gdf.to_crs("EPSG:31983")  # SIRGAS 2000 / UTM zone 23S (Central Brazil)
    gdf_proj[geom_col] = gdf_proj[geom_col].buffer(distance_km * 1000)
    result = gdf_proj.to_crs("EPSG:4326")
    logger.info(f"[GEOS/Shapely] Buffer of {distance_km}km applied to {len(result)} features")
    return result


def spatial_join_clusters(
    left_gdf: Any,
    right_gdf: Any,
    how: str = "inner",
    predicate: str = "intersects",
) -> Any:
    """
    Perform a spatial join using GEOS predicates.

    Library: GeoPandas + Shapely (GEOS backend)
    Predicates: 'intersects', 'within', 'contains', 'crosses', 'touches'

    Use case: "Which renewable energy plants are WITHIN each industrial cluster?"
    """
    import geopandas as gpd

    result = gpd.sjoin(left_gdf, right_gdf, how=how, predicate=predicate)
    logger.info(f"[GEOS/Shapely] Spatial join: {len(result)} matches ({predicate})")
    return result


def validate_geometries(gdf: Any) -> dict:
    """
    Validate and fix geometries using GEOS.

    Library: Shapely (shapely.validation.make_valid)
    Method: GeoSeries.is_valid + make_valid()

    Essential for: MapBiomas shapefiles, ANP spatial data
    """
    from shapely.validation import make_valid

    total = len(gdf)
    invalid_mask = ~gdf.geometry.is_valid
    invalid_count = invalid_mask.sum()

    if invalid_count > 0:
        gdf.loc[invalid_mask, "geometry"] = gdf.loc[invalid_mask, "geometry"].apply(make_valid)
        logger.info(f"[GEOS/Shapely] Fixed {invalid_count}/{total} invalid geometries")

    return {
        "total_features": total,
        "invalid_fixed": int(invalid_count),
        "all_valid": bool(gdf.geometry.is_valid.all()),
    }
