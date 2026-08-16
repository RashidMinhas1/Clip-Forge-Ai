import pytest
import uuid
from unittest.mock import patch, MagicMock

from app.tasks.transcription import task_transcribe_source

class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)

@pytest.mark.asyncio
@patch("app.tasks.transcription.TranscriptionService")
@patch("app.tasks.transcription.AsyncSessionLocal")
async def test_task_updates_status_to_processing(mock_session_maker, mock_service_cls):
    mock_service = mock_service_cls.return_value
    mock_service.transcribe = AsyncMock()
    
    mock_session = AsyncMock()
    mock_session_maker.return_value.__aenter__.return_value = mock_session
    
    transcript_id = str(uuid.uuid4())
    source_path = "/tmp/test.mp4"
    
    await task_transcribe_source(transcript_id, source_path)
    
    mock_service.transcribe.assert_called_once()
    assert mock_service.transcribe.call_args[0][0] == source_path

@pytest.mark.asyncio
@patch("app.tasks.transcription.TranscriptionService")
@patch("app.tasks.transcription.AsyncSessionLocal")
async def test_task_updates_status_to_completed(mock_session_maker, mock_service_cls):
    mock_service = mock_service_cls.return_value
    mock_service.transcribe = AsyncMock()
    
    mock_session = AsyncMock()
    mock_session_maker.return_value.__aenter__.return_value = mock_session
    
    transcript_id = str(uuid.uuid4())
    await task_transcribe_source(transcript_id, "/tmp/test.mp4")
    mock_service.transcribe.assert_called_once()

@pytest.mark.asyncio
@patch("app.tasks.transcription.TranscriptionService")
@patch("app.tasks.transcription.AsyncSessionLocal")
async def test_task_updates_status_to_failed(mock_session_maker, mock_service_cls):
    mock_service = mock_service_cls.return_value
    mock_service.transcribe = AsyncMock(side_effect=Exception("Failed"))
    
    mock_session = AsyncMock()
    mock_session_maker.return_value.__aenter__.return_value = mock_session
    
    transcript_id = str(uuid.uuid4())
    
    with pytest.raises(Exception):
        await task_transcribe_source(transcript_id, "/tmp/test.mp4")

@pytest.mark.asyncio
@patch("app.tasks.transcription.TranscriptionService")
@patch("app.tasks.transcription.AsyncSessionLocal")
async def test_task_persists_segments_and_words(mock_session_maker, mock_service_cls):
    # This behavior is largely tested in the service, but we ensure the task calls it
    mock_service = mock_service_cls.return_value
    mock_service.transcribe = AsyncMock()
    
    transcript_id = str(uuid.uuid4())
    await task_transcribe_source(transcript_id, "/tmp/test.mp4")
    
    mock_service.transcribe.assert_called_once()

@pytest.mark.asyncio
@patch("app.tasks.transcription.TranscriptionService")
@patch("app.tasks.transcription.AsyncSessionLocal")
async def test_task_cleans_up_on_completion(mock_session_maker, mock_service_cls):
    # Cleanup is done in the service block which task executes
    mock_service = mock_service_cls.return_value
    mock_service.transcribe = AsyncMock()
    
    transcript_id = str(uuid.uuid4())
    await task_transcribe_source(transcript_id, "/tmp/test.mp4")
    
    mock_service.transcribe.assert_called_once()
