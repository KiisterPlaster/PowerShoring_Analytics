"""
High-Speed Cache Hydrator.
Recursively downloads massive ArcGIS layers and persists them into the PostGIS spatial_layers table.
"""
import os
import sys
import httpx
import asyncio
import json
from typing import List, Dict

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from geoalchemy2.shape import from_shape
from shapely.geometry import shape

# Add backend directory to sys path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.config import settings
from models.orm import SpatialLayer
from core.database import get_sync_engine
SessionLocal = sessionmaker(bind=get_sync_engine())

ARCGIS_BASE = settings.ARCGIS_BASE_URL

async def fetch_entire_layer(layer_key: str) -> List[Dict]:
    """Recursively fetch all pages from ArcGIS until exhausted."""
    if layer_key not in settings.ARCGIS_LAYERS:
        print(f"Skipping unknown layer: {layer_key}")
        return []
        
    path = settings.ARCGIS_LAYERS[layer_key]
    base_url = f"{ARCGIS_BASE}/{path}"
    
    all_features = []
    offset = 0
    page_size = 2000 # Native limit
    
    print(f"Starting extraction for '{layer_key}'...")
    async with httpx.AsyncClient(timeout=120.0) as client:
        while True:
            url = (
                f"{base_url}?where=1=1&outFields=*&f=geojson"
                f"&resultOffset={offset}&resultRecordCount={page_size}"
            )
            try:
                res = await client.get(url)
                res.raise_for_status()
                data = res.json()
            except Exception as e:
                print(f"  [!] HTTP Failure at offset {offset}: {str(e)}")
                break
                
            features = data.get("features", [])
            feature_count = len(features)
            all_features.extend(features)
            
            print(f"  --> Pulled {feature_count} features (Total so far: {len(all_features)})")
            
            # End condition: less than page size means end of set, or explicitly check exceeded flag
            if feature_count < page_size:
                break
                
            exceeded = data.get("properties", {}).get("exceededTransferLimit", False)
            if exceeded is False and feature_count < page_size: # Defensive double check
                break
                
            offset += page_size
            
    print(f"Completed extraction for '{layer_key}'. Total features: {len(all_features)}")
    return all_features

def persist_to_db(layer_key: str, features: List[Dict]):
    """Commit geometry features directly to spatial_layers PostGIS table."""
    db = SessionLocal()
    try:
        # Check basic categorical metadata from our catalog
        from core.clusters_data import LAYER_CATALOG
        meta = next((c for c in LAYER_CATALOG if c["layer_key"] == layer_key), {})
        cat = meta.get("category", "General")
        display = meta.get("display_name", layer_key.replace("_", " ").title())
        
        print(f"Committing {len(features)} features to DB for {layer_key}...")
        
        inserted = 0
        for feat in features:
            geom_dict = feat.get("geometry")
            if not geom_dict:
                continue
            
            try:
                # Create geometry shape via shapely to valid form
                geom_obj = shape(geom_dict)
                
                # Filter non-essential large properties to keep DB light if needed, or keep all
                layer_entry = SpatialLayer(
                    layer_key=layer_key,
                    source="ArcGIS Cache",
                    display_name=display,
                    category=cat,
                    geom=from_shape(geom_obj, srid=4326),
                    properties=feat.get("properties", {})
                )
                db.add(layer_entry)
                inserted += 1
                
                # Batch commit every 200 to keep memory low
                if inserted % 200 == 0:
                    db.commit()
            except Exception as e:
                pass # Silently ignore corrupt feature topologies
                
        db.commit()
        print(f"Successfully persisted {inserted} features to DB.")
        
    except Exception as e:
        db.rollback()
        print(f"Database persistence failed: {str(e)}")
    finally:
        db.close()

async def main():
    # Pick priority heavy layers that frequently fail 502 or are truncated
    priority_layers = [
        "terras_indigenas",    # Frequently 502s
        "unidades_conservacao", # Slow
        "estradas",            # Truncated
        "ferrovias"            # Picotada (truncated)
    ]
    
    for layer in priority_layers:
        feats = await fetch_entire_layer(layer)
        if feats:
            persist_to_db(layer, feats)

if __name__ == "__main__":
    asyncio.run(main())
