import numpy as np
import pandas as pd

from app.models.schemas import CleaningSummary

NA_MARKERS = {
    "n/a", "na", "n.a.", "n.a", "nan", "null", "none", "-", "--",
    ".", "..", "...", "?", "??", "undefined", "missing", "vacío",
    "vacio", "sin dato", "sin datos", "no aplica", "no disponible",
}


def _rule_1_normalize_strings(df: pd.DataFrame) -> int:
    """Normalización de cadenas: strip + lowercase en columnas de texto."""
    count = 0
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        mask = df[col].notna()
        original = df.loc[mask, col]
        cleaned = original.str.strip().str.lower()
        changed = (original != cleaned).sum()
        count += int(changed)
        df.loc[mask, col] = cleaned
    return count


def _rule_2_prune_empty(df: pd.DataFrame) -> tuple[pd.DataFrame, int, int]:
    """Poda topológica: elimina filas/columnas totalmente vacías."""
    rows_before = len(df)
    df = df.dropna(how="all", axis=0)
    rows_removed = rows_before - len(df)

    cols_before = len(df.columns)
    df = df.dropna(how="all", axis=1)
    cols_removed = cols_before - len(df.columns)

    return df, rows_removed, cols_removed


def _rule_3_deduplicate(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Deduplicación: elimina calcos exactos manteniendo el primero."""
    rows_before = len(df)
    df = df.drop_duplicates(keep="first")
    return df, rows_before - len(df)


def _rule_4_coerce_types(df: pd.DataFrame) -> int:
    """Coerción de tipos: convierte marcadores humanos a NaN real y ajusta tipos numéricos."""
    coerced = 0
    str_cols = df.select_dtypes(include="object").columns

    for col in str_cols:
        mask = df[col].notna() & df[col].str.lower().str.strip().isin(NA_MARKERS)
        hits = int(mask.sum())
        if hits > 0:
            df.loc[mask, col] = np.nan
            coerced += hits

    for col in str_cols:
        if col not in df.columns:
            continue
        try:
            numeric = pd.to_numeric(df[col], errors="coerce")
            non_null_original = df[col].notna().sum()
            non_null_numeric = numeric.notna().sum()
            if non_null_numeric > 0 and (non_null_numeric / max(non_null_original, 1)) > 0.5:
                df[col] = numeric
        except Exception:
            continue

    return coerced


def _rule_5_flag_outliers(df: pd.DataFrame) -> int:
    """Etiquetado de atípicos con vallas de Tukey (Q1 - 1.5*IQR, Q3 + 1.5*IQR)."""
    flagged = 0
    num_cols = df.select_dtypes(include="number").columns

    for col in num_cols:
        series = df[col].dropna()
        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outlier_mask = df[col].notna() & ((df[col] < lower) | (df[col] > upper))
        hits = int(outlier_mask.sum())
        if hits > 0:
            flag_col = f"{col}__outlier"
            df[flag_col] = np.where(outlier_mask, True, False)
            flagged += hits

    return flagged


def run_cleaning_pipeline(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, CleaningSummary]:
    """Ejecuta las 5 reglas de limpieza en orden. Retorna (df_limpio, df_dlq, resumen)."""
    strings_normalized = _rule_1_normalize_strings(df)
    df, empty_rows, empty_cols = _rule_2_prune_empty(df)
    df, duplicates_removed = _rule_3_deduplicate(df)
    values_coerced = _rule_4_coerce_types(df)
    outliers_flagged = _rule_5_flag_outliers(df)

    # DLQ: filas con más del 80% de nulos (corrupción irreparable)
    original_cols = [c for c in df.columns if not c.endswith("__outlier")]
    null_ratio = df[original_cols].isnull().sum(axis=1) / max(len(original_cols), 1)
    dlq_mask = null_ratio > 0.8
    df_dlq = df[dlq_mask].copy()
    df_clean = df[~dlq_mask].copy()

    summary = CleaningSummary(
        strings_normalized=strings_normalized,
        empty_rows_removed=empty_rows,
        empty_cols_removed=empty_cols,
        duplicates_removed=duplicates_removed,
        values_coerced=values_coerced,
        outliers_flagged=outliers_flagged,
        dlq_records=len(df_dlq),
    )

    return df_clean, df_dlq, summary
