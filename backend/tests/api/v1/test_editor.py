import pytest
import uuid
from httpx import AsyncClient
from app.db.models import Project, Source, ClipDiscoveryRun, ClipCandidate

@pytest.fixture
async def sample_project(db_session):
    project = Project(name="Test Project", status="active")
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)
    return project

@pytest.fixture
async def sample_clip_candidate(db_session, sample_project):
    run = ClipDiscoveryRun(
        project_id=sample_project.id,
        source_id=uuid.uuid4(),
        status="completed"
    )
    db_session.add(run)
    await db_session.commit()
    await db_session.refresh(run)

    candidate = ClipCandidate(
        run_id=run.id,
        project_id=sample_project.id,
        title="Test Clip",
        hook="Hook",
        reason="Reason",
        start_time=10.0,
        end_time=20.0,
        duration=10.0,
        score=9.5,
        confidence=0.9,
        transcript_excerpt="Test excerpt",
        status="approved",
        framing_mode="ORIGINAL"
    )
    db_session.add(candidate)
    await db_session.commit()
    await db_session.refresh(candidate)
    return candidate

@pytest.mark.asyncio
async def test_get_clip(client: AsyncClient, sample_project, sample_clip_candidate):
    response = await client.get(f"/api/v1/projects/{sample_project.id}/clips/{sample_clip_candidate.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(sample_clip_candidate.id)
    assert data["start_time"] == 10.0
    assert data["end_time"] == 20.0
    assert data["framing_mode"] == "ORIGINAL"

@pytest.mark.asyncio
async def test_update_clip_edit(client: AsyncClient, sample_project, sample_clip_candidate):
    payload = {
        "start_time": 12.0,
        "end_time": 18.0,
        "framing_mode": "FACE_TRACK_9_16"
    }
    response = await client.patch(f"/api/v1/projects/{sample_project.id}/clips/{sample_clip_candidate.id}/edit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["start_time"] == 12.0
    assert data["end_time"] == 18.0
    assert data["duration"] == 6.0
    assert data["framing_mode"] == "FACE_TRACK_9_16"

@pytest.mark.asyncio
async def test_update_clip_edit_invalid_bounds(client: AsyncClient, sample_project, sample_clip_candidate):
    payload = {
        "start_time": 20.0,
        "end_time": 15.0,  # Invalid: start_time > end_time
        "framing_mode": "FACE_TRACK_9_16"
    }
    response = await client.patch(f"/api/v1/projects/{sample_project.id}/clips/{sample_clip_candidate.id}/edit", json=payload)
    assert response.status_code == 422
