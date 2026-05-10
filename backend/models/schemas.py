"""Pydantic schemas for API request/response validation."""
# pylint: disable=too-few-public-methods
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"


class MatchmakerRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Investor query describing the desired industrial project",
        examples=["Quero instalar uma planta de química verde para produção de e-metanol"],
    )


class MatchmakerResponse(BaseModel):
    cluster_recommended: str
    cluster_id: str
    location: str
    justification: str
    energy_profile: str
    logistics: str
    socioeconomic_impact: str
    transition_justa: str
    raw_model: str = ""


class ClusterOut(BaseModel):
    id: str
    name: str
    region: str
    state: str
    lat: float
    lng: float
    port: str
    vocations: list[str]
    energy_sources: list[str]
    critical_minerals: list[str]
    hydrogen_potential: str
    description: str


class LayerInfo(BaseModel):
    layer_key: str
    display_name: str
    category: str
    icon: str


class IBGEDataResponse(BaseModel):
    source: str
    table_code: str
    territorial_level: str
    data: list[dict]
