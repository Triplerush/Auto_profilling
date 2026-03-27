from pydantic import BaseModel
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class ColumnProfile(BaseModel):
    name: str
    dtype: str
    null_count: int
    null_percent: float
    unique_count: int
    unique_percent: float


class HealthSummary(BaseModel):
    total_rows: int
    total_columns: int
    memory_usage_mb: float
    duplicate_rows: int
    duplicate_percent: float
    total_nulls: int
    total_null_percent: float
    columns: list[ColumnProfile]


class CleaningSummary(BaseModel):
    strings_normalized: int
    empty_rows_removed: int
    empty_cols_removed: int
    duplicates_removed: int
    values_coerced: int
    outliers_flagged: int
    dlq_records: int


class ProcessResponse(BaseModel):
    task_id: str
    status: TaskStatus
    health_summary: HealthSummary
    cleaning_summary: CleaningSummary
    download_url: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: TaskStatus
    health_summary: HealthSummary | None = None
    cleaning_summary: CleaningSummary | None = None
    download_url: str | None = None
    error: str | None = None
