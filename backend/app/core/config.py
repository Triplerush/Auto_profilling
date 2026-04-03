from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "Auto Profiling - Notebook Viewer"
    app_version: str = "2.0.0"
    debug: bool = False

    notebooks_dir: Path = Path("/app/notebooks")
    results_dir: Path = Path("/app/results")

    model_config = {"env_prefix": "PROFILING_"}


settings = Settings()
