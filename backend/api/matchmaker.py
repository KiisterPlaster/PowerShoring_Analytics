"""
Matchmaker Router — AI-powered industrial investment recommendation engine.
"""
from fastapi import APIRouter, HTTPException

from core.ai_engine import run_matchmaker
from core.config import settings
from models.schemas import MatchmakerRequest, MatchmakerResponse

router = APIRouter(prefix="/api/matchmaker", tags=["AI Matchmaker"])


@router.post("/", response_model=MatchmakerResponse)
async def matchmaker(request: MatchmakerRequest):
    """
    Receive an investor query and return an AI-powered cluster recommendation.
    Uses GPT-4o with System Prompt Injection containing Atlas 2025 data.
    """
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key not configured. Set OPENAI_API_KEY in .env",
        )

    result = await run_matchmaker(request.query)
    return MatchmakerResponse(**result)
