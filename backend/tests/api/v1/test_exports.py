import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Project, Source, ClipDiscoveryRun, ClipCandidate, Transcript, TranscriptSegment, TranscriptWord, RenderJob
import uuid
import os

@pytest.fixture
async def setup_export_data(db_session: AsyncSession):
    project = Project(name="Test Project")
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)

    source = Source(
        project_id=project.id,
        url="https://youtube.com/watch?v=123",
        status="completed",
        title="Test Source",
        duration=100
    )
    db_session.add(source)
    await db_session.commit()
    await db_session.refresh(source)

    run = ClipDiscoveryRun(
        source_id=source.id,
        status="completed"
    )
    db_session.add(run)
    await db_session.commit()
    await db_session.refresh(run)

    clip = ClipCandidate(
        run_id=run.id,
        project_id=project.id,
        start_time=10.0,
        end_time=20.0,
        title="Test Clip",
        score=9.0,
        explanation="Test explanation",
        status="approved"
    )
    db_session.add(clip)
    await db_session.commit()
    await db_session.refresh(clip)

    transcript = Transcript(
        source_id=source.id,
        status="completed"
    )
    db_session.add(transcript)
    await db_session.commit()
    await db_session.refresh(transcript)

    segment = TranscriptSegment(
        transcript_id=transcript.id,
        segment_index=0,
        start_time=10.0,
        end_time=20.0,
        text="Hello world"
    )
    db_session.add(segment)
    await db_session.commit()
    await db_session.refresh(segment)

    word1 = TranscriptWord(
        segment_id=segment.id,
        word_index=0,
        start_time=10.0,
        end_time=11.0,
        word="Hello",
        probability=0.9
    )
    word2 = TranscriptWord(
        segment_id=segment.id,
        word_index=1,
        start_time=11.0,
        end_time=12.0,
        word="world",
        probability=0.9
    )
    db_session.add_all([word1, word2])
    await db_session.commit()

    # Create dummy output file
    output_path = f"/tmp/test_output_{uuid.uuid4()}.mp4"
    with open(output_path, "w") as f:
        f.write("dummy video data")

    job = RenderJob(
        clip_id=clip.id,
        project_id=project.id,
        status="completed",
        progress=100.0,
        output_path=output_path
    )
    db_session.add(job)
    await db_session.commit()
    await db_session.refresh(job)

    return project, job, output_path

@pytest.mark.asyncio
async def test_list_exports(async_client: AsyncClient, setup_export_data):
    project, job, _ = setup_export_data
    
    response = await async_client.get(f"/api/v1/projects/{project.id}/exports")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == str(job.id)

@pytest.mark.asyncio
async def test_download_video(async_client: AsyncClient, setup_export_data):
    _, job, output_path = setup_export_data
    
    response = await async_client.get(f"/api/v1/exports/{job.id}/download/video")
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"

    if os.path.exists(output_path):
        os.remove(output_path)

@pytest.mark.asyncio
async def test_download_captions(async_client: AsyncClient, setup_export_data):
    _, job, output_path = setup_export_data
    
    response = await async_client.get(f"/api/v1/exports/{job.id}/download/captions?format=srt")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/x-subrip"
    text = response.text
    assert "Hello world" in text
    
    response = await async_client.get(f"/api/v1/exports/{job.id}/download/captions?format=vtt")
    assert response.status_code == 200
    assert "WEBVTT" in response.text
    
    response = await async_client.get(f"/api/v1/exports/{job.id}/download/captions?format=txt")
    assert response.status_code == 200
    assert response.text.strip() == "Hello world"
    
    if os.path.exists(output_path):
        os.remove(output_path)

@pytest.mark.asyncio
async def test_retry_render(async_client: AsyncClient, setup_export_data):
    project, job, output_path = setup_export_data
    
    response = await async_client.post(f"/api/v1/renders/{job.id}/retry")
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "queued"
    assert data["progress"] == 0.0
    
    if os.path.exists(output_path):
        os.remove(output_path)
