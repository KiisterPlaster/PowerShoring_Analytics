"""
Clusters Router — Serves real industrial cluster data from Atlas 2025.
"""
from fastapi import APIRouter, HTTPException

from core.clusters_data import CLUSTERS_DATA
from models.schemas import ClusterOut

router = APIRouter(prefix="/api/clusters", tags=["Industrial Clusters"])


@router.get("/", response_model=list[ClusterOut])
async def list_clusters():
    """Return all 9 industrial clusters from Atlas do Futuro Industrial 2025."""
    return CLUSTERS_DATA


@router.get("/{cluster_id}", response_model=ClusterOut)
async def get_cluster(cluster_id: str):
    """Return a specific cluster by ID."""
    for cluster in CLUSTERS_DATA:
        if cluster["id"] == cluster_id:
            return cluster
    raise HTTPException(
        status_code=404,
        detail=f"Cluster '{cluster_id}' not found. Available: {[c['id'] for c in CLUSTERS_DATA]}",
    )


@router.get("/region/{region}")
async def get_clusters_by_region(region: str):
    """Filter clusters by region (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)."""
    filtered = [c for c in CLUSTERS_DATA if c["region"].lower() == region.lower()]
    if not filtered:
        regions = list({c["region"] for c in CLUSTERS_DATA})
        raise HTTPException(
            status_code=404,
            detail=f"No clusters in region '{region}'. Available: {regions}",
        )
    return filtered
