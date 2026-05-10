"""
PowerShoring Analytics — File Ingestion Validators
Ensures uploaded Shapefiles and CSVs match geospatial requirements.
"""
import zipfile
import io
from typing import Tuple

def validate_shapefile_archive(file_bytes: bytes) -> Tuple[bool, str]:
    """
    Verify that an uploaded ZIP contains the mandatory shapefile components.
    Requires: .shp, .shx, .dbf
    """
    try:
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
            file_list = z.namelist()
            extensions = {f.split('.')[-1].lower() for f in file_list if '.' in f}
            
            missing = []
            for req in ['shp', 'shx', 'dbf']:
                if req not in extensions:
                    missing.append(f".{req}")
            
            if missing:
                return False, f"Missing mandatory extensions: {', '.join(missing)}"
            return True, "Valid archive"
    except zipfile.BadZipFile:
        return False, "Uploaded file is not a valid zip archive."
    except Exception as e:
        return False, f"Unexpected corruption: {str(e)}"

def validate_crs(gdf) -> Tuple[bool, str]:
    """Checks if GeoDataFrame CRS is WGS84 (EPSG 4326) or convertible."""
    if gdf.crs is None:
        return False, "Undefined Spatial Reference System (CRS). Ensure .prj file exists."
    return True, str(gdf.crs)
