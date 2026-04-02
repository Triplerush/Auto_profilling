"""Parser de Jupyter Notebooks (.ipynb) a Data Contract JSON.

Lee archivos .ipynb, extrae celdas con sus outputs (texto, HTML/dataframes,
imagenes base64) y los estructura en el formato NotebookDetail que el
frontend renderiza directamente.
"""

import hashlib
import json
from pathlib import Path

from app.core.config import settings
from app.models.schemas import (
    CellOutput,
    NotebookCell,
    NotebookDetail,
    NotebookSummary,
)


def _generate_id(filename: str) -> str:
    """Genera un ID determinista a partir del nombre del archivo."""
    return hashlib.md5(filename.encode()).hexdigest()[:12]


def _extract_title(nb: dict, filename: str) -> str:
    """Extrae el titulo del primer markdown cell que tenga un heading #."""
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown":
            for line in cell.get("source", []):
                stripped = line.strip()
                if stripped.startswith("# "):
                    return stripped.lstrip("# ").strip()
    return filename.replace(".ipynb", "").replace("_", " ")


def _extract_description(nb: dict) -> str:
    """Extrae descripcion del primer markdown cell (lineas despues del titulo)."""
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown":
            lines = cell.get("source", [])
            desc_lines = []
            past_title = False
            for line in lines:
                stripped = line.strip()
                if not past_title:
                    if stripped.startswith("# "):
                        past_title = True
                    continue
                if stripped and not stripped.startswith("#"):
                    desc_lines.append(stripped)
                if len(desc_lines) >= 3:
                    break
            if desc_lines:
                return " ".join(desc_lines)
    return ""


def _parse_outputs(raw_outputs: list[dict]) -> list[CellOutput]:
    """Convierte outputs raw de Jupyter al formato CellOutput."""
    outputs: list[CellOutput] = []

    for raw in raw_outputs:
        output_type = raw.get("output_type", "")

        if output_type == "stream":
            text = "".join(raw.get("text", []))
            if text.strip():
                outputs.append(CellOutput(
                    output_type="text",
                    content=text,
                ))

        elif output_type in ("execute_result", "display_data"):
            data = raw.get("data", {})

            # Prioridad: imagen > HTML > texto
            if "image/png" in data:
                img_data = data["image/png"]
                if isinstance(img_data, list):
                    img_data = "".join(img_data)
                outputs.append(CellOutput(
                    output_type="image",
                    content=f"data:image/png;base64,{img_data.strip()}",
                    attrs={"mime_type": "image/png"},
                ))

            elif "image/svg+xml" in data:
                svg = data["image/svg+xml"]
                if isinstance(svg, list):
                    svg = "".join(svg)
                outputs.append(CellOutput(
                    output_type="image",
                    content=svg,
                    attrs={"mime_type": "image/svg+xml"},
                ))

            elif "text/html" in data:
                html = data["text/html"]
                if isinstance(html, list):
                    html = "".join(html)
                outputs.append(CellOutput(
                    output_type="html",
                    content=html,
                ))

            elif "text/plain" in data:
                text = data["text/plain"]
                if isinstance(text, list):
                    text = "".join(text)
                if text.strip():
                    outputs.append(CellOutput(
                        output_type="text",
                        content=text,
                    ))

        elif output_type == "error":
            traceback = raw.get("traceback", [])
            outputs.append(CellOutput(
                output_type="error",
                content="\n".join(traceback),
                attrs={
                    "ename": raw.get("ename", ""),
                    "evalue": raw.get("evalue", ""),
                },
            ))

    return outputs


def _parse_cell(index: int, raw_cell: dict) -> NotebookCell:
    """Parsea una celda individual del notebook."""
    source = raw_cell.get("source", [])
    if isinstance(source, list):
        source = "".join(source)

    cell_type = raw_cell.get("cell_type", "code")
    outputs = []

    if cell_type == "code":
        outputs = _parse_outputs(raw_cell.get("outputs", []))

    return NotebookCell(
        index=index,
        cell_type=cell_type,
        source=source,
        outputs=outputs,
        execution_count=raw_cell.get("execution_count"),
    )


def parse_notebook(path: Path) -> NotebookDetail:
    """Parsea un archivo .ipynb completo y retorna el Data Contract."""
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    filename = path.name
    nb_id = _generate_id(filename)

    cells = [
        _parse_cell(i, cell)
        for i, cell in enumerate(nb.get("cells", []))
    ]

    return NotebookDetail(
        id=nb_id,
        filename=filename,
        title=_extract_title(nb, filename),
        description=_extract_description(nb),
        cells=cells,
    )


def get_notebook_summary(path: Path) -> NotebookSummary:
    """Genera un resumen ligero sin parsear todos los outputs (para galeria)."""
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    filename = path.name
    cells = nb.get("cells", [])
    code_cells = [c for c in cells if c.get("cell_type") == "code"]
    md_cells = [c for c in cells if c.get("cell_type") == "markdown"]

    has_images = False
    has_dataframes = False
    for cell in code_cells:
        for output in cell.get("outputs", []):
            data = output.get("data", {})
            if "image/png" in data or "image/svg+xml" in data:
                has_images = True
            if "text/html" in data:
                has_dataframes = True
            if has_images and has_dataframes:
                break

    return NotebookSummary(
        id=_generate_id(filename),
        filename=filename,
        title=_extract_title(nb, filename),
        description=_extract_description(nb),
        cell_count=len(cells),
        code_cells=len(code_cells),
        markdown_cells=len(md_cells),
        has_images=has_images,
        has_dataframes=has_dataframes,
    )


def list_notebooks() -> list[NotebookSummary]:
    """Lista todos los notebooks disponibles en el directorio configurado."""
    nb_dir = settings.notebooks_dir
    if not nb_dir.exists():
        return []

    summaries = []
    for path in sorted(nb_dir.glob("*.ipynb")):
        if path.name.startswith("."):
            continue
        try:
            summaries.append(get_notebook_summary(path))
        except (json.JSONDecodeError, KeyError):
            continue

    return summaries


def get_notebook_by_id(notebook_id: str) -> NotebookDetail | None:
    """Busca un notebook por ID y lo parsea completo."""
    nb_dir = settings.notebooks_dir
    if not nb_dir.exists():
        return None

    for path in nb_dir.glob("*.ipynb"):
        if _generate_id(path.name) == notebook_id:
            return parse_notebook(path)

    return None
