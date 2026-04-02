from pydantic import BaseModel


# ──────────────────────────────────────────────
# Data Contract: Notebook Visualization Platform
# ──────────────────────────────────────────────


class NotebookSummary(BaseModel):
    """Resumen para la galeria de notebooks."""
    id: str
    filename: str
    title: str
    description: str
    cell_count: int
    code_cells: int
    markdown_cells: int
    has_images: bool
    has_dataframes: bool


class CellOutput(BaseModel):
    """Un output individual de una celda de codigo."""
    output_type: str  # text, html, image, error, dataframe
    content: str      # texto plano, HTML, base64, o JSON stringificado
    attrs: dict | None = None  # metadata adicional (ej: mime_type, alt_text)


class NotebookCell(BaseModel):
    """Celda parseada de un notebook."""
    index: int
    cell_type: str      # markdown, code
    source: str          # codigo fuente o markdown raw
    outputs: list[CellOutput]
    execution_count: int | None = None


class NotebookDetail(BaseModel):
    """Notebook completo parseado - Data Contract principal."""
    id: str
    filename: str
    title: str
    description: str
    cells: list[NotebookCell]


class NotebookListResponse(BaseModel):
    """Respuesta del endpoint de listado."""
    notebooks: list[NotebookSummary]
    total: int


class UploadResponse(BaseModel):
    """Respuesta al subir un notebook."""
    id: str
    filename: str
    message: str
