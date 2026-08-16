from abc import ABC, abstractmethod
from typing import Any, Dict
from app.services.ai.models import AIRequest, AIResponse

class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_text(self, req: AIRequest) -> AIResponse:
        pass

    @abstractmethod
    async def generate_structured(self, req: AIRequest, schema: Dict[str, Any]) -> AIResponse:
        pass
