import logging
import uuid
from app.tasks.broker import broker
from app.services.transcription.transcription_service import TranscriptionService
from app.db.database import AsyncSessionLocal
from app.db.models import Source

logger = logging.getLogger(__name__)

@broker.task(task_name="task_transcribe_source")
async def task_transcribe_source(transcript_id: str, source_path: str):
    logger.info(f"Task task_transcribe_source started for transcript {transcript_id}")
    
    async with AsyncSessionLocal() as session:
        service = TranscriptionService(session)
        try:
            await service.transcribe(source_path, uuid.UUID(transcript_id))
        except Exception as e:
            logger.error(f"Task failed for transcript {transcript_id}: {e}")
            raise
