import json
import logging
import time
from pathlib import Path

from app.core.config import settings

logger = logging.getLogger(__name__)


class _ModelEntry:
    """Cached entry for a discovered model."""

    def __init__(self, analysis_id: str, analysis_title: str, model_meta: dict, json_path: Path):
        self.analysis_id = analysis_id
        self.analysis_title = analysis_title
        self.artifact = model_meta["artifact"]
        self.format = model_meta["format"]
        self.input_schema: list[str] = model_meta["input_schema"]
        self.sample_input: dict = model_meta["sample_input"]
        self.metrics: dict = model_meta["metrics"]
        self.json_path = json_path

        # Lazy-loaded model object
        self._model = None

        # Stats
        self.total_predictions = 0
        self.cumulative_latency = 0.0
        self.last_prediction_at: str | None = None

    @property
    def artifact_path(self) -> Path:
        return self.json_path.parent / self.artifact

    def load_model(self):
        """Load the model from disk (lazy, on first predict)."""
        if self._model is not None:
            return self._model

        import joblib

        path = self.artifact_path
        if not path.exists():
            raise FileNotFoundError(f"Model artifact not found: {path}")

        logger.info("Loading model from %s", path)
        self._model = joblib.load(path)
        return self._model

    @property
    def model(self):
        return self.load_model()

    def record_prediction(self, latency_ms: float):
        self.total_predictions += 1
        self.cumulative_latency += latency_ms
        self.last_prediction_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    @property
    def avg_latency_ms(self) -> float:
        if self.total_predictions == 0:
            return 0.0
        return round(self.cumulative_latency / self.total_predictions, 2)


class ModelRegistry:
    """Scans results/ for Data Contracts with model field, caches metadata."""

    def __init__(self):
        self._entries: dict[str, _ModelEntry] = {}
        self._scanned = False

    def _scan(self):
        """Scan results directory for JSON files with a model field."""
        results_dir = settings.results_dir
        if not results_dir.exists():
            logger.warning("Results directory does not exist: %s", results_dir)
            return

        for path in sorted(results_dir.glob("*.json")):
            if path.name.startswith("."):
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logger.warning("Error reading %s: %s", path.name, e)
                continue

            model_meta = data.get("model")
            if not model_meta:
                continue

            metadata = data.get("metadata", {})
            analysis_id = metadata.get("id", path.stem)
            analysis_title = metadata.get("title", analysis_id)

            artifact_path = path.parent / model_meta["artifact"]
            if not artifact_path.exists():
                logger.warning("Model artifact missing for %s: %s", analysis_id, artifact_path)
                continue

            self._entries[analysis_id] = _ModelEntry(
                analysis_id=analysis_id,
                analysis_title=analysis_title,
                model_meta=model_meta,
                json_path=path,
            )
            logger.info("Discovered model: %s (%s)", analysis_id, model_meta["artifact"])

        self._scanned = True

    def _ensure_scanned(self):
        if not self._scanned:
            self._scan()

    def list_models(self) -> list[_ModelEntry]:
        self._ensure_scanned()
        return list(self._entries.values())

    def get_model(self, model_id: str) -> _ModelEntry | None:
        self._ensure_scanned()
        return self._entries.get(model_id)

    def reload(self):
        """Force re-scan of results directory."""
        self._entries.clear()
        self._scanned = False
        self._scan()


registry = ModelRegistry()
