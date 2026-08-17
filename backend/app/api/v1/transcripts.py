import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.db.models import Source, Project
from app.models.transcript import TranscriptResponse, TranscribeRequest
from app.repositories.transcript import TranscriptRepository
from app.tasks.transcription import task_transcribe_source
from app.api.deps import get_authorized_project

router = APIRouter(tags=["transcripts"])

@router.post("/projects/{project_id}/sources/{source_id}/transcribe", status_code=status.HTTP_202_ACCEPTED)
async def transcribe_source(
    project_id: uuid.UUID,
    source_id: uuid.UUID,
    request: TranscribeRequest = None,
    db: AsyncSession = Depends(get_db),
    project: Project = Depends(get_authorized_project)
):
    # Validate source belongs to project
    stmt = select(Source).where(Source.id == source_id, Source.project_id == project_id)
    result = await db.execute(stmt)
    source = result.scalars().first()
    
    if not source:
        raise HTTPException(status_code=404, detail="Source not found in the given project")
        
    if not source.has_audio:
        raise HTTPException(status_code=400, detail="Source has no audio to transcribe")
        
    if not source.local_storage_reference:
        raise HTTPException(status_code=400, detail="Source media is not available locally")

    repo = TranscriptRepository(db)
    
    # Check for active transcription
    active_transcript = await repo.get_active_by_source(source_id)
    if active_transcript:
        raise HTTPException(status_code=409, detail="Transcription is already in progress or queued for this source")
        
    # Create new transcript record
    transcript = await repo.create(source_id)
    
    # Dispatch Taskiq task
    await task_transcribe_source.kiq(str(transcript.id), source.local_storage_reference)
    
    return {"message": "Transcription queued", "transcript_id": transcript.id}

@router.get("/projects/{project_id}/sources/{source_id}/transcript", response_model=TranscriptResponse)
async def get_transcript(
    project_id: uuid.UUID,
    source_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    project: Project = Depends(get_authorized_project)
):
    # Validate source belongs to project
    stmt = select(Source).where(Source.id == source_id, Source.project_id == project_id)
    result = await db.execute(stmt)
    source = result.scalars().first()
    
    if not source:
        raise HTTPException(status_code=404, detail="Source not found in the given project")
        
    repo = TranscriptRepository(db)
    transcript = await repo.get_by_source(source_id)
    
    if not transcript:
        raise HTTPException(status_code=404, detail="No transcript found for this source")
        
    return transcript
