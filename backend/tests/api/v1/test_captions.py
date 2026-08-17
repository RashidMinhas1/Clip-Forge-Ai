import pytest
from httpx import AsyncClient
from uuid import uuid4

@pytest.mark.asyncio
async def test_get_captions_not_found(client: AsyncClient):
    project_id = uuid4()
    clip_id = uuid4()
    response = await client.get(f"/api/v1/projects/{project_id}/clips/{clip_id}/captions")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_patch_captions_config_not_found(client: AsyncClient):
    project_id = uuid4()
    clip_id = uuid4()
    response = await client.patch(
        f"/api/v1/projects/{project_id}/clips/{clip_id}/caption-config",
        json={"preset_name": "test_preset"}
    )
    assert response.status_code == 404
