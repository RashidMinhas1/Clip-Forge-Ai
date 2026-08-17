from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from uuid import UUID

class CaptionWord(BaseModel):
    word: str
    start_time: float
    end_time: float
    is_active: bool = False

class CaptionChunk(BaseModel):
    text: str
    start_time: float
    end_time: float
    words: List[CaptionWord]

class CaptionConfigUpdate(BaseModel):
    preset_name: Optional[str] = Field(None, pattern=r"^[a-zA-Z0-9_-]+$")
    font_family: Optional[str] = Field(None, pattern=r"^[a-zA-Z0-9\s_-]+$")
    font_size: Optional[int] = Field(None, ge=8, le=144)
    text_color: Optional[str] = Field(None, pattern=r"^#(?:[0-9a-fA-F]{3,4}){1,2}$")
    highlight_color: Optional[str] = Field(None, pattern=r"^#(?:[0-9a-fA-F]{3,4}){1,2}$")
    bg_color: Optional[str] = Field(None, pattern=r"^#(?:[0-9a-fA-F]{3,4}){1,2}$")
    is_rtl: Optional[bool] = None

class CaptionConfigResponse(BaseModel):
    id: UUID
    clip_id: UUID
    preset_name: str
    font_family: Optional[str] = None
    font_size: Optional[int] = None
    text_color: Optional[str] = None
    highlight_color: Optional[str] = None
    bg_color: Optional[str] = None
    is_rtl: bool

    model_config = ConfigDict(from_attributes=True)

class ClipCaptionsResponse(BaseModel):
    chunks: List[CaptionChunk]
    config: CaptionConfigResponse
