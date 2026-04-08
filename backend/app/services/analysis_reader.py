import json
import logging
from pathlib import Path

from app.core.config import settings
from app.models.analysis_schemas import AnalysisDetail, AnalysisSummary

logger = logging.getLogger(__name__)


def _read_json(path: Path) -> dict | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Error reading %s: %s", path.name, e)
        return None


def list_analyses() -> list[AnalysisSummary]:
    results_dir = settings.results_dir
    if not results_dir.exists():
        return []

    summaries = []
    for path in sorted(results_dir.glob("*.json")):
        if path.name.startswith("."):
            continue
        raw = _read_json(path)
        if raw is None:
            continue
        try:
            detail = AnalysisDetail.model_validate(raw)
            meta = detail.metadata
            summaries.append(AnalysisSummary(
                id=meta.id,
                title=meta.title,
                description=meta.description,
                author=meta.author,
                created_at=meta.created_at,
                tags=meta.tags,
                kpi_count=len(detail.kpis),
                section_count=len(detail.sections),
                has_model=detail.model is not None,
                colab_url=meta.colab_url,
                github_url=meta.github_url,
            ))
        except Exception as e:
            logger.warning("Validation failed for %s: %s", path.name, e)
    return summaries


def get_analysis_by_id(analysis_id: str) -> AnalysisDetail | None:
    results_dir = settings.results_dir
    if not results_dir.exists():
        return None

    for path in results_dir.glob("*.json"):
        if path.name.startswith("."):
            continue
        raw = _read_json(path)
        if raw is None:
            continue
        try:
            detail = AnalysisDetail.model_validate(raw)
            if detail.metadata.id == analysis_id:
                return detail
        except Exception:
            continue
    return None


def save_analysis(data: AnalysisDetail) -> Path:
    results_dir = settings.results_dir
    results_dir.mkdir(parents=True, exist_ok=True)
    path = results_dir / f"{data.metadata.id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data.model_dump(), f, indent=2, ensure_ascii=False)
    return path
