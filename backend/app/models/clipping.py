from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class AIClipCandidate(BaseModel):
    title: str = Field(..., description="A catchy title for the clip")
    hook: str = Field(..., description="The hook of the clip")
    reason: str = Field(..., description="Why this clip is engaging and valuable")
    start_word: str = Field(..., description="The exact first word of the clip excerpt, exactly as it appears in the transcript")
    end_word: str = Field(..., description="The exact last word of the clip excerpt, exactly as it appears in the transcript")
    excerpt: str = Field(..., description="The full exact text excerpt of the clip, matching the transcript exactly")
    score: float = Field(..., ge=0, le=10, description="Overall score out of 10")
    confidence: float = Field(..., ge=0, le=1, description="Confidence in the bounds and score, 0 to 1")

class AIClipCandidateList(BaseModel):
    candidates: List[AIClipCandidate] = Field(..., description="List of generated clip candidates")

class ClipCandidateCreate(BaseModel):
    run_id: UUID
    project_id: UUID
    title: str
    hook: str
    reason: str
    start_time: float
    end_time: float
    duration: float
    score: float
    confidence: float
    transcript_excerpt: str

class ClipCandidateUpdate(BaseModel):
    status: str

class ClipEditUpdate(BaseModel):
    start_time: float = Field(..., description="Adjusted start time in seconds")
    end_time: float = Field(..., description="Adjusted end time in seconds")
    framing_mode: str = Field(..., description="Framing mode e.g., ORIGINAL, FACE_TRACK_9_16, SPLIT_SCREEN")

class ClipCandidateResponse(BaseModel):
    id: UUID
    run_id: UUID
    project_id: UUID
    title: str
    hook: str
    reason: str
    start_time: float
    end_time: float
    duration: float
    score: float
    confidence: float
    transcript_excerpt: str
    status: str
    framing_mode: str

    class Config:
        orm_mode = True
        from_attributes = True

class ClipDiscoveryRunResponse(BaseModel):
    id: UUID
    project_id: UUID
    source_id: UUID
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    candidates: Optional[List[ClipCandidateResponse]] = None

    class Config:
        orm_mode = True
        from_attributes = True
