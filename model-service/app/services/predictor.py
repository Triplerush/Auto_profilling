import time

from app.services.model_registry import _ModelEntry


def _to_python_native(value):
    """Convert numpy types to Python native."""
    if hasattr(value, "item"):
        return value.item()
    if hasattr(value, "tolist"):
        return value.tolist()
    return value


def predict(entry: _ModelEntry, features: dict[str, float | int]) -> dict:
    """Run prediction on a loaded model.

    Returns dict with: prediction, probability, confidence, latency_ms.
    """
    # Validate all required features are present
    missing = set(entry.input_schema) - set(features.keys())
    if missing:
        raise ValueError(f"Missing features: {missing}")

    # Build input in correct column order
    ordered_values = [features[col] for col in entry.input_schema]
    input_2d = [ordered_values]

    model = entry.model
    start = time.perf_counter()

    # Predict
    raw_prediction = model.predict(input_2d)
    prediction = _to_python_native(raw_prediction[0])

    # Try to get probability
    probability = None
    confidence = None
    if hasattr(model, "predict_proba"):
        try:
            proba = model.predict_proba(input_2d)[0]
            proba_list = [_to_python_native(p) for p in proba]
            # Confidence = probability of the predicted class
            pred_idx = int(prediction) if isinstance(prediction, (int, float)) else 0
            if pred_idx < len(proba_list):
                confidence = round(proba_list[pred_idx], 4)
            probability = round(max(proba_list), 4)
        except Exception:
            pass

    latency_ms = round((time.perf_counter() - start) * 1000, 2)
    entry.record_prediction(latency_ms)

    return {
        "prediction": prediction,
        "probability": probability,
        "confidence": confidence,
        "latency_ms": latency_ms,
    }
