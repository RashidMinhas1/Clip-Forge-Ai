import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.db.models import ClipCandidate, Project
from app.models.captions import ClipCaptionsResponse, CaptionConfigUpdate, CaptionConfigResponse
from app.services.captions import get_clip_captions, update_caption_config
from app.api.deps import get_authorized_project

router = APIRouter(prefix="/projects", tags=["Captions"])

async def get_clip_for_project(db: AsyncSession, project_id: uuid.UUID, clip_id: uuid.UUID) -> ClipCandidate:
    stmt = select(ClipCandidate).where(ClipCandidate.id == clip_id, ClipCandidate.project_id == project_id)
    result = await db.execute(stmt)
    clip = result.scalars().first()
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")
    return clip

@router.get("/{project_id}/clips/{clip_id}/captions", response_model=ClipCaptionsResponse)
async def get_captions(
    project_id: uuid.UUID,
    clip_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    project: Project = Depends(get_authorized_project)
):
    try:
        clip = await get_clip_for_project(db, project_id, clip_id)
        chunks, config = await get_clip_captions(db, clip)
        return ClipCaptionsResponse(chunks=chunks, config=config)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{project_id}/clips/{clip_id}/caption-config", response_model=CaptionConfigResponse)
async def patch_caption_config(
    project_id: uuid.UUID,
    clip_id: uuid.UUID,
    update_data: CaptionConfigUpdate,
    db: AsyncSession = Depends(get_db),
    project: Project = Depends(get_authorized_project)
):
    try:
        clip = await get_clip_for_project(db, project_id, clip_id)
        config = await update_caption_config(db, clip, update_data)
        return config
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
