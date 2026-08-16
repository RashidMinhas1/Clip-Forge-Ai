from dataclasses import dataclass
from typing import List, Optional
import logging
from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)

@dataclass
class WordResult:
    word: str
    start: float
    end: float
    probability: float

@dataclass
class SegmentResult:
    id: int
    start: float
    end: float
    text: str
    words: List[WordResult]

@dataclass
class TranscriptionResult:
    language: str
    duration: float
    segments: List[SegmentResult]
    model_used: str

class LocalTranscriptionError(Exception):
    pass

def transcribe_local(audio_path: str, model_size: str, device: str, compute_type: str) -> TranscriptionResult:
    """
    Transcribes audio using local faster-whisper model.
    """
    logger.info(f"Transcribing locally with model: {model_size}, device: {device}, compute_type: {compute_type}")
    try:
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        segments, info = model.transcribe(audio_path, word_timestamps=True)
        
        segment_results = []
        for segment in segments:
            words = []
            if segment.words:
                for word in segment.words:
                    words.append(WordResult(
                        word=word.word,
                        start=word.start,
                        end=word.end,
                        probability=word.probability
                    ))
            
            segment_results.append(SegmentResult(
                id=segment.id,
                start=segment.start,
                end=segment.end,
                text=segment.text,
                words=words
            ))
            
        return TranscriptionResult(
            language=info.language,
            duration=info.duration,
            segments=segment_results,
            model_used=f"local-{model_size}"
        )
    except Exception as e:
        logger.error(f"Local transcription failed: {e}")
        raise LocalTranscriptionError(f"Local transcription error: {e}")
