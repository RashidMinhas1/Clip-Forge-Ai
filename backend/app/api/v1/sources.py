from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from typing import Any
import uuid

from ...models.source import SourceMetadata, YouTubeIngestionRequest
from ...services.source.storage import StorageService
from ...services.source.validator import ValidatorService
from ...services.source.media_probe import MediaProbeService
from ...services.source.youtube import YouTubeSourceProvider
from ...services.source.ingestion import SourceIngestionService
from ...repositories.source import SourceRepository
from ...db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_authorized_project, get_current_user
from app.db.models import Project, User

router = APIRouter(prefix="/sources", tags=["Sources"])

# Dependency injection
def get_ingestion_service(db: AsyncSession = Depends(get_db)) -> SourceIngestionService:
    storage = StorageService()
    validator = ValidatorService()
    probe = MediaProbeService()
    youtube = YouTubeSourceProvider()
    source_repository = SourceRepository(db)
    return SourceIngestionService(
        storage_service=storage,
        validator_service=validator,
        media_probe_service=probe,
        youtube_provider=youtube,
        source_repository=source_repository
    )

@router.post("/local", response_model=SourceMetadata)
async def ingest_local(
    project_id: uuid.UUID = Form(...),
    file: UploadFile = File(...),
    service: SourceIngestionService = Depends(get_ingestion_service),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Ingests a local video file.
    Validates limits and performs media probing synchronously, then persists asynchronously.
    """
    await get_authorized_project(str(project_id), db, current_user)
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename not provided")
        
    result = await service.ingest_local_file(
        project_id=project_id,
        filename=file.filename,
        file_stream=file.file,
        size_bytes=file.size or 0
    )
    
    if result.ingestion_status == "failed":
        raise HTTPException(status_code=400, detail=result.model_dump(mode="json"))
        
    return result

@router.post("/youtube", response_model=SourceMetadata)
async def ingest_youtube(
    request: YouTubeIngestionRequest,
    service: SourceIngestionService = Depends(get_ingestion_service),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Ingests a YouTube URL.
    Downloads and probes media synchronously, then persists asynchronously.
    """
    await get_authorized_project(str(request.project_id), db, current_user)
    
    result = await service.ingest_youtube_url(project_id=request.project_id, url=request.url)
    
    if result.ingestion_status == "failed":
        raise HTTPException(status_code=400, detail=result.model_dump(mode="json"))
        
    return result
