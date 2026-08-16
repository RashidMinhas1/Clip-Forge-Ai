from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from uuid import UUID
from app.db.models import ClipDiscoveryRun, ClipCandidate
from app.models.clipping import ClipCandidateCreate

class ClippingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_run(self, project_id: UUID, source_id: UUID) -> ClipDiscoveryRun:
        run = ClipDiscoveryRun(
            project_id=project_id,
            source_id=source_id,
            status="queued"
        )
        self.session.add(run)
        await self.session.commit()
        await self.session.refresh(run)
        return run

    async def get_run(self, run_id: UUID, project_id: UUID) -> Optional[ClipDiscoveryRun]:
        stmt = select(ClipDiscoveryRun).options(selectinload(ClipDiscoveryRun.candidates)).where(
            ClipDiscoveryRun.id == run_id,
            ClipDiscoveryRun.project_id == project_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_run_status(self, run_id: UUID, status: str, error_message: Optional[str] = None) -> None:
        stmt = select(ClipDiscoveryRun).where(ClipDiscoveryRun.id == run_id)
        result = await self.session.execute(stmt)
        run = result.scalars().first()
        if run:
            run.status = status
            if error_message:
                run.error_message = error_message
            await self.session.commit()

    async def create_candidates(self, candidates_data: List[ClipCandidateCreate]) -> List[ClipCandidate]:
        candidates = [ClipCandidate(**data.dict()) for data in candidates_data]
        self.session.add_all(candidates)
        await self.session.commit()
        return candidates

    async def get_candidates_for_project(self, project_id: UUID) -> List[ClipCandidate]:
        stmt = select(ClipCandidate).where(ClipCandidate.project_id == project_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
