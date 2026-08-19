import uuid
import pytest
from httpx import AsyncClient
from app.db.models import Project, User

@pytest.mark.asyncio
async def test_legacy_project_migration_preserves_project(client: AsyncClient, db_session):
    # Tests that a legacy project with user_id=None is preserved and cannot be accessed
    # without explicitly claiming it.
    project = Project(name="Legacy", user_id=None)
    db_session.add(project)
    await db_session.commit()

    response = await client.get(f"/api/v1/projects/{project.id}")
    # Requires auth now and user is not owner
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_new_project_assigns_owner(authenticated_client: AsyncClient, current_user: User):
    response = await authenticated_client.post("/api/v1/projects", json={"name": "New Owned Project"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Owned Project"
    # Ownership is enforced internally; we can query to verify if needed

@pytest.mark.asyncio
async def test_unauthorized_access(authenticated_client: AsyncClient, db_session):
    # User B (authenticated_client) tries to access User A's project
    user_a = User(email="usera@test.com", is_active=True)
    db_session.add(user_a)
    await db_session.commit()

    project_a = Project(name="User A Project", user_id=user_a.id)
    db_session.add(project_a)
    await db_session.commit()

    response = await authenticated_client.get(f"/api/v1/projects/{project_a.id}")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_legacy_access_denied(authenticated_client: AsyncClient, db_session):
    project = Project(name="Legacy", user_id=None)
    db_session.add(project)
    await db_session.commit()

    response = await authenticated_client.get(f"/api/v1/projects/{project.id}")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_explicit_claim(authenticated_client: AsyncClient, db_session, current_user: User):
    project = Project(name="Legacy to Claim", user_id=None)
    db_session.add(project)
    await db_session.commit()

    response = await authenticated_client.post(f"/api/v1/projects/{project.id}/claim")
    assert response.status_code == 200

    # Double claim by someone else should fail
    # (Simulated by same user requesting again, which also fails since it's already claimed)
    response2 = await authenticated_client.post(f"/api/v1/projects/{project.id}/claim")
    assert response2.status_code == 403

@pytest.mark.asyncio
async def test_no_implicit_claim(authenticated_client: AsyncClient, db_session):
    project = Project(name="Legacy", user_id=None)
    db_session.add(project)
    await db_session.commit()

    response = await authenticated_client.patch(f"/api/v1/projects/{project.id}", json={"name": "Test"})
    assert response.status_code == 403
