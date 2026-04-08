from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    ModelInfo,
    ModelListResponse,
    ModelStats,
    PredictRequest,
    PredictResponse,
)
from app.services.model_registry import registry
from app.services.predictor import predict

router = APIRouter(prefix="/v1/models", tags=["models"])


@router.get("", response_model=ModelListResponse)
def list_models():
    entries = registry.list_models()
    models = [
        ModelInfo(
            id=e.analysis_id,
            analysis_title=e.analysis_title,
            artifact=e.artifact,
            format=e.format,
            input_schema=e.input_schema,
            sample_input=e.sample_input,
            metrics=e.metrics,
        )
        for e in entries
    ]
    return ModelListResponse(models=models, total=len(models))


@router.get("/{model_id}", response_model=ModelInfo)
def get_model(model_id: str):
    entry = registry.get_model(model_id)
    if not entry:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found")
    return ModelInfo(
        id=entry.analysis_id,
        analysis_title=entry.analysis_title,
        artifact=entry.artifact,
        format=entry.format,
        input_schema=entry.input_schema,
        sample_input=entry.sample_input,
        metrics=entry.metrics,
    )


@router.post("/{model_id}/predict", response_model=PredictResponse)
def predict_model(model_id: str, request: PredictRequest):
    entry = registry.get_model(model_id)
    if not entry:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found")

    try:
        result = predict(entry, request.features)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return PredictResponse(
        prediction=result["prediction"],
        probability=result["probability"],
        confidence=result["confidence"],
        input_received=request.features,
    )


@router.get("/{model_id}/stats", response_model=ModelStats)
def get_model_stats(model_id: str):
    entry = registry.get_model(model_id)
    if not entry:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found")
    return ModelStats(
        total_predictions=entry.total_predictions,
        avg_latency_ms=entry.avg_latency_ms,
        last_prediction_at=entry.last_prediction_at,
    )
