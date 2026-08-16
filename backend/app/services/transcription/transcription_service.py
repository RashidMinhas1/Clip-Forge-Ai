import logging
import os
import tempfile
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.services.transcription.audio_extractor import extract_audio
from app.services.transcription.local_whisper import transcribe_local
from app.services.transcription.openai_whisper import transcribe_openai
from app.repositories.transcript import TranscriptRepository
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class TranscriptionService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.repo = TranscriptRepository(db_session)
        
    async def transcribe(self, source_path: str, transcript_id: str):
        logger.info(f"Starting transcription process for transcript_id: {transcript_id}")
        
        await self.repo.update_status(transcript_id, "processing")
        
        temp_dir = tempfile.mkdtemp()
        audio_path = None
        
        try:
            # Extract Audio
            audio_path = extract_audio(source_path, temp_dir)
            
            # Try Local Whisper first, fallback to OpenAI
            try:
                result = transcribe_local(
                    audio_path=audio_path,
                    model_size=settings.WHISPER_MODEL_SIZE,
                    device=settings.WHISPER_DEVICE,
                    compute_type=settings.WHISPER_COMPUTE_TYPE
                )
            except Exception as e:
                logger.warning(f"Local transcription failed, attempting OpenAI fallback: {e}")
                if not settings.OPENAI_API_KEY:
                    raise Exception("Local transcription failed and OpenAI API key not configured")
                
                result = transcribe_openai(
                    audio_path=audio_path,
                    api_key=settings.OPENAI_API_KEY
                )
                
            # Persist results
            segments_data = []
            for seg in result.segments:
                words_data = [
                    {
                        "word_index": idx,
                        "start_time": w.start,
                        "end_time": w.end,
                        "word": w.word,
                        "probability": w.probability
                    }
                    for idx, w in enumerate(seg.words)
                ]
                segments_data.append({
                    "segment_index": seg.id,
                    "start_time": seg.start,
                    "end_time": seg.end,
                    "text": seg.text,
                    "words": words_data
                })
                
            await self.repo.add_segments(transcript_id, segments_data)
            await self.repo.update_status(
                transcript_id, 
                status="completed", 
                language=result.language, 
                duration=result.duration, 
                model_used=result.model_used,
                completed_at=datetime.now(timezone.utc)
            )
            logger.info(f"Transcription completed for transcript_id: {transcript_id}")
            
        except Exception as e:
            logger.error(f"Transcription failed for transcript_id: {transcript_id}: {e}")
            await self.repo.update_status(transcript_id, "failed", error_message=str(e))
            raise
        finally:
            # Cleanup temp files
            if audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except Exception as e:
                    logger.warning(f"Failed to remove temp audio file: {e}")
            if os.path.exists(temp_dir):
                try:
                    os.rmdir(temp_dir)
                except Exception as e:
                    logger.warning(f"Failed to remove temp directory: {e}")
