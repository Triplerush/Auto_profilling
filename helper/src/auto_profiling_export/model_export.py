from pathlib import Path


def _to_python_native(value):
    """Convert numpy/pandas types to Python native types for JSON serialization."""
    if hasattr(value, "item"):
        return value.item()
    if hasattr(value, "tolist"):
        return value.tolist()
    return value


def export_model(
    model,
    analysis_id: str,
    input_schema: list[str],
    sample_input: dict,
    metrics: dict,
    output_dir: str | Path,
    model_format: str = "joblib",
) -> dict:
    """Export a trained model as a joblib artifact and return Data Contract metadata.

    Args:
        model: Trained sklearn-compatible model with .predict() method.
        analysis_id: Slug ID matching the analysis (e.g. "dota2-pro-matches").
        input_schema: Ordered list of feature names the model expects.
        sample_input: Dict mapping feature names to example values.
        metrics: Dict of metric names to float values (e.g. {"accuracy": 0.63}).
        output_dir: Directory where the .joblib file will be saved.
        model_format: Serialization format (only "joblib" supported).

    Returns:
        Dict with the Data Contract model field structure.
    """
    try:
        import joblib
    except ImportError:
        raise ImportError(
            "joblib is required for model export. "
            "Install it with: pip install auto-profiling-export[ml]"
        )

    if model_format != "joblib":
        raise ValueError(f"Unsupported format '{model_format}'. Only 'joblib' is supported.")

    # Validate that the model can predict with the sample input
    ordered_values = [sample_input[col] for col in input_schema]
    try:
        model.predict([ordered_values])
    except Exception as e:
        raise ValueError(
            f"Model failed to predict with sample_input: {e}. "
            f"Ensure sample_input keys match input_schema."
        )

    # Serialize model
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_name = f"{analysis_id}_model.joblib"
    artifact_path = output_dir / artifact_name
    joblib.dump(model, artifact_path)

    # Build Data Contract model field
    clean_sample = {
        k: round(_to_python_native(v), 4) if isinstance(_to_python_native(v), float) else _to_python_native(v)
        for k, v in sample_input.items()
    }
    clean_metrics = {
        k: round(_to_python_native(v), 4)
        for k, v in metrics.items()
    }

    return {
        "artifact": artifact_name,
        "format": model_format,
        "input_schema": list(input_schema),
        "sample_input": clean_sample,
        "metrics": clean_metrics,
    }
