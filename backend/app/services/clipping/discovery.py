import json
import logging
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.models import Transcript, TranscriptWord, ClipDiscoveryRun, Project
from app.models.clipping import AIClipCandidateList, ClipCandidateCreate
from app.services.ai.router import AIRouter
from app.services.ai.models import AIRequest
from app.repositories.clipping import ClippingRepository

logger = logging.getLogger(__name__)

class ClipDiscoveryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.clipping_repo = ClippingRepository(session)
        self.ai_router = AIRouter()

    async def discover_clips(self, run_id: UUID, project_id: UUID, source_id: UUID) -> None:
        try:
            # 1. Update status to processing
            await self.clipping_repo.update_run_status(run_id, "processing")
            
            # 2. Fetch transcript and words
            stmt = select(Transcript).where(Transcript.source_id == source_id).order_by(Transcript.created_at.desc())
            result = await self.session.execute(stmt)
            transcript = result.scalars().first()
            
            if not transcript or transcript.status != "completed":
                raise ValueError("Source does not have a completed transcript.")

            stmt = select(TranscriptWord).join(TranscriptWord.segment).where(
                TranscriptWord.segment.has(transcript_id=transcript.id)
            ).order_by(TranscriptWord.start_time)
            
            words_result = await self.session.execute(stmt)
            words = list(words_result.scalars().all())
            
            if not words:
                raise ValueError("Transcript has no words.")

            transcript_text = " ".join([w.word for w in words])

            # 3. Request AI Analysis
            prompt = f"""
You are an expert video editor. Analyze the following transcript and find the 3 most engaging, standalone clips.
Return a JSON object matching this schema: {AIClipCandidateList.schema_json()}
Ensure the start_word, end_word, and excerpt exactly match the transcript.

Transcript:
{transcript_text}
"""
            req = AIRequest(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o",  # Default, router will override
                max_tokens=4000
            )

            # Using generate_structured for schema
            # AIClipCandidateList is the schema type
            ai_response = await self.ai_router.generate_structured(req, AIClipCandidateList)
            
            # 4. Parse response
            try:
                # Some models return json markdown blocks
                content = ai_response.content.strip()
                if content.startswith("```json"):
                    content = content[7:-3].strip()
                elif content.startswith("```"):
                    content = content[3:-3].strip()
                
                parsed = AIClipCandidateList.parse_raw(content)
            except Exception as e:
                logger.error(f"Failed to parse AI response: {ai_response.content}")
                raise ValueError(f"AI returned invalid format: {e}")

            # 5. Timestamp mapping
            candidates_data = []
            for ai_cand in parsed.candidates:
                # Find start time
                start_time = None
                for w in words:
                    if w.word.strip('.,!?').lower() == ai_cand.start_word.strip('.,!?').lower():
                        start_time = w.start_time
                        break
                
                # Find end time
                end_time = None
                for w in reversed(words):
                    if w.word.strip('.,!?').lower() == ai_cand.end_word.strip('.,!?').lower():
                        end_time = w.end_time
                        break
                
                if start_time is None or end_time is None:
                    continue
                if start_time >= end_time:
                    continue
                    
                candidates_data.append(ClipCandidateCreate(
                    run_id=run_id,
                    project_id=project_id,
                    title=ai_cand.title,
                    hook=ai_cand.hook,
                    reason=ai_cand.reason,
                    start_time=start_time,
                    end_time=end_time,
                    duration=end_time - start_time,
                    score=ai_cand.score,
                    confidence=ai_cand.confidence,
                    transcript_excerpt=ai_cand.excerpt
                ))
            
            if not candidates_data:
                raise ValueError("No valid candidates found with matching bounds.")

            await self.clipping_repo.create_candidates(candidates_data)
            await self.clipping_repo.update_run_status(run_id, "completed")
            
        except Exception as e:
            logger.error(f"Discovery run {run_id} failed: {e}")
            await self.clipping_repo.update_run_status(run_id, "failed", str(e))

