from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class AIRequest(BaseModel):
    messages: List[Dict[str, str]]
    model: str
    max_tokens: int = 1024
    temperature: float = 0.7

class AIResponse(BaseModel):
    content: str
    provider: str
    model: str
    usage: Dict[str, int]
    latency: float
