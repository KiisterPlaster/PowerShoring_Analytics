"""
TerraBrasilis (INPE) Data Router — Consumes real PRODES/DETER REST API for deforestation data.
"""
import httpx
from fastapi import APIRouter, HTTPException, Query
from core.cache import cached

router = APIRouter(prefix="/api/terrabrasilis", tags=["TerraBrasilis / INPE"])

BASE_URL = "https://terrabrasilis.dpi.inpe.br/api/v1"

@router.get("/programs")
@cached(ttl=86400, key_prefix="terrabrasilis")
async def list_programs():
    """List available monitoring programs (PRODES, DETER)."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/monitoring/program")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"INPE API Error: {str(e)}")

@router.get("/indicators")
@cached(ttl=3600, key_prefix="terrabrasilis")
async def get_indicators(
    program: str = Query("prodes", description="prodes or deter"),
    biome: str = Query("legal_amazon", description="legal_amazon, cerrado, etc.")
):
    """Fetch deforestation indicators filtered by program and biome."""
    async with httpx.AsyncClient() as client:
        try:
            # Generic endpoint for indicators based on open API pattern
            response = await client.get(f"{BASE_URL}/monitoring/program/{program}/data/{biome}")
            response.raise_for_status()
            return {
                "source": f"INPE TerraBrasilis - {program.upper()} {biome.replace('_', ' ').title()}",
                "data": response.json()
            }
        except httpx.HTTPStatusError:
            # Fallback for specific pathing in TerraBrasilis API
            return {
                "source": f"INPE TerraBrasilis - {program.upper()} {biome}",
                "info": "Consult data available via WFS/WMS services or bulk REST.",
                "api_base": f"{BASE_URL}/monitoring/program"
            }
        except Exception as e:
             raise HTTPException(status_code=502, detail=str(e))
