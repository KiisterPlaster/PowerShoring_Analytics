"""
Geospatial Router — Exposes PostGIS, GeoPandas, GiST, and GEOS/Shapely
operations via API endpoints.

Connection Summary:
  PostGIS:   postgresql://user:pass@host:5432/db (psycopg2 / SQLAlchemy)
  GiST:     CREATE INDEX ... USING GIST (geom_column) — SQL within PostGIS
  GeoPandas: read_postgis(), to_postgis(), read_file() — Python library
  GEOS:     shapely.geometry, shapely.ops — C++ bindings via Python
"""
from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from core.geo_engine import (
    verify_postgis_connection,
    ensure_gist_index,
    read_geodata_from_postgis,
    write_geodata_to_postgis,
    read_shapefile,
    spatial_analysis_buffer,
    validate_geometries,
)
import tempfile
import os

router = APIRouter(prefix="/api/geo", tags=["Geospatial - PostGIS/GeoPandas/GEOS"])


@router.get("/postgis/status")
async def postgis_status():
    """
    Verify PostGIS connection and return version info.
    Connection: SQLAlchemy engine → psycopg2 → PostgreSQL+PostGIS
    """
    result = verify_postgis_connection()
    return {
        "service": "PostGIS",
        "connection_type": "SQLAlchemy + psycopg2-binary",
        "connection_string_format": "postgresql://user:password@host:5432/database",
        "index_type": "GiST (Generalized Search Tree)",
        **result,
    }


@router.get("/postgis/tables")
async def list_postgis_tables():
    """
    List all spatial tables in PostGIS with geometry info.
    Connection: SQL query via SQLAlchemy engine.
    """
    from sqlalchemy import create_engine, text
    from core.config import settings

    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT f_table_name, f_geometry_column, coord_dimension, srid, type
                FROM geometry_columns
                ORDER BY f_table_name;
            """))
            tables = [
                {
                    "table": row[0],
                    "geometry_column": row[1],
                    "dimensions": row[2],
                    "srid": row[3],
                    "geometry_type": row[4],
                }
                for row in result
            ]
            return {
                "source": "PostGIS geometry_columns catalog",
                "connection_type": "SQLAlchemy + psycopg2",
                "tables": tables,
                "total": len(tables),
            }
    except Exception as exc:
        return {
            "source": "PostGIS",
            "status": "unavailable",
            "error": str(exc),
            "note": "Start PostGIS with: docker-compose up -d postgis",
        }


@router.post("/postgis/gist-index")
async def create_gist_index(
    table_name: str = Query(..., description="PostGIS table name"),
    geom_column: str = Query("geom", description="Geometry column name"),
):
    """
    Create a GiST spatial index on a PostGIS table.

    GiST (Generalized Search Tree) is NOT an external API —
    it's a PostgreSQL index method optimized for spatial queries.

    SQL: CREATE INDEX IF NOT EXISTS idx_{table}_{col} ON {table} USING GIST ({col});
    """
    result = ensure_gist_index(table_name, geom_column)
    return {
        "service": "GiST Index (PostGIS)",
        "connection_type": "SQL command via SQLAlchemy",
        "table": table_name,
        "geom_column": geom_column,
        "result": result,
        "explanation": (
            "GiST is a PostgreSQL index type (not an external API). "
            "It accelerates spatial queries like ST_Intersects, ST_Within, ST_DWithin."
        ),
    }


@router.post("/shapefile/upload")
async def upload_shapefile(
    file: UploadFile = File(..., description="Shapefile (.shp), GeoPackage (.gpkg), or GeoJSON"),
    table_name: str = Query("uploaded_layer", description="PostGIS table name for storage"),
):
    """
    Upload and process a spatial file using GeoPandas.

    GeoPandas connection methods:
      - read_file()   → reads .shp, .gpkg, .geojson, .kml (engine: Pyogrio/Fiona)
      - to_postgis()  → writes to PostGIS (engine: SQLAlchemy + psycopg2)

    GEOS validation:
      - Shapely's make_valid() fixes self-intersections and topology errors
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # Check file extension
    valid_extensions = {".shp", ".gpkg", ".geojson", ".json", ".kml"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in valid_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{ext}'. Supported: {valid_extensions}",
        )

    # Save to temp file and process with GeoPandas
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Read with GeoPandas (uses Pyogrio/Fiona → GEOS)
        gdf = read_shapefile(tmp_path)

        # Validate geometries with GEOS/Shapely
        validation = validate_geometries(gdf)

        # Return GeoJSON preview (first 50 features)
        preview = gdf.head(50)
        geojson = preview.__geo_interface__ if hasattr(preview, "__geo_interface__") else {}

        return {
            "service": "GeoPandas + GEOS/Shapely",
            "connection_type": "read_file() → Pyogrio engine",
            "filename": file.filename,
            "features_loaded": len(gdf),
            "geometry_validation": validation,
            "crs": str(gdf.crs),
            "columns": list(gdf.columns),
            "bounds": list(gdf.total_bounds),
            "preview_geojson": geojson,
            "note": "File processed locally. Use to_postgis() to persist in PostGIS.",
        }

    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Error processing spatial file: {str(exc)}",
        )
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


