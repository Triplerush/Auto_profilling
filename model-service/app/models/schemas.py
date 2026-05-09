from typing import Any

from pydantic import BaseModel


class RecommendationConfig(BaseModel):
    enabled: bool = True
    label: str = "Top recomendaciones"
    rating_field: str = "rating"
    match_fields: list[str] = []
    display_fields: list[str] = []
    top_k: int = 5


class ModelInfo(BaseModel):
    id: str
    analysis_title: str
    artifact: str
    format: str
    input_schema: list[str]
    sample_input: dict[str, Any]
    metrics: dict[str, float]
    recommendation: RecommendationConfig | None = None


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


class RecommendRequest(BaseModel):
    features: dict[str, float | int]
    top_k: int | None = None


class RecommendItem(BaseModel):
    title: str | None = None
    type: str | None = None
    genre: str | None = None
    platform: str | None = None
    country: str | None = None
    language: str | None = None
    release_year: int | None = None
    duration_minutes: int | None = None
    rating: float | None = None
    votes: int | None = None
    match_count: int = 0
    rating_distance: float = 0.0


class RecommendResponse(BaseModel):
    predicted_rating: float
    user_categories: dict[str, str]
    items: list[dict[str, Any]]
    rating_field: str
    display_fields: list[str]
    label: str
    latency_ms: float | None = None
