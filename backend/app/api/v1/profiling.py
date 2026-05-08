from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    NotebookDetail,
    NotebookListResponse,
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
