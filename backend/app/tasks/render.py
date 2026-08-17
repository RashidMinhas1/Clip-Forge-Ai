from uuid import UUID
from datetime import datetime, timezone
import asyncio
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.tasks.broker import broker
from app.db.database import AsyncSessionLocal
from app.db.models import RenderJob, ClipCandidate, Source, ClipDiscoveryRun
from app.services.render import RenderService
from app.services.captions import get_clip_captions

@broker.task(task_name="render_clip")
async def task_render_clip(job_id: str) -> None:
    job_uuid = UUID(job_id)
    render_service = RenderService()
    
    async with AsyncSessionLocal() as session:
        stmt = select(RenderJob).where(RenderJob.id == job_uuid)
        result = await session.execute(stmt)
        job = result.scalars().first()
        
        if not job:
            return
            
        job.status = "processing"
        job.progress = 10.0
        await session.commit()
        
        try:
            # Fetch clip with relation
            stmt = (
                select(ClipCandidate)
                .where(ClipCandidate.id == job.clip_id)
                .options(selectinload(ClipCandidate.run).selectinload(ClipDiscoveryRun.source))
            )
            result = await session.execute(stmt)
            clip = result.scalars().first()
            
            if not clip:
                raise ValueError(f"Clip {job.clip_id} not found")
                
            source = clip.run.source
            if not source:
                raise ValueError("Source not found for clip")

            chunks, caption_config = await get_clip_captions(session, clip)
            
            # Generate output path
            output_path = render_service.storage_service.generate_source_path(extension=".mp4")
            
            # Build command
            cmd, srt_path = render_service.build_ffmpeg_command(
                source=source,
                clip=clip,
                caption_config=caption_config,
                caption_chunks=chunks,
                output_path=output_path
            )
            
            # Update progress before executing
            job.progress = 30.0
            await session.commit()

            # Execute
            success = await asyncio.to_thread(render_service.execute_render, cmd, srt_path)
            
            if success:
                job.status = "completed"
                job.progress = 100.0
                job.output_path = output_path
            else:
                job.status = "failed"
                job.error_message = "FFmpeg execution failed"
                
            job.completed_at = datetime.now(timezone.utc)
            await session.commit()

        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.now(timezone.utc)
            await session.commit()
