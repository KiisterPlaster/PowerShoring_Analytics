"""
PowerShoring Analytics — GeoAlchemy2 ORM Models

Maps all PostGIS tables from init.sql to SQLAlchemy models with
proper Geometry column types for spatial queries.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, Boolean,
    ARRAY as PgArray, Numeric, func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PgUUID
from geoalchemy2 import Geometry

from core.database import Base


class Cluster(Base):
    """Industrial cluster from Atlas do Futuro Industrial 2025."""
    __tablename__ = "clusters"

    id = Column(String(50), primary_key=True)
    name = Column(String(200), nullable=False)
    region = Column(String(50), nullable=False)
    state = Column(String(10), nullable=False)
    port = Column(String(200))
    vocations = Column(PgArray(Text))
    energy_sources = Column(PgArray(Text))
    critical_minerals = Column(PgArray(Text))
    hydrogen_potential = Column(Text)
    description = Column(Text)
    geom = Column(Geometry("POINT", srid=4326))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class SpatialLayer(Base):
    """Generic spatial layer from ArcGIS PID or external sources."""
    __tablename__ = "spatial_layers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    layer_key = Column(String(100), unique=True, nullable=False)
    source = Column(String(100), nullable=False)
    display_name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text)
    geom = Column(Geometry("GEOMETRY", srid=4326))
    properties = Column(JSONB, default={})
    fetched_at = Column(DateTime, default=func.now())


class IBGEData(Base):
    """IBGE SIDRA data (PIB, PAM, PEVS, BDiA)."""
    __tablename__ = "ibge_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_table = Column(String(20), nullable=False)
    source_name = Column(String(100), nullable=False)
    territorial_level = Column(String(5), nullable=False)
    ibge_code = Column(String(20))
    period = Column(String(20))
    variable_code = Column(String(20))
    variable_name = Column(String(200))
    value = Column(Numeric)
    unit = Column(String(50))
    municipality_name = Column(String(200))
    state_code = Column(String(5))
    raw_data = Column(JSONB, default={})
    fetched_at = Column(DateTime, default=func.now())


class ANPData(Base):
    """ANP energy data (petroleum, gas, biofuels, reserves)."""
    __tablename__ = "anp_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_key = Column(String(50), nullable=False)
    uf = Column(String(5))
    period = Column(String(20))
    product = Column(String(100))
    value = Column(Numeric)
    unit = Column(String(50))
    raw_data = Column(JSONB, default={})
    fetched_at = Column(DateTime, default=func.now())


class MapBiomasData(Base):
    """MapBiomas land use/cover data."""
    __tablename__ = "mapbiomas_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    land_use_class = Column(Integer)
    land_use_name = Column(String(200))
    area_ha = Column(Numeric)
    municipality_code = Column(String(20))
    state = Column(String(5))
    biome = Column(String(50))
    geom = Column(Geometry("GEOMETRY", srid=4326))
    raw_data = Column(JSONB, default={})
    fetched_at = Column(DateTime, default=func.now())


class TerraBrasilisData(Base):
    """INPE TerraBrasilis deforestation data (PRODES/DETER)."""
    __tablename__ = "terrabrasilis_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    program = Column(String(20), nullable=False)
    year = Column(Integer)
    state = Column(String(5))
    municipality = Column(String(200))
    area_km2 = Column(Numeric)
    biome = Column(String(50))
    geom = Column(Geometry("GEOMETRY", srid=4326))
    raw_data = Column(JSONB, default={})
    fetched_at = Column(DateTime, default=func.now())


class EPEData(Base):
    """EPE energy system data (WebMap + BEN)."""
    __tablename__ = "epe_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(50), nullable=False)
    category = Column(String(100))
    name = Column(String(300))
    energy_type = Column(String(100))
    capacity_mw = Column(Numeric)
    state = Column(String(5))
    geom = Column(Geometry("GEOMETRY", srid=4326))
    raw_data = Column(JSONB, default={})
    fetched_at = Column(DateTime, default=func.now())


class ANEELData(Base):
    """ANEEL SIGA power generation data."""
    __tablename__ = "aneel_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    plant_name = Column(String(300))
    plant_type = Column(String(100))
    fuel_source = Column(String(100))
    capacity_kw = Column(Numeric)
    status = Column(String(50))
    state = Column(String(5))
    municipality = Column(String(200))
    geom = Column(Geometry("POINT", srid=4326))
    raw_data = Column(JSONB, default={})
    fetched_at = Column(DateTime, default=func.now())


class CONABData(Base):
    """CONAB agricultural production data."""
    __tablename__ = "conab_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product = Column(String(100), nullable=False)
    harvest_year = Column(String(20))
    state = Column(String(5))
    area_planted_ha = Column(Numeric)
    production_tons = Column(Numeric)
    yield_kg_ha = Column(Numeric)
    raw_data = Column(JSONB, default={})
    fetched_at = Column(DateTime, default=func.now())


class InternationalData(Base):
    """International data (World Bank, IRENA, World Steel)."""
    __tablename__ = "international_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(50), nullable=False)
    indicator_code = Column(String(100))
    indicator_name = Column(String(300))
    country_code = Column(String(10))
    country_name = Column(String(100))
    year = Column(Integer)
    value = Column(Numeric)
    unit = Column(String(50))
    raw_data = Column(JSONB, default={})
    fetched_at = Column(DateTime, default=func.now())


class ETLJob(Base):
    """ETL pipeline job tracking."""
    __tablename__ = "etl_jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(PgUUID(as_uuid=True))
    source = Column(String(100), nullable=False)
    status = Column(String(20), default="pending")
    records_processed = Column(Integer, default=0)
    error_message = Column(Text)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
