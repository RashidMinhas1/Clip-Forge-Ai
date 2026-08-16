import logging
from typing import List
from openai import OpenAI
from app.services.transcription.local_whisper import TranscriptionResult, SegmentResult, WordResult

logger = logging.getLogger(__name__)

class OpenAITranscriptionError(Exception):
    pass

def transcribe_openai(audio_path: str, api_key: str) -> TranscriptionResult:
    """
    Transcribes audio using OpenAI Whisper API.
    """
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not configured.")
        
    logger.info(f"Transcribing with OpenAI Whisper API")
    try:
        client = OpenAI(api_key=api_key)
        
        with open(audio_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["word", "segment"]
            )
            
        segment_results = []
        # Process words to match them to segments if possible or just map words directly if segment contains them
        
        # OpenAI verbose_json with word/segment granularity returns lists of segments and words.
        response_dict = response.model_dump()
        segments_data = response_dict.get("segments", [])
        words_data = response_dict.get("words", [])
        
        for idx, segment in enumerate(segments_data):
            seg_start = segment.get("start", 0.0)
            seg_end = segment.get("end", 0.0)
            
            # Find words that fall into this segment
            segment_words = []
            for w in words_data:
                # Basic overlap/inclusion check
                if w.get("start", 0.0) >= seg_start and w.get("end", 0.0) <= seg_end + 0.1:
                    segment_words.append(WordResult(
                        word=w.get("word", ""),
                        start=w.get("start", 0.0),
                        end=w.get("end", 0.0),
                        probability=1.0  # OpenAI doesn't return probability currently in standard verbose_json
                    ))
            
            segment_results.append(SegmentResult(
                id=idx,
                start=seg_start,
                end=seg_end,
                text=segment.get("text", ""),
                words=segment_words
            ))
            
        return TranscriptionResult(
            language=response_dict.get("language", "unknown"),
            duration=response_dict.get("duration", 0.0),
            segments=segment_results,
            model_used="openai-whisper-1"
        )
        
    except Exception as e:
        logger.error(f"OpenAI transcription failed: {e}")
        raise OpenAITranscriptionError(f"OpenAI transcription error: {e}")
