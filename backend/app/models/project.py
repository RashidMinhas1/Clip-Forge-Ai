from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime
from .source import SourceMetadata

class ProjectCreate(BaseModel):
    name: str

class ProjectUpdate(BaseModel):
    name: str

class ProjectResponse(BaseModel):
    id: uuid.UUID
    name: str
    status: str
    created_at: datetime
    updated_at: datetime
    sources: Optional[List[SourceMetadata]] = []

    model_config = ConfigDict(from_attributes=True)
