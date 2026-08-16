import logging
import uuid
from app.tasks.broker import broker
from app.services.clipping.discovery import ClipDiscoveryService
from app.db.database import AsyncSessionLocal

logger = logging.getLogger(__name__)

@broker.task(task_name="task_discover_clips")
async def task_discover_clips(run_id: str, project_id: str, source_id: str):
    logger.info(f"Task task_discover_clips started for run {run_id}")
    
    async with AsyncSessionLocal() as session:
        service = ClipDiscoveryService(session)
        try:
            await service.discover_clips(uuid.UUID(run_id), uuid.UUID(project_id), uuid.UUID(source_id))
        except Exception as e:
            logger.error(f"Task failed for run {run_id}: {e}")
            raise
