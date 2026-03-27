import uuid

import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from app.core.config import settings
from app.models.schemas import (
    ProcessResponse,
    TaskStatus,
    TaskStatusResponse,
)
from app.services.cleaning import run_cleaning_pipeline
from app.services.profiling import generate_health_summary
from app.services.storage import (
    get_dlq_path,
    get_output_path,
    get_task,
    save_task,
)

router = APIRouter(prefix="/v1/profiling", tags=["profiling"])


@router.post("/process", response_model=ProcessResponse)
def process_file(file: UploadFile = File(...)):
    """Endpoint principal: carga CSV, ejecuta profiling + limpieza y devuelve resultados.

    Se define como función síncrona (def) para que FastAPI la delegue
    automáticamente a un thread pool, evitando bloquear el event loop
    con operaciones CPU-bound de Pandas.
    """
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos .csv")

    task_id = uuid.uuid4().hex[:12]

    try:
        df = pd.read_csv(file.file, low_memory=False)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error al leer el CSV: {e}")

    if df.empty:
        raise HTTPException(status_code=422, detail="El archivo CSV está vacío")

    # WAP - Write: captura inmutable del estado original
    health_before = generate_health_summary(df)

    # WAP - Audit: motor de limpieza
    df_clean, df_dlq, cleaning_summary = run_cleaning_pipeline(df)

    # WAP - Publish: consolidar en zona de descarga
    output_path = get_output_path(task_id)
    df_clean.to_csv(output_path, index=False)

    if len(df_dlq) > 0:
        dlq_path = get_dlq_path(task_id)
        df_dlq.to_csv(dlq_path, index=False)

    download_url = f"/v1/profiling/download/{task_id}"

    return ProcessResponse(
        task_id=task_id,
        status=TaskStatus.completed,
        health_summary=health_before,
        cleaning_summary=cleaning_summary,
        download_url=download_url,
    )


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_status(task_id: str):
    """Consulta el estado de una tarea."""
    # Primero verificar si el archivo existe (procesamiento síncrono ya terminado)
    output_path = get_output_path(task_id)
    if output_path.exists():
        return TaskStatusResponse(
            task_id=task_id,
            status=TaskStatus.completed,
            download_url=f"/v1/profiling/download/{task_id}",
        )

    # Fallback a Redis para tareas async
    task_data = await get_task(task_id)
    if task_data is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    return TaskStatusResponse(**task_data)


@router.get("/download/{task_id}")
async def download_file(task_id: str):
    """Descarga el archivo CSV limpio."""
    output_path = get_output_path(task_id)
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado o expirado")

    return FileResponse(
        path=str(output_path),
        media_type="text/csv",
        filename=f"cleaned_{task_id}.csv",
    )


@router.get("/download/{task_id}/dlq")
async def download_dlq(task_id: str):
    """Descarga los registros enviados a la Dead Letter Queue."""
    dlq_path = get_dlq_path(task_id)
    if not dlq_path.exists():
        raise HTTPException(status_code=404, detail="No hay registros DLQ para esta tarea")

    return FileResponse(
        path=str(dlq_path),
        media_type="text/csv",
        filename=f"dlq_{task_id}.csv",
    )
