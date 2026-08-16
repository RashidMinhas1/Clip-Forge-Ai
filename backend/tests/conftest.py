"""
Root conftest.py for all backend tests.

Provides the `client` fixture (an httpx.AsyncClient pointed at the FastAPI app)
used by API-layer tests.  Tests that exercise the database directly
(e.g. test_projects.py) will remain BLOCKED — ENVIRONMENT when PostgreSQL is
unavailable; the fixture itself does not require a live DB connection.
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    """Async HTTP client bound to the FastAPI ASGI app."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as ac:
        yield ac
