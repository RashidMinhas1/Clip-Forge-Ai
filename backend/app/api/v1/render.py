from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.db.models import RenderJob, ClipCandidate, Project
from app.models.render import RenderJobCreate, RenderJobResponse
from app.tasks.render import task_render_clip
from app.api.deps import get_current_user
from app.db.models import User

router = APIRouter(prefix="/renders", tags=["Renders"])

@router.post("/{clip_id}", response_model=RenderJobResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_render_job(
    clip_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify clip exists
    stmt = select(ClipCandidate).where(ClipCandidate.id == clip_id)
    result = await session.execute(stmt)
    clip = result.scalars().first()
    
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")

    # Verify project ownership
    stmt = select(Project).where(Project.id == clip.project_id)
    result = await session.execute(stmt)
    project = result.scalars().first()
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    job = RenderJob(
        clip_id=clip.id,
        project_id=clip.project_id,
        status="queued",
        progress=0.0
    )
    session.add(job)
    await session.commit()
    await session.refresh(job)

    # Queue background task
    await task_render_clip.kiq(str(job.id))

    return job

@router.get("/{job_id}", response_model=RenderJobResponse)
async def get_render_job(
    job_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(RenderJob).where(RenderJob.id == job_id)
    result = await session.execute(stmt)
    job = result.scalars().first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Render job not found")

    # Verify project ownership
    stmt = select(Project).where(Project.id == job.project_id)
    result = await session.execute(stmt)
    project = result.scalars().first()
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    return job

@router.post("/{job_id}/retry", response_model=RenderJobResponse, status_code=status.HTTP_202_ACCEPTED)
async def retry_render_job(
    job_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(RenderJob).where(RenderJob.id == job_id)
    result = await session.execute(stmt)
    job = result.scalars().first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Render job not found")

    # Verify project ownership
    stmt = select(Project).where(Project.id == job.project_id)
    result = await session.execute(stmt)
    project = result.scalars().first()
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    if job.status not in ["failed", "cancelled", "completed"]:
        raise HTTPException(status_code=400, detail="Can only retry failed, cancelled, or completed jobs")

    # Reset job state
    job.status = "queued"
    job.progress = 0.0
    job.error_message = None
    job.completed_at = None
    job.output_path = None
    
    await session.commit()
    await session.refresh(job)

    # Re-queue background task
    await task_render_clip.kiq(str(job.id))

    return job
