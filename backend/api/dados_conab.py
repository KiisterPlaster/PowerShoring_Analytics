"""
CONAB Data Router — Proxy metadata for the Agricultural Supply National Company data.
Aggregates access to harvest dashboards and products mapping.
"""
from fastapi import APIRouter, Query
from core.cache import cached

router = APIRouter(prefix="/api/conab", tags=["CONAB"])

@router.get("/summary")
@cached(ttl=86400, key_prefix="conab_root")
async def get_conab_summary():
    """Returns access metadata for CONAB agricultural surveys."""
    return {
        "source": "Companhia Nacional de Abastecimento (CONAB)",
        "dashboard": "https://portaldeinformacoes.conab.gov.br/produtos-360.html",
        "status": "Dataset available for bulk ingestion through administrative ETL module.",
        "mapped_commodities": ["Soja", "Milho", "Algodão", "Cana-de-Açúcar"]
    }

@router.get("/safra")
async def get_sample_harvest():
    """Mock statistical representative data until actual massive XLSX dump ingestion."""
    return {
        "source": "Estimativa CONAB Safra 2024/25",
        "brazil_total_grain_est": "311.0 Million Tons",
        "note": "Use internal DB queries once ETL finishes executing on spatial datasets."
    }