# ========================================================
# Connection Documentation Endpoint
# ========================================================
@router.get("/connections")
async def list_geo_connections():
    """Document all geospatial connection methods in the system."""
    return {
        "geospatial_stack": [
            {
                "component": "PostGIS",
                "type": "Database Extension",
                "connection": "postgresql://user:password@host:5432/database",
                "driver": "psycopg2-binary (sync) / asyncpg (async)",
                "orm": "SQLAlchemy + GeoAlchemy2",
                "purpose": "Persistent storage of geospatial data with SQL spatial queries",
                "key_functions": ["ST_Intersects", "ST_Within", "ST_Buffer", "ST_Distance"],
            },
            {
                "component": "GiST",
                "type": "PostgreSQL Index Method",
                "connection": "SQL command within PostGIS session",
                "syntax": "CREATE INDEX ... USING GIST (geometry_column);",
                "purpose": "Accelerates spatial queries (R-tree like index for geometry)",
                "note": "NOT an external API — it's a PostgreSQL internal index type",
            },
            {
                "component": "GeoPandas",
                "type": "Python Library",
                "connection": "Import: import geopandas as gpd",
                "methods": {
                    "read_postgis": "Read from PostGIS → gpd.read_postgis(sql, con=engine)",
                    "to_postgis": "Write to PostGIS → gdf.to_postgis(name, con=engine)",
                    "read_file": "Read files → gpd.read_file('data.shp', engine='pyogrio')",
                    "sjoin": "Spatial join → gpd.sjoin(left, right, predicate='intersects')",
                },
                "engines": ["Pyogrio (fast, default)", "Fiona (fallback)", "GDAL"],
                "formats": [".shp", ".gpkg", ".geojson", ".kml", ".csv (with geometry)"],
            },
            {
                "component": "GEOS (Geometry Engine Open Source)",
                "type": "C++ Library (accessed via Python bindings)",
                "connection": "Python bindings via Shapely library",
                "import": "from shapely.geometry import Point, Polygon; from shapely.ops import unary_union",
                "purpose": "Core geometry engine for spatial predicates and operations",
                "key_ops": ["buffer", "intersection", "union", "difference", "is_valid", "make_valid"],
                "note": "GEOS is also used internally by PostGIS for spatial operations",
            },
            {
                "component": "Shapely",
                "type": "Python Library (GEOS bindings)",
                "connection": "Import: from shapely.geometry import Point",
                "version": "2.0+ (uses direct GEOS C API, no PyGEOS needed)",
                "purpose": "Python interface to GEOS geometric operations",
            },
        ]
    }
