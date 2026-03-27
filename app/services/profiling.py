import pandas as pd

from app.models.schemas import ColumnProfile, HealthSummary


def generate_health_summary(df: pd.DataFrame) -> HealthSummary:
    """Genera el reporte de salud del dataset basado en dimensiones de calidad."""
    total_rows = len(df)
    total_cols = len(df.columns)
    memory_mb = round(df.memory_usage(deep=True).sum() / (1024 * 1024), 4)

    duplicates = int(df.duplicated().sum())
    dup_pct = round((duplicates / max(total_rows, 1)) * 100, 2)

    total_nulls = int(df.isnull().sum().sum())
    total_cells = total_rows * total_cols
    null_pct = round((total_nulls / max(total_cells, 1)) * 100, 2)

    columns = []
    for col in df.columns:
        null_count = int(df[col].isnull().sum())
        unique_count = int(df[col].nunique())
        columns.append(
            ColumnProfile(
                name=col,
                dtype=str(df[col].dtype),
                null_count=null_count,
                null_percent=round((null_count / max(total_rows, 1)) * 100, 2),
                unique_count=unique_count,
                unique_percent=round((unique_count / max(total_rows, 1)) * 100, 2),
            )
        )

    return HealthSummary(
        total_rows=total_rows,
        total_columns=total_cols,
        memory_usage_mb=memory_mb,
        duplicate_rows=duplicates,
        duplicate_percent=dup_pct,
        total_nulls=total_nulls,
        total_null_percent=null_pct,
        columns=columns,
    )
