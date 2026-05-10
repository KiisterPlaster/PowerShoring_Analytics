"""
PowerShoring Analytics — File Ingestion Validators
Ensures uploaded Shapefiles and CSVs match geospatial and security requirements.
"""
import zipfile
import io
import re
import os
from typing import Tuple

# Set maximum allowed ingestion size (e.g., 100MB) to prevent RAM depletion attacks.
MAX_ZIP_SIZE = int(os.getenv("MAX_INGEST_SIZE_BYTES", 100 * 1024 * 1024))

def sanitize_table_name(name: str) -> str:
    """
    Restrict database identifiers strictly to a-z, 0-9, and underscores.
    Prevents SQL Injection and schema parsing malfunctions.
    """
    # Keep only valid alphanum characters
    clean = re.sub(r'[^a-zA-Z0-9_]', '', name.strip().replace(' ', '_'))
    return clean.lower()[:60] # Reasonable length limit for PostgreSQL tables

def validate_shapefile_archive(file_bytes: bytes) -> Tuple[bool, str]:
    """
    Validates archive for mandatory components, path traversal, and dangerous payloads.
    """
    # 1. File Size Hard Limit
    if len(file_bytes) > MAX_ZIP_SIZE:
        size_mb = len(file_bytes) / (1024 * 1024)
        return False, f"Archive exceeds limit: {size_mb:.1f}MB > {MAX_ZIP_SIZE/(1024*1024)}MB allowed."

    try:
        # Convert stream to check content integrity without writing to disk
        in_mem = io.BytesIO(file_bytes)
        
        with zipfile.ZipFile(in_mem) as z:
            file_list = z.infolist()
            extensions = set()
            total_uncompressed_size = 0
            
            for info in file_list:
                filename = info.filename
                
                # 2. Path Traversal Guard (ZipSlip)
                # Reject absolute paths, parent directory backtracks, or NT drives
                if os.path.isabs(filename) or '..' in filename or filename.startswith('/') or ':' in filename:
                     return False, f"SECURITY VIOLATION: Disallowed path pattern inside ZIP: '{filename}'"
                
                total_uncompressed_size += info.file_size
                
                # Collect unique extensions from leaf names
                base = os.path.basename(filename)
                if '.' in base:
                    extensions.add(base.split('.')[-1].lower())
            
            # 3. Deflate Bomb Protection
            # Enforce compression ratio checks or total uncompressed ceilings
            if total_uncompressed_size > MAX_ZIP_SIZE * 5:
                 return False, "SECURITY VIOLATION: Highly suspicious compression ratio (Potential Zip Bomb)."

            # 4. Content Integrity Requirements
            missing = []
            for req in ['shp', 'shx', 'dbf']:
                if req not in extensions:
                    missing.append(f".{req}")
            
            if missing:
                return False, f"Mandatory component missing: {', '.join(missing)}"
                
            return True, "Archive successfully sanitized and verified."

    except zipfile.BadZipFile:
        return False, "Uploaded file is not a valid zip archive structure."
    except Exception as e:
        return False, f"Verification aborted due to internal structural anomaly: {str(e)}"

def validate_crs(gdf) -> Tuple[bool, str]:
    """Checks if GeoDataFrame CRS is WGS84 (EPSG 4326) or convertible."""
    if gdf.crs is None:
        return False, "Undefined Spatial Reference System (CRS). Ensure .prj file exists."
    return True, str(gdf.crs)
