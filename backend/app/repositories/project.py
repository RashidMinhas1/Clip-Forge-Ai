from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db.models import Project

class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, user_id: uuid.UUID) -> Project:
        project = Project(name=name, user_id=user_id)
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def get_by_id(self, project_id: uuid.UUID) -> Optional[Project]:
        # Gets by ID without checking ownership (used internally, or when checking if claimable)
        result = await self.session.execute(
            select(Project)
            .options(selectinload(Project.sources))
            .where(Project.id == project_id)
        )
        return result.scalars().first()

    async def list_by_user(self, user_id: uuid.UUID) -> List[Project]:
        result = await self.session.execute(
            select(Project).where(Project.user_id == user_id).order_by(Project.created_at.desc())
        )
        return list(result.scalars().all())

    async def update(self, project: Project) -> Project:
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def delete(self, project: Project) -> None:
        await self.session.delete(project)
        await self.session.commit()
