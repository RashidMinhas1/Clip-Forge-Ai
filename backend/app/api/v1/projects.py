from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from app.api.deps import get_current_user
from app.core.supabase import get_supabase_client

router = APIRouter(prefix="/projects", tags=["Projects"])

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    created_at: str
    updated_at: str

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, current_user: dict = Depends(get_current_user)):
    """Create a new project."""
    supabase = get_supabase_client()
    data = {
        "user_id": current_user["id"],
        "name": project.name,
        "description": project.description
    }
    
    response = supabase.table("projects").insert(data).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create project")
    
    return response.data[0]

@router.get("/", response_model=List[ProjectResponse])
def list_projects(current_user: dict = Depends(get_current_user)):
    """List all projects owned by the current user."""
    supabase = get_supabase_client()
    # Since we use service_role client, we MUST manually enforce user_id filtering here
    response = supabase.table("projects").select("*").eq("user_id", current_user["id"]).execute()
    return response.data

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific project."""
    supabase = get_supabase_client()
    response = supabase.table("projects").select("*").eq("id", project_id).eq("user_id", current_user["id"]).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Project not found")
        
    return response.data[0]

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a specific project."""
    supabase = get_supabase_client()
    response = supabase.table("projects").delete().eq("id", project_id).eq("user_id", current_user["id"]).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Project not found or already deleted")
    
    return None
