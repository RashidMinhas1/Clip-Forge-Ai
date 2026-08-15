from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import Any

from ...models.source import SourceMetadata, YouTubeIngestionRequest
from ...services.source.storage import StorageService
from ...services.source.validator import ValidatorService
from ...services.source.media_probe import MediaProbeService
from ...services.source.youtube import YouTubeSourceProvider
from ...services.source.ingestion import SourceIngestionService

router = APIRouter(prefix="/sources", tags=["Sources"])

# Dependency injection
def get_ingestion_service() -> SourceIngestionService:
    storage = StorageService()
    validator = ValidatorService()
    probe = MediaProbeService()
    youtube = YouTubeSourceProvider()
    return SourceIngestionService(
        storage_service=storage,
        validator_service=validator,
        media_probe_service=probe,
        youtube_provider=youtube
    )

@router.post("/local", response_model=SourceMetadata)
async def ingest_local(
    file: UploadFile = File(...),
    service: SourceIngestionService = Depends(get_ingestion_service)
) -> Any:
    """
    Ingests a local video file.
    Validates limits and performs media probing synchronously.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename not provided")
        
    result = service.ingest_local_file(
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
    service: SourceIngestionService = Depends(get_ingestion_service)
) -> Any:
    """
    Ingests a YouTube URL.
    Downloads and probes media synchronously.
    """
    result = service.ingest_youtube_url(url=request.url)
    
    if result.ingestion_status == "failed":
        raise HTTPException(status_code=400, detail=result.model_dump(mode="json"))
        
    return result
