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
    Background background worker responsible for converting the upload binary 
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
