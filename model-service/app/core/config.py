from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Auto Profiling - Model Service"
    app_version: str = "1.0.0"
    debug: bool = False

    results_dir: Path = Path("/app/results")

    model_config = {"env_prefix": "MODEL_"}


settings = Settings()
