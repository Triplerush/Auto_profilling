from typing import Annotated, Any, Literal, Union

from pydantic import BaseModel, Field

class AnalysisMetadata(BaseModel):
    id: str
    title: str
    description: str = ""
    author: str = ""
    created_at: str
    tags: list[str] = []
    colab_url: str | None = None
    github_url: str | None = None


class KPI(BaseModel):
    label: str
    value: str
    description: str = ""
    severity: Literal["ok", "warning", "critical"] = "ok"


class ChartDataset(BaseModel):
    label: str
    data: list[Any]


class ChartData(BaseModel):
    labels: list[str] = []
    datasets: list[ChartDataset] = []


class ChartComponent(BaseModel):
    type: Literal["chart"]
    title: str = ""
    chart_type: str
    data: ChartData
    config: dict = {}


class DataFrameData(BaseModel):
    columns: list[str]
    rows: list[list[Any]]


class DataFrameComponent(BaseModel):
    type: Literal["dataframe"]
    title: str = ""
    data: DataFrameData
    config: dict = {}


class MetricGridComponent(BaseModel):
    type: Literal["metric_grid"]
    title: str = ""
    metrics: list[dict]


class TextComponent(BaseModel):
    type: Literal["text"]
    content: str


class CorrelationMatrixComponent(BaseModel):
    type: Literal["correlation_matrix"]
    title: str = ""
    columns: list[str]
    matrix: list[list[float]]


class ConfusionMatrixComponent(BaseModel):
    type: Literal["confusion_matrix"]
    title: str = ""
    labels: list[str]
    matrix: list[list[int]]


class CodeSnippetComponent(BaseModel):
    type: Literal["code_snippet"]
    title: str = ""
    language: str = "python"
    code: str


class ImageComponent(BaseModel):
    type: Literal["image"]
    title: str = ""
    src: str
    alt: str = ""


Component = Annotated[
    Union[
        ChartComponent,
        DataFrameComponent,
        MetricGridComponent,
        TextComponent,
        CorrelationMatrixComponent,
        ConfusionMatrixComponent,
        CodeSnippetComponent,
        ImageComponent,
    ],
    Field(discriminator="type"),
]




class ModelInfo(BaseModel):
    artifact: str
    format: str = "joblib"
    input_schema: list[str]
    sample_input: dict[str, float | int]
    metrics: dict[str, float]




class AnalysisSection(BaseModel):
    title: str
    description: str = ""
    components: list[Component]


class AnalysisDetail(BaseModel):
    metadata: AnalysisMetadata
    kpis: list[KPI] = []
    sections: list[AnalysisSection] = []
    model: ModelInfo | None = None




class AnalysisSummary(BaseModel):
    id: str
    title: str
    description: str
    author: str
    created_at: str
    tags: list[str]
    kpi_count: int
    section_count: int
    has_model: bool = False
    colab_url: str | None = None
    github_url: str | None = None


class AnalysisListResponse(BaseModel):
    analyses: list[AnalysisSummary]
    total: int


class AnalysisUploadResponse(BaseModel):
    id: str
    title: str
    message: str
