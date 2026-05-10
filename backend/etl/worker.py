"""
PowerShoring Analytics — Celery Worker Config

Configures the task queue for running heavy ETL processes asynchronously.
Run using: celery -A etl.worker worker --loglevel=info
"""
import os
from celery import Celery
from core.config import settings

# Create instance
celery_app = Celery(
    "powershoring_etl",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max for massive spatial jobs
)

# Autodiscover tasks in etl directory
celery_app.autodiscover_tasks(['etl'], force=True)
