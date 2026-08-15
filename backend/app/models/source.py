from typing import Optional, Literal
from datetime import datetime, timezone
from pydantic import BaseModel, HttpUrl, Field

class SourceUploadRequest(BaseModel):
    pass  # Used for local uploads if additional metadata is needed

class YouTubeIngestionRequest(BaseModel):
    url: str = Field(..., description="The YouTube URL to ingest")

class SourceMetadata(BaseModel):
    source_id: str
    source_type: Literal["local", "youtube"]
    original_url: Optional[str] = None
    normalized_url: Optional[str] = None
    provider: Optional[str] = None
    provider_video_id: Optional[str] = None
    title: Optional[str] = None
    duration: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    video_codec: Optional[str] = None
    audio_codec: Optional[str] = None
    has_audio: bool = False
    container: Optional[str] = None
    file_size: Optional[int] = None
    local_storage_reference: Optional[str] = None
    ingestion_status: Literal["accepted", "invalid", "unsupported", "corrupted", "unavailable", "processing", "failed"]
    validation_status: Literal["valid", "invalid", "pending"]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    error_code: Optional[str] = None
    error_message: Optional[str] = None
