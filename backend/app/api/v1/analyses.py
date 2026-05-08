from fastapi import APIRouter, HTTPException

from app.models.analysis_schemas import (
    AnalysisDetail,
    AnalysisListResponse,
)
from app.services.analysis_reader import (
    get_analysis_by_id,
    list_analyses,
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
