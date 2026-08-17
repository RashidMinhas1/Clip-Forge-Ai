import math
import json
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.models import ClipCandidate, Transcript, TranscriptSegment, TranscriptWord, ClipDiscoveryRun

class ExportService:
    @staticmethod
    def _format_timestamp_srt(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        msecs = int(round((seconds - int(seconds)) * 1000))
        if msecs == 1000:
            secs += 1
            msecs = 0
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{msecs:03d}"

    @staticmethod
    def _format_timestamp_vtt(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        msecs = int(round((seconds - int(seconds)) * 1000))
        if msecs == 1000:
            secs += 1
            msecs = 0
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{msecs:03d}"

    async def get_clip_words(self, db: AsyncSession, clip: ClipCandidate) -> List[TranscriptWord]:
        # Get the source ID via the run
        stmt = select(ClipDiscoveryRun).where(ClipDiscoveryRun.id == clip.run_id)
        result = await db.execute(stmt)
        run = result.scalars().first()
        if not run:
            return []

        # Get the transcript for the source
        stmt = select(Transcript).where(
            Transcript.source_id == run.source_id,
            Transcript.status == "completed"
        ).order_by(Transcript.created_at.desc())
        result = await db.execute(stmt)
        transcript = result.scalars().first()
        if not transcript:
            return []

        # Get words within the clip boundary
        # Since words are associated with segments, we first get segments overlapping the clip
        stmt = select(TranscriptSegment).where(
            TranscriptSegment.transcript_id == transcript.id,
            TranscriptSegment.start_time <= clip.end_time,
            TranscriptSegment.end_time >= clip.start_time
        ).options(selectinload(TranscriptSegment.words))
        result = await db.execute(stmt)
        segments = result.scalars().all()

        words = []
        for segment in sorted(segments, key=lambda s: s.segment_index):
            for word in sorted(segment.words, key=lambda w: w.word_index):
                # Include words that at least partially overlap with the clip
                if word.start_time <= clip.end_time and word.end_time >= clip.start_time:
                    words.append(word)

        return words

    async def generate_subtitles(self, db: AsyncSession, clip: ClipCandidate, fmt: str) -> str:
        words = await self.get_clip_words(db, clip)
        if not words:
            return ""

        # Adjust start time to be relative to the clip's start
        # E.g. if clip starts at 10.0 and word starts at 11.5, word is now at 1.5
        adjusted_words = []
        for w in words:
            start = max(0.0, w.start_time - clip.start_time)
            end = min(clip.duration, w.end_time - clip.start_time)
            adjusted_words.append({
                "word": w.word,
                "start": start,
                "end": end
            })

        if fmt == "srt":
            return self._generate_srt(adjusted_words)
        elif fmt == "vtt":
            return self._generate_vtt(adjusted_words)
        elif fmt == "txt":
            return self._generate_txt(adjusted_words)
        elif fmt == "json":
            return self._generate_json(adjusted_words)
        else:
            raise ValueError(f"Unsupported format: {fmt}")

    def _generate_srt(self, words: List[dict]) -> str:
        # Group words into chunks of ~5 words or ~2 seconds
        chunks = self._chunk_words(words)
        lines = []
        for i, chunk in enumerate(chunks, 1):
            start = chunk[0]["start"]
            end = chunk[-1]["end"]
            text = " ".join(w["word"].strip() for w in chunk)
            lines.append(f"{i}")
            lines.append(f"{self._format_timestamp_srt(start)} --> {self._format_timestamp_srt(end)}")
            lines.append(text)
            lines.append("")
        return "\n".join(lines)

    def _generate_vtt(self, words: List[dict]) -> str:
        chunks = self._chunk_words(words)
        lines = ["WEBVTT", ""]
        for i, chunk in enumerate(chunks, 1):
            start = chunk[0]["start"]
            end = chunk[-1]["end"]
            text = " ".join(w["word"].strip() for w in chunk)
            lines.append(f"{i}")
            lines.append(f"{self._format_timestamp_vtt(start)} --> {self._format_timestamp_vtt(end)}")
            lines.append(text)
            lines.append("")
        return "\n".join(lines)

    def _generate_txt(self, words: List[dict]) -> str:
        return " ".join(w["word"].strip() for w in words)

    def _generate_json(self, words: List[dict]) -> str:
        return json.dumps({"words": words}, indent=2)

    def _chunk_words(self, words: List[dict], max_words: int = 6) -> List[List[dict]]:
        chunks = []
        current_chunk = []
        for w in words:
            current_chunk.append(w)
            if len(current_chunk) >= max_words:
                chunks.append(current_chunk)
                current_chunk = []
        if current_chunk:
            chunks.append(current_chunk)
        return chunks
