import pytest
import uuid
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.clipping.discovery import ClipDiscoveryService
from app.models.clipping import AIClipCandidateList, AIClipCandidate
from app.db.models import Transcript, TranscriptWord, TranscriptSegment

@pytest.fixture
def mock_session():
    session = AsyncMock()
    return session

@pytest.mark.asyncio
async def test_discover_clips_success(mock_session):
    service = ClipDiscoveryService(mock_session)
    service.clipping_repo = AsyncMock()
    service.ai_router = AsyncMock()
    
    run_id = uuid.uuid4()
    project_id = uuid.uuid4()
    source_id = uuid.uuid4()
    
    # Mock transcript
    transcript = Transcript(id=uuid.uuid4(), source_id=source_id, status="completed")
    
    # Mock words
    word1 = TranscriptWord(word="Hello", start_time=0.0, end_time=1.0)
    word2 = TranscriptWord(word="world", start_time=1.0, end_time=2.0)
    word3 = TranscriptWord(word="this", start_time=2.0, end_time=3.0)
    word4 = TranscriptWord(word="is", start_time=3.0, end_time=4.0)
    word5 = TranscriptWord(word="great", start_time=4.0, end_time=5.0)
    
    # Mock database queries
    mock_result_transcript = MagicMock()
    mock_result_transcript.scalars().first.return_value = transcript
    
    mock_result_words = MagicMock()
    mock_result_words.scalars().all.return_value = [word1, word2, word3, word4, word5]
    
    mock_session.execute.side_effect = [mock_result_transcript, mock_result_words]
    
    # Mock AI response
    ai_response = MagicMock()
    ai_response.content = AIClipCandidateList(candidates=[
        AIClipCandidate(
            title="Great Clip",
            hook="Hello world",
            reason="Good hook",
            start_word="Hello",
            end_word="great",
            excerpt="Hello world this is great",
            score=9.0,
            confidence=0.9
        )
    ]).json()
    service.ai_router.generate_structured.return_value = ai_response
    
    await service.discover_clips(run_id, project_id, source_id)
    
    service.clipping_repo.update_run_status.assert_any_call(run_id, "processing")
    service.clipping_repo.create_candidates.assert_called_once()
    
    # Verify candidate times
    args = service.clipping_repo.create_candidates.call_args[0][0]
    assert len(args) == 1
    assert args[0].start_time == 0.0
    assert args[0].end_time == 5.0
    
    service.clipping_repo.update_run_status.assert_any_call(run_id, "completed")
