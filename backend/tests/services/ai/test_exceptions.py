import pytest
from app.services.ai.exceptions import AIProviderError, AIAuthenticationError, AITimeoutError, AIRateLimitError

def test_exceptions_hierarchy():
    assert issubclass(AIAuthenticationError, AIProviderError)
    assert issubclass(AITimeoutError, AIProviderError)
    assert issubclass(AIRateLimitError, AIProviderError)

def test_exception_instantiation():
    exc = AIAuthenticationError("Invalid API Key")
    assert str(exc) == "Invalid API Key"
