"""
PowerShoring Analytics — FastAPI Application Entry Point
A strategic decision platform for Brazil's green reindustrialization.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api.arcgis_proxy import router as arcgis_router
from api.dados_ibge import router as ibge_router
from api.clusters import router as clusters_router
from api.matchmaker import router as matchmaker_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown lifecycle."""
    print(f"[START] {settings.APP_NAME} v{settings.APP_VERSION} starting...")
    print(f"[ARCGIS] Base: {settings.ARCGIS_BASE_URL}")
    print(f"[LAYERS] Registered: {len(settings.ARCGIS_LAYERS)}")
    print(f"[CLUSTERS] Loaded: 9 (Atlas 2025)")
    print(f"[AI] Model: {settings.OPENAI_MODEL}")
    yield
    print("[STOP] Shutting down PowerShoring Analytics...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Plataforma de suporte à decisão para a neoindustrialização verde do Brasil. "
        "Cruza infraestrutura logística, energia limpa e clusters industriais "
        "para orientar investimentos estratégicos (Powershoring)."
    ),
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(arcgis_router)
app.include_router(ibge_router)
app.include_router(clusters_router)
app.include_router(matchmaker_router)


@app.get("/api/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "version": settings.APP_VERSION,
        "service": settings.APP_NAME,
        "layers_available": len(settings.ARCGIS_LAYERS),
        "clusters_loaded": 9,
        "ai_model": settings.OPENAI_MODEL,
    }
