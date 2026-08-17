import os
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.db.models import RenderJob, ClipCandidate, Project, User
from app.models.render import RenderJobResponse
from app.services.export import ExportService
from app.api.deps import get_authorized_project, get_current_user

router = APIRouter(prefix="", tags=["Exports"])

@router.get("/projects/{project_id}/exports", response_model=List[RenderJobResponse])
async def list_exports(
    project_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    project: Project = Depends(get_authorized_project)
):
    # Fetch completed and failed render jobs
    stmt = select(RenderJob).where(
        RenderJob.project_id == project_id,
        RenderJob.status.in_(["completed", "failed"])
    ).order_by(RenderJob.created_at.desc())
    
    result = await session.execute(stmt)
    jobs = result.scalars().all()
    return jobs

@router.get("/exports/{job_id}/download/video")
async def download_video(
    job_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(RenderJob).where(RenderJob.id == job_id)
    result = await session.execute(stmt)
    job = result.scalars().first()

    if not job:
        raise HTTPException(status_code=404, detail="Export not found")
        
    stmt = select(Project).where(Project.id == job.project_id)
    result = await session.execute(stmt)
    project = result.scalars().first()
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Export is not completed")
    if not job.output_path or not os.path.exists(job.output_path):
        raise HTTPException(status_code=404, detail="Video file not found")

    # The file path is already secured by the backend render task, 
    # and job.output_path is generated server-side.
    return FileResponse(
        path=job.output_path,
        media_type="video/mp4",
        filename=f"clipforge_export_{job_id}.mp4"
    )

@router.get("/exports/{job_id}/download/captions")
async def download_captions(
    job_id: uuid.UUID,
    format: str = "srt",
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(RenderJob).where(RenderJob.id == job_id)
    result = await session.execute(stmt)
    job = result.scalars().first()

    if not job:
        raise HTTPException(status_code=404, detail="Export not found")
        
    stmt = select(Project).where(Project.id == job.project_id)
    result = await session.execute(stmt)
    project = result.scalars().first()
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    stmt = select(ClipCandidate).where(ClipCandidate.id == job.clip_id)
    result = await session.execute(stmt)
    clip = result.scalars().first()
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")

    export_service = ExportService()
    try:
        content = await export_service.generate_subtitles(session, clip, format.lower())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not content:
        raise HTTPException(status_code=404, detail="No captions found for this clip")

    media_types = {
        "srt": "application/x-subrip",
        "vtt": "text/vtt",
        "txt": "text/plain",
        "json": "application/json"
    }

    return Response(
        content=content,
        media_type=media_types.get(format.lower(), "text/plain"),
        headers={"Content-Disposition": f'attachment; filename="captions_{job_id}.{format.lower()}"'}
    )
