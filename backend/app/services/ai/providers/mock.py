import time
from typing import Any, Dict
from app.services.ai.models import AIRequest, AIResponse
from app.services.ai.providers.base import BaseAIProvider

class MockProvider(BaseAIProvider):
    async def generate_text(self, req: AIRequest) -> AIResponse:
        return AIResponse(
            content="Mock response",
            provider="mock",
            model=req.model,
            usage={"total_tokens": 10},
            latency=0.1
        )

    async def generate_structured(self, req: AIRequest, schema: Dict[str, Any]) -> AIResponse:
        return await self.generate_text(req)
