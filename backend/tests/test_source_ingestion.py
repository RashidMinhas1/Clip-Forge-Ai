import pytest
import uuid
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

from app.main import app
from app.services.source.youtube import YouTubeProviderException
from app.services.source.validator import SourceValidationError
from app.services.source.media_probe import MediaProbeException

from app.api.deps import get_current_user
from app.db.models import User, Project

client = TestClient(app)
test_project_id = str(uuid.uuid4())

@patch("app.api.v1.sources.get_authorized_project", new_callable=AsyncMock)
@patch("app.services.source.youtube.YouTubeSourceProvider.extract_metadata")
@patch("app.services.source.youtube.YouTubeSourceProvider.download_video")
@patch("app.services.source.media_probe.MediaProbeService.probe_file")
@patch("app.services.source.storage.StorageService.generate_source_path")
def test_ingest_youtube_success(mock_generate_path, mock_probe, mock_download, mock_extract, mock_auth):
    mock_auth.return_value = Project(id=uuid.UUID(test_project_id))
    mock_extract.return_value = {
        "id": "dQw4w9WgXcQ",
        "title": "Never Gonna Give You Up",
        "duration": 212
    }
    mock_download.return_value = None
    mock_probe.return_value = {
        "duration": 212.0,
        "width": 1920,
        "height": 1080,
        "fps": 30.0,
        "video_codec": "h264",
        "audio_codec": "aac",
        "has_audio": True,
        "container": "mp4",
        "file_size": 15000000
    }
    mock_generate_path.return_value = "/mock/storage/1234.mp4"

    response = client.post("/api/v1/sources/youtube", json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "project_id": test_project_id})

    assert response.status_code == 200
    assert response.json()["source_type"] == "youtube"
    assert response.json()["title"] == "Never Gonna Give You Up"

@patch("app.api.v1.sources.get_authorized_project", new_callable=AsyncMock)
@patch("app.services.source.youtube.YouTubeSourceProvider.extract_metadata")
def test_ingest_youtube_metadata_failure(mock_extract, mock_auth):
    mock_auth.return_value = Project(id=uuid.UUID(test_project_id))
    mock_extract.side_effect = YouTubeProviderException("Not found", "SOURCE_UNAVAILABLE")

    response = client.post("/api/v1/sources/youtube", json={"url": "https://www.youtube.com/watch?v=invalid", "project_id": test_project_id})

    assert response.status_code == 400

@patch("app.api.v1.sources.get_authorized_project", new_callable=AsyncMock)
def test_ingest_youtube_invalid_url(mock_auth):
    mock_auth.return_value = Project(id=uuid.UUID(test_project_id))
    # It should fail basic regex validation
    response = client.post("/api/v1/sources/youtube", json={"url": "https://example.com/video.mp4", "project_id": test_project_id})

    assert response.status_code == 400

@patch("app.api.v1.sources.get_authorized_project", new_callable=AsyncMock)
@patch("app.services.source.media_probe.MediaProbeService.probe_file")
@patch("app.services.source.storage.StorageService.generate_source_path")
@patch("builtins.open", new_callable=MagicMock)
def test_ingest_local_success(mock_open, mock_generate_path, mock_probe, mock_auth):
    mock_auth.return_value = Project(id=uuid.UUID(test_project_id))
    mock_generate_path.return_value = "/mock/storage/local.mp4"
    mock_probe.return_value = {
        "duration": 60.0,
        "width": 1280,
        "height": 720,
        "fps": 60.0,
        "video_codec": "hevc",
        "audio_codec": "aac",
        "has_audio": True,
        "container": "mp4",
        "file_size": 5000000
    }

    file_content = b"fake video content"
    response = client.post(
        "/api/v1/sources/local",
        data={"project_id": test_project_id},
        files={"file": ("test_video.mp4", file_content, "video/mp4")}
    )

    assert response.status_code == 200
    assert response.json()["source_type"] == "local"

@patch("app.api.v1.sources.get_authorized_project", new_callable=AsyncMock)
def test_ingest_local_unsupported_extension(mock_auth):
    mock_auth.return_value = Project(id=uuid.UUID(test_project_id))
    file_content = b"fake document"
    response = client.post(
        "/api/v1/sources/local",
        data={"project_id": test_project_id},
        files={"file": ("test.pdf", file_content, "application/pdf")}
    )

    assert response.status_code == 400
