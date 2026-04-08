from typing import Any

from pydantic import BaseModel


class ModelInfo(BaseModel):
    id: str
    analysis_title: str
    artifact: str
    format: str
    input_schema: list[str]
    sample_input: dict[str, Any]
    metrics: dict[str, float]


class ModelListResponse(BaseModel):
    models: list[ModelInfo]
    total: int


class PredictRequest(BaseModel):
    features: dict[str, float | int]


class PredictResponse(BaseModel):
    prediction: Any
    probability: float | None = None
    confidence: float | None = None
    input_received: dict[str, float | int]


class ModelStats(BaseModel):
    total_predictions: int = 0
    avg_latency_ms: float = 0.0
    last_prediction_at: str | None = None
