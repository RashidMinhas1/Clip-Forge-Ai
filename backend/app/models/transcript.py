from typing import List, Optional
from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime

class TranscriptWordResponse(BaseModel):
    id: uuid.UUID
    word_index: int
    start_time: float
    end_time: float
    word: str
    probability: Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True)

class TranscriptSegmentResponse(BaseModel):
    id: uuid.UUID
    segment_index: int
    start_time: float
    end_time: float
    text: str
    words: List[TranscriptWordResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class TranscriptResponse(BaseModel):
    id: uuid.UUID
    source_id: uuid.UUID
    status: str
    language: Optional[str] = None
    duration: Optional[float] = None
    model_used: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    segments: List[TranscriptSegmentResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class TranscribeRequest(BaseModel):
    language: Optional[str] = None
