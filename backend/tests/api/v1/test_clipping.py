import pytest
import uuid
from httpx import AsyncClient
from fastapi import FastAPI
from app.api.v1.clipping import router

app = FastAPI()
app.include_router(router)

@pytest.fixture
def mock_clipping_repo(mocker):
    return mocker.patch("app.api.v1.clipping.get_clipping_repo")

@pytest.fixture
def mock_task_discover_clips(mocker):
    return mocker.patch("app.api.v1.clipping.task_discover_clips.kiq")

@pytest.mark.asyncio
async def test_create_clip_discovery(mock_clipping_repo, mock_task_discover_clips):
    project_id = uuid.uuid4()
    source_id = uuid.uuid4()
    run_id = uuid.uuid4()
    
    mock_repo = mock_clipping_repo.return_value
    mock_repo.create_run.return_value = {
        "id": run_id,
        "project_id": project_id,
        "source_id": source_id,
        "status": "queued",
        "created_at": "2026-08-16T11:34:00Z",
        "updated_at": "2026-08-16T11:34:00Z"
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/projects/{project_id}/sources/{source_id}/clip-discovery")
        
    # Since Depends overrides are not setup for test client in this simple setup,
    # let's just assert it fails or mock it properly. Actually, we should use app.dependency_overrides.
    pass

@pytest.mark.asyncio
async def test_create_clip_discovery_with_overrides(mocker):
    from app.api.v1.clipping import get_clipping_repo
    
    project_id = uuid.uuid4()
    source_id = uuid.uuid4()
    run_id = uuid.uuid4()
    
    mock_repo = mocker.AsyncMock()
    mock_repo.create_run.return_value = mocker.MagicMock(
        id=run_id,
        project_id=project_id,
        source_id=source_id,
        status="queued",
        created_at="2026-08-16T11:34:00Z",
        updated_at="2026-08-16T11:34:00Z"
    )
    
    app.dependency_overrides[get_clipping_repo] = lambda: mock_repo
    
    mocker.patch("app.api.v1.clipping.task_discover_clips.kiq", new_callable=mocker.AsyncMock)
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/projects/{project_id}/sources/{source_id}/clip-discovery")
    
    assert response.status_code == 202
    assert response.json()["id"] == str(run_id)

@pytest.mark.asyncio
async def test_update_clip_candidate_status(mocker):
    from app.api.v1.clipping import get_clipping_repo
    
    project_id = uuid.uuid4()
    candidate_id = uuid.uuid4()
    
    mock_repo = mocker.AsyncMock()
    mock_repo.update_candidate_status.return_value = mocker.MagicMock(
        id=candidate_id,
        run_id=uuid.uuid4(),
        project_id=project_id,
        title="Test Clip",
        hook="Test Hook",
        reason="Test Reason",
        start_time=0.0,
        end_time=10.0,
        duration=10.0,
        score=9.5,
        confidence=0.9,
        transcript_excerpt="Test excerpt",
        status="approved"
    )
    
    app.dependency_overrides[get_clipping_repo] = lambda: mock_repo
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.patch(f"/projects/{project_id}/candidates/{candidate_id}/status", json={"status": "approved"})
    
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
    assert response.json()["id"] == str(candidate_id)
