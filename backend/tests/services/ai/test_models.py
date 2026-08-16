from app.services.ai.models import AIRequest, AIResponse

def test_ai_request_defaults():
    req = AIRequest(messages=[{"role": "user", "content": "Hello"}], model="test-model")
    assert req.max_tokens == 1024
    assert req.temperature == 0.7
    assert len(req.messages) == 1
    assert req.model == "test-model"

def test_ai_response():
    resp = AIResponse(
        content="Hello world",
        provider="test-provider",
        model="test-model",
        usage={"total_tokens": 10},
        latency=0.5
    )
    assert resp.content == "Hello world"
    assert resp.provider == "test-provider"
    assert resp.latency == 0.5
