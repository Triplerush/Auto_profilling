VALID_SEVERITIES = {"ok", "warning", "critical"}
VALID_COMPONENT_TYPES = {
    "chart", "dataframe", "metric_grid", "text",
    "correlation_matrix", "confusion_matrix", "code_snippet", "image",
}


def validate_report(data: dict):
    errors = []

    metadata = data.get("metadata")
    if not metadata:
        errors.append("Missing 'metadata'")
    else:
        for field in ("id", "title", "created_at"):
            if not metadata.get(field):
                errors.append(f"metadata.{field} is required")

    for i, kpi in enumerate(data.get("kpis", [])):
        if not kpi.get("label"):
            errors.append(f"kpis[{i}].label is required")
        if not kpi.get("value"):
            errors.append(f"kpis[{i}].value is required")
        severity = kpi.get("severity", "ok")
        if severity not in VALID_SEVERITIES:
            errors.append(f"kpis[{i}].severity '{severity}' not in {VALID_SEVERITIES}")

    sections = data.get("sections", [])
    if not sections:
        errors.append("At least one section is required")

    for i, section in enumerate(sections):
        if not section.get("title"):
            errors.append(f"sections[{i}].title is required")
        components = section.get("components", [])
        if not components:
            errors.append(f"sections[{i}] has no components")
        for j, comp in enumerate(components):
            comp_type = comp.get("type")
            if comp_type not in VALID_COMPONENT_TYPES:
                errors.append(
                    f"sections[{i}].components[{j}].type '{comp_type}' not in {VALID_COMPONENT_TYPES}"
                )

    model = data.get("model")
    if model:
        required_model_keys = {"artifact", "format", "input_schema", "sample_input", "metrics"}
        missing = required_model_keys - set(model.keys())
        if missing:
            errors.append(f"model is missing keys: {missing}")
        if not isinstance(model.get("input_schema"), list):
            errors.append("model.input_schema must be a list")
        if not isinstance(model.get("sample_input"), dict):
            errors.append("model.sample_input must be a dict")
        if not isinstance(model.get("metrics"), dict):
            errors.append("model.metrics must be a dict")

    if errors:
        raise ValueError("Data Contract validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
