"""
IBGE / SIDRA Data Router — Consumes real IBGE SIDRA API v3 for socioeconomic data.
"""
import sidrapy
import pandas as pd
import httpx
from fastapi import APIRouter, HTTPException, Query
from core.cache import cached

router = APIRouter(prefix="/api/ibge", tags=["IBGE / SIDRA / BDiA"])


@router.get("/pib")
@cached(ttl=86400, key_prefix="sidra_pib")
async def get_pib_municipal(
    territorial_level: str = Query("3", description="1=Brasil, 2=UF, 3=Município"),
    ibge_code: str = Query("all", description="IBGE territorial code or 'all'"),
    period: str = Query("last 1", description="Period filter (e.g. 'last 5')"),
):
    """
    Fetch GDP (PIB) per capita data from SIDRA Table 5938.
    Returns real IBGE data, not mocks.
    """
    try:
        data = sidrapy.get_table(
            table_code="5938",
            territorial_level=territorial_level,
            ibge_territorial_code=ibge_code,
            variable="37",
            period=period,
        )
        df = pd.DataFrame(data)
        # Clean SIDRA header row
        if len(df) > 0 and df.iloc[0].str.contains("Valor", na=False).any():
            df = df.iloc[1:]
        records = df.to_dict(orient="records")
        return {
            "source": "IBGE SIDRA — Tabela 5938 (PIB dos Municípios)",
            "table_code": "5938",
            "territorial_level": territorial_level,
            "record_count": len(records),
            "data": records,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error fetching SIDRA data: {str(exc)}",
        )


@router.get("/pam")
@cached(ttl=86400, key_prefix="sidra_pam")
async def get_producao_agricola(
    territorial_level: str = Query("3", description="1=Brasil, 2=UF, 3=Município"),
    ibge_code: str = Query("all", description="IBGE territorial code or 'all'"),
    variable: str = Query("214", description="214=Quantidade produzida (toneladas)"),
    period: str = Query("last 1", description="Period filter"),
    classification: str = Query("81/all", description="Crop classification"),
):
    """
    Fetch PAM (Produção Agrícola Municipal) from SIDRA Table 1419.
    Essential for biomass/biofuel feedstock mapping.
    """
    try:
        data = sidrapy.get_table(
            table_code="1419",
            territorial_level=territorial_level,
            ibge_territorial_code=ibge_code,
            variable=variable,
            period=period,
            classifications={classification.split("/")[0]: classification.split("/")[1]},
        )
        df = pd.DataFrame(data)
        if len(df) > 0 and df.iloc[0].str.contains("Valor", na=False).any():
            df = df.iloc[1:]
        records = df.to_dict(orient="records")
        return {
            "source": "IBGE SIDRA — Tabela 1419 (PAM - Produção Agrícola Municipal)",
            "table_code": "1419",
            "territorial_level": territorial_level,
            "record_count": len(records),
            "data": records,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error fetching PAM data: {str(exc)}",
        )


@router.get("/pevs")
@cached(ttl=86400, key_prefix="sidra_pevs")
async def get_extracao_vegetal(
    territorial_level: str = Query("2", description="1=Brasil, 2=UF"),
    ibge_code: str = Query("all", description="IBGE territorial code or 'all'"),
    period: str = Query("last 1", description="Period filter"),
):
    """
    Fetch PEVS (Produção Extração Vegetal e Silvicultura) from SIDRA Table 289.
    Used for charcoal/forestry data essential for green steel analysis.
    """
    try:
        data = sidrapy.get_table(
            table_code="289",
            territorial_level=territorial_level,
            ibge_territorial_code=ibge_code,
            variable="all",
            period=period,
        )
        df = pd.DataFrame(data)
        if len(df) > 0 and df.iloc[0].str.contains("Valor", na=False).any():
            df = df.iloc[1:]
        records = df.to_dict(orient="records")
        return {
            "source": "IBGE SIDRA — Tabela 289 (PEVS - Extração Vegetal e Silvicultura)",
            "table_code": "289",
            "territorial_level": territorial_level,
            "record_count": len(records),
            "data": records,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error fetching PEVS data: {str(exc)}",
        )


@router.get("/bdia/metadata")
@cached(ttl=86400, key_prefix="bdia_meta")
async def get_bdia_metadata():
    """
    Returns metadata catalog endpoint details for BDiA (Banco de Informações Ambientais).
    IBGE uses separate infrastructure for BDiA.
    """
    return {
        "source": "IBGE BDiA",
        "description": "Coleção de bases temáticas de recursos naturais: Geologia, Pedologia, Vegetação.",
        "web_portal": "https://bdiaweb.ibge.gov.br/#/home",
        "api_notes": "Data vectors stored locally in spatial_layers via ETL processes.",
        "available_themes": ["Geomorfologia", "Geologia", "Pedologia", "Vegetação"]
    }
