from typing import List, Optional
import uuid
from app.repositories.project import ProjectRepository
from app.db.models import Project

class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def create_project(self, name: str, user_id: uuid.UUID) -> Project:
        if not name or not name.strip():
            raise ValueError("Project name cannot be empty")
        return await self.repository.create(name.strip(), user_id)

    async def get_project(self, project_id: uuid.UUID) -> Optional[Project]:
        return await self.repository.get_by_id(project_id)

    async def list_projects(self, user_id: uuid.UUID) -> List[Project]:
        return await self.repository.list_by_user(user_id)

    async def update_project(self, project_id: uuid.UUID, name: str) -> Optional[Project]:
        project = await self.repository.get_by_id(project_id)
        if not project:
            return None
        if not name or not name.strip():
            raise ValueError("Project name cannot be empty")
        project.name = name.strip()
        return await self.repository.update(project)

    async def delete_project(self, project_id: uuid.UUID) -> bool:
        project = await self.repository.get_by_id(project_id)
        if not project:
            return False
        await self.repository.delete(project)
        return True

    async def claim_project(self, project_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Project]:
        project = await self.repository.get_by_id(project_id)
        if not project:
            return None
        if project.user_id is not None:
            # Already claimed
            raise PermissionError("Project has already been claimed")
        
        # Claim
        project.user_id = user_id
        return await self.repository.update(project)
