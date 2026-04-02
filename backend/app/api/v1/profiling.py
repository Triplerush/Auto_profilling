import shutil

from fastapi import APIRouter, HTTPException, UploadFile, File

from app.core.config import settings
from app.models.schemas import (
    NotebookDetail,
    NotebookListResponse,
    UploadResponse,
)
from app.services.notebook_parser import (
    get_notebook_by_id,
    list_notebooks,
)

router = APIRouter(prefix="/v1/notebooks", tags=["notebooks"])


@router.get("", response_model=NotebookListResponse)
def get_notebooks():
    """Lista todos los notebooks disponibles en el directorio."""
    notebooks = list_notebooks()
    return NotebookListResponse(notebooks=notebooks, total=len(notebooks))


@router.get("/{notebook_id}", response_model=NotebookDetail)
def get_notebook(notebook_id: str):
    """Retorna el contenido completo parseado de un notebook."""
    detail = get_notebook_by_id(notebook_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Notebook no encontrado")
    return detail


@router.post("/upload", response_model=UploadResponse)
async def upload_notebook(file: UploadFile = File(...)):
    """Sube un notebook .ipynb al directorio de notebooks."""
    if not file.filename or not file.filename.endswith(".ipynb"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos .ipynb")

    nb_dir = settings.notebooks_dir
    nb_dir.mkdir(parents=True, exist_ok=True)

    dest = nb_dir / file.filename
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Validar que sea un JSON valido de Jupyter
    import json
    try:
        with open(dest, "r", encoding="utf-8") as f:
            nb = json.load(f)
        if "cells" not in nb:
            dest.unlink()
            raise HTTPException(status_code=422, detail="El archivo no es un notebook Jupyter valido")
    except json.JSONDecodeError:
        dest.unlink()
        raise HTTPException(status_code=422, detail="El archivo no contiene JSON valido")

    from app.services.notebook_parser import _generate_id
    nb_id = _generate_id(file.filename)

    return UploadResponse(
        id=nb_id,
        filename=file.filename,
        message="Notebook subido exitosamente",
    )
