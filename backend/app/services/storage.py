import json
from pathlib import Path

import redis.asyncio as redis

from app.core.config import settings
from app.models.schemas import TaskStatus

_redis: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def close_redis() -> None:
    global _redis
    if _redis is not None:
        await _redis.close()
        _redis = None


def ensure_dirs() -> None:
    """Crea los directorios necesarios para almacenamiento temporal."""
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.output_dir.mkdir(parents=True, exist_ok=True)
    settings.dlq_dir.mkdir(parents=True, exist_ok=True)


async def save_task(task_id: str, data: dict) -> None:
    r = await get_redis()
    await r.set(f"task:{task_id}", json.dumps(data), ex=settings.task_ttl_seconds)


async def get_task(task_id: str) -> dict | None:
    r = await get_redis()
    raw = await r.get(f"task:{task_id}")
    if raw is None:
        return None
    return json.loads(raw)


async def update_task_status(task_id: str, status: TaskStatus, **extra) -> None:
    data = await get_task(task_id)
    if data is None:
        return
    data["status"] = status.value
    data.update(extra)
    await save_task(task_id, data)


def get_output_path(task_id: str) -> Path:
    return settings.output_dir / f"{task_id}.csv"


def get_dlq_path(task_id: str) -> Path:
    return settings.dlq_dir / f"{task_id}_dlq.csv"
