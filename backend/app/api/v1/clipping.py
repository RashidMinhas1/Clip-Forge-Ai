import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.repositories.clipping import ClippingRepository
from app.models.clipping import ClipCandidateResponse, ClipDiscoveryRunResponse, ClipCandidateUpdate
from app.tasks.clipping import task_discover_clips

router = APIRouter(prefix="/projects", tags=["Clipping"])

def get_clipping_repo(db: AsyncSession = Depends(get_db)) -> ClippingRepository:
    return ClippingRepository(db)

@router.post("/{project_id}/sources/{source_id}/clip-discovery", response_model=ClipDiscoveryRunResponse, status_code=202)
async def create_clip_discovery(
    project_id: uuid.UUID,
    source_id: uuid.UUID,
    repo: ClippingRepository = Depends(get_clipping_repo)
):
    try:
        run = await repo.create_run(project_id, source_id)
        # Kick off background task
        await task_discover_clips.kiq(str(run.id), str(project_id), str(source_id))
        return run
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}/sources/{source_id}/clip-discovery/{run_id}", response_model=ClipDiscoveryRunResponse)
async def get_clip_discovery_status(
    project_id: uuid.UUID,
    source_id: uuid.UUID,
    run_id: uuid.UUID,
    repo: ClippingRepository = Depends(get_clipping_repo)
):
    try:
        run = await repo.get_run(run_id, project_id)
        if not run:
            raise HTTPException(status_code=404, detail="Discovery run not found")
        # Validate source_id matches
        if run.source_id != source_id:
            raise HTTPException(status_code=400, detail="Run does not belong to this source")
        return run
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}/clip-candidates", response_model=List[ClipCandidateResponse])
async def list_clip_candidates(
    project_id: uuid.UUID,
    repo: ClippingRepository = Depends(get_clipping_repo)
):
    try:
        candidates = await repo.get_candidates_for_project(project_id)
        return candidates
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{project_id}/candidates/{candidate_id}/status", response_model=ClipCandidateResponse)
async def update_clip_candidate_status(
    project_id: uuid.UUID,
    candidate_id: uuid.UUID,
    update_data: ClipCandidateUpdate,
    repo: ClippingRepository = Depends(get_clipping_repo)
):
    if update_data.status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'approved' or 'rejected'")
    try:
        candidate = await repo.update_candidate_status(candidate_id, project_id, update_data.status)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        return candidate
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
