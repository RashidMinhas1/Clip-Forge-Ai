from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime

class RenderJobCreate(BaseModel):
    clip_id: UUID

class RenderJobResponse(BaseModel):
    id: UUID
    clip_id: UUID
    project_id: UUID
    status: str
    progress: float
    output_path: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
