import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.repositories.project import ProjectRepository
from app.services.project import ProjectService
from app.models.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])

def get_project_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    repository = ProjectRepository(db)
    return ProjectService(repository)

@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(
    data: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    try:
        project = await service.create_project(name=data.name)
        return project
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    service: ProjectService = Depends(get_project_service)
):
    try:
        return await service.list_projects()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: uuid.UUID,
    service: ProjectService = Depends(get_project_service)
):
    try:
        project = await service.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: uuid.UUID,
    data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    try:
        project = await service.update_project(project_id, name=data.name)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: uuid.UUID,
    service: ProjectService = Depends(get_project_service)
):
    try:
        success = await service.delete_project(project_id)
        if not success:
            raise HTTPException(status_code=404, detail="Project not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
