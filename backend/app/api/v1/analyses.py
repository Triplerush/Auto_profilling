import json

from fastapi import APIRouter, HTTPException, UploadFile, File

from app.models.analysis_schemas import (
    AnalysisDetail,
    AnalysisListResponse,
    AnalysisUploadResponse,
)
from app.services.analysis_reader import (
    get_analysis_by_id,
    list_analyses,
    save_analysis,
)

router = APIRouter(prefix="/v1/analyses", tags=["analyses"])


@router.get("", response_model=AnalysisListResponse)
def get_analyses():
    """Lista todos los analisis disponibles."""
    analyses = list_analyses()
    return AnalysisListResponse(analyses=analyses, total=len(analyses))


@router.get("/{analysis_id}", response_model=AnalysisDetail)
def get_analysis(analysis_id: str):
    """Retorna el Data Contract completo de un analisis."""
    detail = get_analysis_by_id(analysis_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Analisis no encontrado")
    return detail


@router.post("/upload", response_model=AnalysisUploadResponse)
async def upload_analysis(file: UploadFile = File(...)):
    """Sube un Data Contract JSON validado."""
    if not file.filename or not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos .json")

    try:
        content = await file.read()
        raw = json.loads(content)
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(status_code=422, detail="El archivo no contiene JSON valido")

    try:
        detail = AnalysisDetail.model_validate(raw)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Data Contract invalido: {e}")

    save_analysis(detail)
    return AnalysisUploadResponse(
        id=detail.metadata.id,
        title=detail.metadata.title,
        message="Analisis subido exitosamente",
    )
