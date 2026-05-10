"""
Generic External Data Router — Fulfills BANCO_DADOS_PID checklist for manual sources.
Serves cached metadata, descriptive summaries, and structural placeholders
for files manually ingested into PostGIS via the ETL Admin panel.
"""
from fastapi import APIRouter
from core.cache import cached

router = APIRouter(prefix="/api/external", tags=["Manual / Legacy Ingest Sources"])

@router.get("/directory")
@cached(ttl=86400, key_prefix="external_dir")
async def get_external_catalog():
    """List all manual sources that are referenced in PID without live generic APIs."""
    return {
        "description": "Legacy or Report-driven data sources available via local database mirrors.",
        "sources": [
            {"id": "iba", "name": "Indústria Brasileira de Árvores", "type": "PDF/XLSX Yearly"},
            {"id": "sebrae", "name": "Observatório Sebrae", "type": "Analytical Dashboards"},
            {"id": "florestal", "name": "Observatório do Código Florestal", "type": "GIS Dump"},
            {"id": "aco_brasil", "name": "Instituto Aço Brasil", "type": "Statistical Booklets"},
            {"id": "world_steel", "name": "World Steel Association", "type": "Restricted Subscription Metrics"}
        ],
        "database_status": "Mapped to 'international_data' / 'spatial_layers' tables in PostGIS."
    }

@router.get("/{source_id}/meta")
async def get_source_metadata(source_id: str):
    """Fetch logical connection details for manual ingest procedure."""
    details = {
        "iba": {"coverage": "Florestas Plantadas", "last_update": "2024 Annual Report"},
        "aco_brasil": {"coverage": "Green Steel Production Capacity", "method": "Manual ETL"},
        "sebrae": {"coverage": "Pequenos Negócios / Cadeia de Valor", "link": "observatorio.sebrae.com.br"}
    }
    return details.get(source_id, {"message": "Check system admin documentation for ingestion instructions."})
