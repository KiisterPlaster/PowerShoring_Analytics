"""
PowerShoring Analytics — Redis Cache Module

Provides:
  - Global Redis client for caching external API responses.
  - Cache decorator for FastAPI routes.
  - Automatic expiration and fallback mechanism.
"""
import json
import logging
import functools
from typing import Any, Optional
from datetime import timedelta

import redis.asyncio as redis

from core.config import settings

logger = logging.getLogger(__name__)

# Global async redis client
_redis: Optional[redis.Redis] = None

async def get_redis_client() -> redis.Redis:
    """Lazy-init the async Redis client."""
    global _redis
    if _redis is None:
        logger.info(f"[Redis] Connecting to {settings.REDIS_URL}")
        _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis

async def cache_get(key: str) -> Optional[Any]:
    """Retrieve data from cache."""
    try:
        client = await get_redis_client()
        value = await client.get(key)
        if value:
            return json.loads(value)
    except Exception as e:
        logger.warning(f"[Redis] Cache get error: {e}")
    return None

async def cache_set(key: str, value: Any, ttl: int = 3600):
    """Store data in cache with time-to-live (seconds)."""
    try:
        client = await get_redis_client()
        await client.set(key, json.dumps(value), ex=ttl)
    except Exception as e:
        logger.warning(f"[Redis] Cache set error: {e}")

def cached(ttl: int = 3600, key_prefix: str = "api_cache"):
    """
    Decorator to cache an async function response.
    Useful for FastAPI route handlers consuming slow external APIs.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key based on function name and arguments
            arg_str = ":".join([str(a) for a in args])
            kwarg_str = ":".join([f"{k}={v}" for k, v in sorted(kwargs.items())])
            cache_key = f"{key_prefix}:{func.__name__}:{arg_str}:{kwarg_str}"
            
            # Try to fetch from cache
            cached_data = await cache_get(cache_key)
            if cached_data is not None:
                logger.info(f"[Cache HIT] {cache_key}")
                return cached_data
            
            # Cache miss: Execute function and store result
            logger.info(f"[Cache MISS] Executing {func.__name__}")
            result = await func(*args, **kwargs)
            
            # Store asynchronously and continue
            await cache_set(cache_key, result, ttl=ttl)
            return result
        return wrapper
    return decorator
