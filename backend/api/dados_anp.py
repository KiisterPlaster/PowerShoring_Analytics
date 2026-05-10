"""
ANP Data Router — Consumes Brazil's Portal de Dados Abertos for energy data.
Source: https://dados.gov.br/dados/organizacoes/visualizar/agencia-nacional-do-petroleo-gas-natural-e-biocombustiveis-anp

Connection Strategy:
  - REST API (JSON) via httpx async client
  - Direct CSV download with pandas for bulk datasets
  - Handles Brazilian encoding (Windows-1252) and decimal separators
"""
import io
import httpx
import pandas as pd
from fastapi import APIRouter, HTTPException, Query
from core.cache import cached

router = APIRouter(prefix="/api/anp", tags=["ANP - Energia"])

# Shared async client
_client: httpx.AsyncClient | None = None


async def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=60.0)
    return _client


# ========================================================
# ANP Official Data Endpoints (Portal de Dados Abertos)
# ========================================================
ANP_DATASETS = {
    "producao_petroleo": {
        "url": "https://dados.gov.br/dados/conjuntos-dados/producao-de-petroleo-e-gas-natural-por-estado-e-localizacao",
        "csv_url": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/ppgn/producao-petroleo-m3.csv",
        "description": "Producao mensal de petroleo por estado (m3)",
    },
    "producao_gas": {
        "url": "https://dados.gov.br/dados/conjuntos-dados/producao-de-petroleo-e-gas-natural-por-estado-e-localizacao",
        "csv_url": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/ppgn/producao-gas-natural-m3.csv",
        "description": "Producao mensal de gas natural por estado (m3)",
    },
    "biocombustiveis": {
        "url": "https://dados.gov.br/dados/conjuntos-dados/vendas-de-derivados-de-petroleo-e-biocombustiveis",
        "csv_url": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/vdpb/vendas-combustiveis-m3.csv",
        "description": "Vendas de biocombustiveis por estado (m3) - etanol, biodiesel",
    },
    "reservas": {
        "url": "https://dados.gov.br/dados/conjuntos-dados/reservas-nacionais-de-petroleo-e-gas-natural",
        "csv_url": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/reservas/reservas-petroleo-m3.csv",
        "description": "Reservas nacionais provadas de petroleo e gas",
    },
    "etanol": {
        "url": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos",
        "csv_url": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/vdpb/vendas-etanol-hidratado-m3.csv",
        "description": "Vendas específicas de etanol hidratado por UF",
    },
    "biodiesel": {
        "url": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos",
        "csv_url": "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/vdpb/vendas-biodiesel-b100-m3.csv",
        "description": "Vendas específicas de biodiesel puro (B100) por UF",
    },
}


@router.get("/datasets")
async def list_anp_datasets():
    """List all available ANP datasets with descriptions."""
    return {
        "source": "ANP - Agencia Nacional do Petroleo, Gas Natural e Biocombustiveis",
        "connection_type": "REST API (JSON) + Direct CSV Download",
        "datasets": {
            key: {"description": val["description"], "portal_url": val["url"]}
            for key, val in ANP_DATASETS.items()
        },
    }


@router.get("/data/{dataset_key}")
@cached(ttl=3600, key_prefix="anp_data")
async def get_anp_data(
    dataset_key: str,
    limit: int = Query(500, ge=1, le=5000, description="Max rows to return"),
    uf: str = Query("", description="Filter by UF (e.g., 'SP', 'BA')"),
):
    """
    Fetch real ANP data from official CSV endpoints.
    Handles Windows-1252 encoding and Brazilian decimal format.
    """
    if dataset_key not in ANP_DATASETS:
        raise HTTPException(
            status_code=404,
            detail=f"Dataset '{dataset_key}' not found. Available: {list(ANP_DATASETS.keys())}",
        )

    dataset = ANP_DATASETS[dataset_key]
    client = await _get_client()

    try:
        response = await client.get(dataset["csv_url"])
        response.raise_for_status()

        # ANP CSVs use Windows-1252 encoding and semicolon separator
        content = response.content
        for encoding in ["utf-8", "latin-1", "cp1252"]:
            try:
                text = content.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            text = content.decode("utf-8", errors="replace")

        # Parse CSV with Brazilian conventions
        df = pd.read_csv(
            io.StringIO(text),
            sep=";",
            decimal=",",
            encoding_errors="replace",
            on_bad_lines="skip",
        )

        # Filter by UF if provided
        if uf:
            uf_upper = uf.upper()
            uf_cols = [c for c in df.columns if "uf" in c.lower() or "estado" in c.lower() or "sigla" in c.lower()]
            if uf_cols:
                df = df[df[uf_cols[0]].astype(str).str.upper() == uf_upper]

        # Limit results
        df = df.head(limit)
        records = df.to_dict(orient="records")

        return {
            "source": f"ANP - {dataset['description']}",
            "dataset_key": dataset_key,
            "connection_type": "REST/CSV (dados.gov.br)",
            "encoding_handled": "Windows-1252 / Latin-1",
            "record_count": len(records),
            "columns": list(df.columns),
            "data": records,
        }

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"ANP returned error: {exc.response.text[:300]}",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error fetching ANP data: {str(exc)}",
        )


# ========================================================
# ANP Swagger / CKAN API (metadata queries)
# ========================================================
ANP_CKAN_BASE = "https://dados.gov.br/api/3/action"


@router.get("/search")
@cached(ttl=3600, key_prefix="anp_search")
async def search_anp_datasets(
    query: str = Query("petroleo", description="Search term"),
    rows: int = Query(10, ge=1, le=50, description="Number of results"),
):
    """
    Search ANP datasets via the CKAN API (Portal de Dados Abertos).
    Returns metadata in JSON format.
    """
    client = await _get_client()
    try:
        response = await client.get(
            f"{ANP_CKAN_BASE}/package_search",
            params={
                "q": f"ANP {query}",
                "rows": rows,
                "fq": "organization:agencia-nacional-do-petroleo-gas-natural-e-biocombustiveis-anp",
            },
        )
        response.raise_for_status()
        data = response.json()

        results = []
        for pkg in data.get("result", {}).get("results", []):
            results.append({
                "title": pkg.get("title", ""),
                "description": pkg.get("notes", "")[:200],
                "url": f"https://dados.gov.br/dados/conjuntos-dados/{pkg.get('name', '')}",
                "resources": len(pkg.get("resources", [])),
                "formats": list({r.get("format", "").upper() for r in pkg.get("resources", [])}),
            })

        return {
            "source": "ANP via CKAN API (dados.gov.br)",
            "connection_type": "REST API (JSON)",
            "query": query,
            "result_count": len(results),
            "results": results,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error searching ANP datasets: {str(exc)}",
        )
