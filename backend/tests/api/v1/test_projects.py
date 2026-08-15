import pytest
import uuid
from httpx import AsyncClient
from app.db.models import Project

@pytest.mark.asyncio
async def test_create_project(client: AsyncClient):
    response = await client.post("/api/v1/projects", json={"name": "Test Project"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Project"
    assert "id" in data
    assert data["status"] == "active"

@pytest.mark.asyncio
async def test_create_project_empty_name(client: AsyncClient):
    response = await client.post("/api/v1/projects", json={"name": ""})
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_list_projects(client: AsyncClient):
    # Create two projects
    await client.post("/api/v1/projects", json={"name": "Project 1"})
    await client.post("/api/v1/projects", json={"name": "Project 2"})
    
    response = await client.get("/api/v1/projects")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    names = [p["name"] for p in data]
    assert "Project 1" in names
    assert "Project 2" in names

@pytest.mark.asyncio
async def test_get_project(client: AsyncClient):
    create_response = await client.post("/api/v1/projects", json={"name": "Project 3"})
    project_id = create_response.json()["id"]
    
    response = await client.get(f"/api/v1/projects/{project_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id
    assert data["name"] == "Project 3"

@pytest.mark.asyncio
async def test_get_project_not_found(client: AsyncClient):
    fake_id = str(uuid.uuid4())
    response = await client.get(f"/api/v1/projects/{fake_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_project(client: AsyncClient):
    create_response = await client.post("/api/v1/projects", json={"name": "Old Name"})
    project_id = create_response.json()["id"]
    
    response = await client.patch(f"/api/v1/projects/{project_id}", json={"name": "New Name"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"

@pytest.mark.asyncio
async def test_delete_project(client: AsyncClient):
    create_response = await client.post("/api/v1/projects", json={"name": "To Delete"})
    project_id = create_response.json()["id"]
    
    response = await client.delete(f"/api/v1/projects/{project_id}")
    assert response.status_code == 204
    
    get_response = await client.get(f"/api/v1/projects/{project_id}")
    assert get_response.status_code == 404
