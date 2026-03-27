from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "Auto Profiling API"
    app_version: str = "1.0.0"
    debug: bool = False

    redis_url: str = "redis://redis:6379/0"

    upload_dir: Path = Path("/tmp/profiling/uploads")
    output_dir: Path = Path("/tmp/profiling/outputs")
    dlq_dir: Path = Path("/tmp/profiling/dlq")

    max_file_size_mb: int = 100
    task_ttl_seconds: int = 3600

    model_config = {"env_prefix": "PROFILING_"}


settings = Settings()
