import re
from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc
from app.db.models import Transcript, TranscriptSegment, TranscriptWord, ClipCandidate, ClipCaptionConfig
from app.models.captions import CaptionChunk, CaptionWord, CaptionConfigUpdate

async def get_or_create_caption_config(session: AsyncSession, clip: ClipCandidate) -> ClipCaptionConfig:
    stmt = select(ClipCaptionConfig).where(ClipCaptionConfig.clip_id == clip.id)
    result = await session.execute(stmt)
    config = result.scalars().first()
    
    if not config:
        config = ClipCaptionConfig(clip_id=clip.id)
        session.add(config)
        await session.commit()
        await session.refresh(config)
        
    return config

async def update_caption_config(session: AsyncSession, clip: ClipCandidate, update_data: CaptionConfigUpdate) -> ClipCaptionConfig:
    config = await get_or_create_caption_config(session, clip)
    
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(config, key, value)
        
    await session.commit()
    await session.refresh(config)
    return config

def _is_rtl(text: str) -> bool:
    """Basic detection of Arabic/Persian/Urdu Unicode blocks."""
    rtl_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
    return bool(rtl_pattern.search(text))

async def generate_caption_chunks(session: AsyncSession, clip: ClipCandidate) -> Tuple[List[CaptionChunk], bool]:
    # Query words that overlap with the clip duration
    stmt = (
        select(TranscriptWord)
        .join(TranscriptSegment)
        .join(Transcript)
        .where(
            Transcript.source_id == clip.source_id,
            TranscriptWord.end_time >= clip.start_time - 0.5,
            TranscriptWord.start_time <= clip.end_time + 0.5
        )
        .order_by(asc(TranscriptWord.start_time))
    )
    result = await session.execute(stmt)
    words = result.scalars().all()

    chunks: List[CaptionChunk] = []
    current_chunk_words: List[CaptionWord] = []
    current_text = ""
    chunk_start = 0.0
    
    has_rtl = False
    WORDS_PER_CHUNK = 6
    
    for word in words:
        # Calculate clip-relative timestamps
        rel_start = max(0.0, word.start_time - clip.start_time)
        rel_end = max(0.0, min(word.end_time - clip.start_time, clip.duration))
        
        # Skip if word is completely outside the clip bounds
        if rel_end <= 0 or rel_start >= clip.duration:
            continue
            
        if _is_rtl(word.word):
            has_rtl = True

        if not current_chunk_words:
            chunk_start = rel_start

        current_chunk_words.append(CaptionWord(
            word=word.word,
            start_time=rel_start,
            end_time=rel_end
        ))
        current_text += (" " if current_text else "") + word.word
        
        # Break chunk on punctuation or word count limit
        if len(current_chunk_words) >= WORDS_PER_CHUNK or word.word.endswith(('.', '?', '!', ',', '。', '؟')):
            chunks.append(CaptionChunk(
                text=current_text,
                start_time=chunk_start,
                end_time=rel_end,
                words=current_chunk_words
            ))
            current_chunk_words = []
            current_text = ""
            
    if current_chunk_words:
        chunks.append(CaptionChunk(
            text=current_text,
            start_time=chunk_start,
            end_time=current_chunk_words[-1].end_time,
            words=current_chunk_words
        ))
        
    return chunks, has_rtl

async def get_clip_captions(session: AsyncSession, clip: ClipCandidate) -> Tuple[List[CaptionChunk], ClipCaptionConfig]:
    chunks, has_rtl = await generate_caption_chunks(session, clip)
    config = await get_or_create_caption_config(session, clip)
    
    if has_rtl and not config.is_rtl:
        config.is_rtl = True
        await session.commit()
        await session.refresh(config)
        
    return chunks, config
