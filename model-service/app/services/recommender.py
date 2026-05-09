from app.services.model_registry import _ModelEntry
from app.services.predictor import predict


def _decode_user_categories(features: dict, match_fields: list[str], input_schema: list[str]) -> dict[str, str]:
    """For each match_field, find which one-hot column is set to 1.

    Returns {field: chosen_value}. Field is omitted if no column is set.
    """
    chosen: dict[str, str] = {}
    for field in match_fields:
        prefix = f"{field}_"
        for col in input_schema:
            if not col.startswith(prefix):
                continue
            if features.get(col) == 1 or features.get(col) == 1.0:
                chosen[field] = col[len(prefix):]
                break
    return chosen


def recommend(entry: _ModelEntry, features: dict[str, float | int], top_k: int | None = None) -> dict:
    """Predict rating for `features` and return catalog items closest to it.

    Ranking: (1) more matching categorical fields first, (2) smaller |rating - prediction|.
    """
    rec_cfg = entry.recommendation
    if not rec_cfg or not rec_cfg.get("enabled"):
        raise ValueError("Recommendation is not enabled for this model")

    catalog = rec_cfg.get("catalog") or []
    if not catalog:
        raise ValueError("Recommendation catalog is empty")

    rating_field = rec_cfg.get("rating_field", "rating")
    match_fields = rec_cfg.get("match_fields", [])
    display_fields = rec_cfg.get("display_fields") or list(catalog[0].keys())
    k = top_k or rec_cfg.get("top_k", 5)

    pred = predict(entry, features)
    predicted_rating = float(pred["prediction"])

    user_categories = _decode_user_categories(features, match_fields, entry.input_schema)

    scored = []
    for item in catalog:
        rating = item.get(rating_field)
        if rating is None:
            continue
        matches = sum(1 for f, v in user_categories.items() if item.get(f) == v)
        distance = abs(float(rating) - predicted_rating)
        scored.append((matches, distance, item))

    scored.sort(key=lambda x: (-x[0], x[1]))
    top = scored[:k]

    items = []
    for matches, distance, item in top:
        out = {f: item.get(f) for f in display_fields if f in item}
        out["match_count"] = matches
        out["rating_distance"] = round(distance, 4)
        items.append(out)

    return {
        "predicted_rating": round(predicted_rating, 4),
        "user_categories": user_categories,
        "items": items,
        "rating_field": rating_field,
        "display_fields": display_fields,
        "label": rec_cfg.get("label", "Top recomendaciones"),
        "latency_ms": pred["latency_ms"],
    }
