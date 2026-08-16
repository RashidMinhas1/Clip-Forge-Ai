class AIProviderError(Exception):
    """Base exception for AI provider errors"""
    pass

class AIAuthenticationError(AIProviderError):
    """Authentication failed"""
    pass

class AITimeoutError(AIProviderError):
    """Request timed out"""
    pass

class AIRateLimitError(AIProviderError):
    """Rate limit exceeded"""
    pass
