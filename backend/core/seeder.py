import logging
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from geoalchemy2.elements import WKTElement

from core.database import get_sync_engine
from models.orm import Cluster
from core.clusters_data import CLUSTERS_DATA

logger = logging.getLogger(__name__)

def seed_database():
    """
    Validates if default dataset exists. If clusters are empty, 
    populates them from static dictionary to the live DB.
    """
    engine = get_sync_engine()
    
    with Session(engine) as session:
        # 1. Count existing rows
        count_stmt = select(func.count()).select_from(Cluster)
        row_count = session.execute(count_stmt).scalar()
        
        if row_count > 0:
            logger.info(f"🌱 Clusters already seeded. Total count: {row_count}. Skipping.")
            return

        logger.info("⚡ Seeding process started: Moving static clusters to dynamic DB...")
        
        new_entries = []
        for c in CLUSTERS_DATA:
            # Convert separate lat/lng into PostGIS Point WKT (SRID 4326)
            # Standard is Point(Longitude Latitude)
            wkt_geom = WKTElement(f"POINT({c['lng']} {c['lat']})", srid=4326)
            
            db_cluster = Cluster(
                id=c['id'],
                name=c['name'],
                region=c['region'],
                state=c['state'],
                port=c['port'],
                vocations=c['vocations'],
                energy_sources=c['energy_sources'],
                critical_minerals=c['critical_minerals'],
                hydrogen_potential=c['hydrogen_potential'],
                description=c['description'],
                geom=wkt_geom
            )
            new_entries.append(db_cluster)
        
        try:
            session.add_all(new_entries)
            session.commit()
            logger.info(f"✅ Seed Success: {len(new_entries)} industrial clusters written to PostGIS.")
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Critical failure during Database Seeding: {str(e)}")
            raise e
