import uuid
from typing import Optional, List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.models import Transcript, TranscriptSegment, TranscriptWord

class TranscriptRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, source_id: uuid.UUID) -> Transcript:
        transcript = Transcript(source_id=source_id)
        self.session.add(transcript)
        await self.session.commit()
        await self.session.refresh(transcript)
        return transcript

    async def get_by_id(self, transcript_id: uuid.UUID) -> Optional[Transcript]:
        stmt = select(Transcript).options(
            selectinload(Transcript.segments).selectinload(TranscriptSegment.words)
        ).where(Transcript.id == transcript_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_source(self, source_id: uuid.UUID) -> Optional[Transcript]:
        # Returns the latest transcript for a source
        stmt = select(Transcript).options(
            selectinload(Transcript.segments).selectinload(TranscriptSegment.words)
        ).where(Transcript.source_id == source_id).order_by(Transcript.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_active_by_source(self, source_id: uuid.UUID) -> Optional[Transcript]:
        stmt = select(Transcript).where(
            Transcript.source_id == source_id,
            Transcript.status.in_(["queued", "processing"])
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_status(self, transcript_id: uuid.UUID, status: str, **kwargs) -> Optional[Transcript]:
        transcript = await self.session.get(Transcript, transcript_id)
        if transcript:
            transcript.status = status
            for key, value in kwargs.items():
                if hasattr(transcript, key):
                    setattr(transcript, key, value)
            await self.session.commit()
            await self.session.refresh(transcript)
        return transcript

    async def add_segments(self, transcript_id: uuid.UUID, segments_data: List[Dict[str, Any]]):
        for seg_data in segments_data:
            segment = TranscriptSegment(
                transcript_id=transcript_id,
                segment_index=seg_data["segment_index"],
                start_time=seg_data["start_time"],
                end_time=seg_data["end_time"],
                text=seg_data["text"]
            )
            self.session.add(segment)
            await self.session.flush()  # to get segment.id

            for word_data in seg_data.get("words", []):
                word = TranscriptWord(
                    segment_id=segment.id,
                    word_index=word_data["word_index"],
                    start_time=word_data["start_time"],
                    end_time=word_data["end_time"],
                    word=word_data["word"],
                    probability=word_data.get("probability")
                )
                self.session.add(word)
        await self.session.commit()
