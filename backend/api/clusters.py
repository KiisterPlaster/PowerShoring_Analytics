"""
Clusters Router — Serves real industrial cluster data pulled dynamically from PostGIS.
"""
from fastapi import APIRouter, HTTPException
from sqlalchemy import select, func
from typing import List

from core.database import get_async_session
from models.orm import Cluster
from models.schemas import ClusterOut

router = APIRouter(prefix="/api/clusters", tags=["Industrial Clusters"])

def _get_cluster_select_stmt():
    """Standard query builder extracting lat/lng components from geometry."""
    return select(
        Cluster.id,
        Cluster.name,
        Cluster.region,
        Cluster.state,
        Cluster.port,
        Cluster.vocations,
        Cluster.energy_sources,
        Cluster.critical_minerals,
        Cluster.hydrogen_potential,
        Cluster.description,
        func.ST_Y(Cluster.geom).label("lat"), # Latitude is Y
        func.ST_X(Cluster.geom).label("lng")  # Longitude is X
    )

@router.get("/", response_model=List[ClusterOut])
async def list_clusters():
    """Return all registered industrial clusters from dynamic Database."""
    async with get_async_session() as session:
        stmt = _get_cluster_select_stmt().order_by(Cluster.name)
        result = await session.execute(stmt)
        return result.mappings().all()

@router.get("/{cluster_id}", response_model=ClusterOut)
async def get_cluster(cluster_id: str):
    """Return a specific cluster by ID."""
    async with get_async_session() as session:
        stmt = _get_cluster_select_stmt().where(Cluster.id == cluster_id)
        result = await session.execute(stmt)
        cluster = result.mappings().first()
        
        if not cluster:
            # Fetch list of all available IDs for the error message helper
            list_stmt = select(Cluster.id)
            all_ids = (await session.execute(list_stmt)).scalars().all()
            raise HTTPException(
                status_code=404,
                detail=f"Cluster '{cluster_id}' not found. Available: {list(all_ids)}",
            )
        return cluster

@router.get("/region/{region}", response_model=List[ClusterOut])
async def get_clusters_by_region(region: str):
    """Filter clusters by region (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)."""
    async with get_async_session() as session:
        # Perform case-insensitive match using ilike
        stmt = _get_cluster_select_stmt().where(Cluster.region.ilike(region))
        result = await session.execute(stmt)
        filtered = result.mappings().all()
        
        if not filtered:
            # Fetch existing regions to help the user
            reg_stmt = select(Cluster.region).distinct()
            regions = (await session.execute(reg_stmt)).scalars().all()
            raise HTTPException(
                status_code=404,
                detail=f"No clusters in region '{region}'. Available: {list(regions)}",
            )
        return filtered
