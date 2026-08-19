import pytest
import uuid
from httpx import AsyncClient

from app.api.deps import get_authorized_project
from app.db.models import Project

@pytest.fixture(autouse=True)
def override_auth_project():
    from app.main import app
    app.dependency_overrides[get_authorized_project] = lambda: Project(id=uuid.uuid4(), user_id=uuid.uuid4())
    yield
    app.dependency_overrides.pop(get_authorized_project, None)

@pytest.mark.asyncio
async def test_create_clip_discovery_with_overrides(mocker, authenticated_client: AsyncClient):
    from app.api.v1.clipping import get_clipping_repo
    from app.main import app
    
    project_id = uuid.uuid4()
    source_id = uuid.uuid4()
    run_id = uuid.uuid4()
    
    mock_repo = mocker.AsyncMock()
    mock_repo.create_run.return_value = mocker.MagicMock(
        id=run_id,
        project_id=project_id,
        source_id=source_id,
        status="queued",
        error_message=None,
        created_at="2026-08-16T11:34:00Z",
        updated_at="2026-08-16T11:34:00Z"
    )
    
    app.dependency_overrides[get_clipping_repo] = lambda: mock_repo
    
    mocker.patch("app.api.v1.clipping.task_discover_clips.kiq", new_callable=mocker.AsyncMock)
    
    response = await authenticated_client.post(f"/api/v1/projects/{project_id}/sources/{source_id}/clip-discovery")
    
    app.dependency_overrides.pop(get_clipping_repo, None)
    
    assert response.status_code == 202
    assert response.json()["id"] == str(run_id)

@pytest.mark.asyncio
async def test_update_clip_candidate_status(mocker, authenticated_client: AsyncClient):
    from app.api.v1.clipping import get_clipping_repo
    from app.main import app
    
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
        status="approved",
        framing_mode="auto"
    )
    
    app.dependency_overrides[get_clipping_repo] = lambda: mock_repo
    
    response = await authenticated_client.patch(f"/api/v1/projects/{project_id}/candidates/{candidate_id}/status", json={"status": "approved"})
    
    app.dependency_overrides.pop(get_clipping_repo, None)
    
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
    assert response.json()["id"] == str(candidate_id)
