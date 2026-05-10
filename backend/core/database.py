"""
PowerShoring Analytics — Async Database Engine

Provides:
  - AsyncSession factory via create_async_engine (asyncpg driver)
  - Sync engine fallback for GeoPandas operations (psycopg2)
  - Connection pool with health checks
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


# ============================================================
# Async Engine (asyncpg driver for FastAPI endpoints)
# ============================================================
_async_database_url = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)

async_engine = create_async_engine(
    _async_database_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide an async database session with automatic cleanup."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ============================================================
# Sync Engine (psycopg2 driver for GeoPandas operations)
# ============================================================
_sync_engine: Engine | None = None


def get_sync_engine() -> Engine:
    """Return a sync SQLAlchemy engine for GeoPandas read_postgis/to_postgis."""
    global _sync_engine
    if _sync_engine is None:
        _sync_engine = create_engine(
            settings.DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            echo=settings.DEBUG,
        )
    return _sync_engine


# ============================================================
# Base Model for GeoAlchemy2 ORM
# ============================================================
class Base(DeclarativeBase):
    """Declarative base for all ORM models."""
    pass
