import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.deps import get_current_user
from app.db.database import get_db, Base
from app.db.models import User

# Use an in-memory SQLite database for testing
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

async def override_get_current_user():
    return User(id=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"), email="test@test.com", is_active=True, app_activated=True)

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(scope="function", autouse=True)
async def reset_overrides():
    # Save the original overrides
    original_overrides = app.dependency_overrides.copy()
    yield
    # Restore the original overrides
    app.dependency_overrides = original_overrides

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def current_user(db_session):
    user = User(id=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"), email="test@test.com", is_active=True, app_activated=True)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest_asyncio.fixture
async def client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as ac:
        yield ac

@pytest_asyncio.fixture
async def async_client(client) -> AsyncClient:
    return client

@pytest_asyncio.fixture
async def authenticated_client(client) -> AsyncClient:
    return client

