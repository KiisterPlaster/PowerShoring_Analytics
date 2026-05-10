"""
ANEEL Data Router — Integrates with ANEEL Dados Abertos (CKAN API).
Consumes dataset SIGA - Sistema de Informações de Geração da ANEEL.
"""
import httpx
from fastapi import APIRouter, HTTPException, Query
from core.cache import cached

router = APIRouter(prefix="/api/aneel", tags=["ANEEL / SIGA"])

CKAN_BASE = "https://dadosabertos.aneel.gov.br/api/3/action"
# Known static resource ID for SIGA dynamic dump if available, or direct search
SIGA_DATASET_NAME = "siga-sistema-de-informacoes-de-geracao-da-aneel"

@router.get("/info")
@cached(ttl=86400, key_prefix="aneel")
async def get_siga_metadata():
    """Fetch metadata for the SIGA dataset from CKAN."""
    url = f"{CKAN_BASE}/package_show"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params={"id": SIGA_DATASET_NAME})
            response.raise_for_status()
            return response.json()["result"]
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"ANEEL CKAN Error: {str(e)}")

@router.get("/search")
@cached(ttl=3600, key_prefix="aneel_search")
async def search_resources(query: str = Query("geracao", description="Search query for datasets")):
    """Search for electricity generation datasets on ANEEL."""
    url = f"{CKAN_BASE}/package_search"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params={"q": query})
            response.raise_for_status()
            results = response.json()["result"]["results"]
            return [
                {"title": r.get("title"), "name": r.get("name"), "notes": r.get("notes")[:200]} 
                for r in results
            ]
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))
