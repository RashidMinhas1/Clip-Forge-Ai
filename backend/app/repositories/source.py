from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Source
from app.models.source import SourceMetadata

class SourceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, project_id: uuid.UUID, metadata: SourceMetadata) -> Source:
        source_data = metadata.model_dump()
        source_id = source_data.pop("id")
        
        source = Source(
            id=source_id,
            project_id=project_id,
            **source_data
        )
        self.session.add(source)
        await self.session.commit()
        await self.session.refresh(source)
        return source

    async def get_by_id(self, source_id: uuid.UUID) -> Optional[Source]:
        result = await self.session.execute(
            select(Source).where(Source.id == source_id)
        )
        return result.scalars().first()

    async def get_by_project(self, project_id: uuid.UUID) -> List[Source]:
        result = await self.session.execute(
            select(Source).where(Source.project_id == project_id).order_by(Source.created_at.desc())
        )
        return list(result.scalars().all())

    async def delete(self, source: Source) -> None:
        await self.session.delete(source)
        await self.session.commit()
