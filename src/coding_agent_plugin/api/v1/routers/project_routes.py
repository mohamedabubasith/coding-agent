from typing import List
from fastapi import APIRouter, status

from coding_agent_plugin.models.project import ProjectCreate, ProjectResponse
from coding_agent_plugin.services.project import project_service

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project_in: ProjectCreate):
    """Create a new project."""
    return await project_service.create_project(project_in)

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(skip: int = 0, limit: int = 100):
    """List all projects."""
    return await project_service.list_projects(skip, limit)

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """Get a specific project."""
    return await project_service.get_project(project_id)
