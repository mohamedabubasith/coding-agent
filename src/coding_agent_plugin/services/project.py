import os
from typing import List, Optional
from fastapi import HTTPException, status

from coding_agent_plugin.core.config import AGENTIC_PROJECTS_DIR
from coding_agent_plugin.repository.project import project_repository
from coding_agent_plugin.models.project import ProjectCreate, ProjectResponse
from coding_agent_plugin.schemas.project import Project

class ProjectService:
    """Service for managing projects."""

    def __init__(self):
        self.repository = project_repository

    async def create_project(self, project_in: ProjectCreate) -> ProjectResponse:
        """Create a new project."""
        # Check if project exists
        existing_project = await self.repository.get_project_by_name(project_in.project_name)
        if existing_project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Project '{project_in.project_name}' already exists"
            )
        
        # Determine storage path
        storage_path = os.path.join(AGENTIC_PROJECTS_DIR, project_in.project_name)
        
        # Create project
        new_project = await self.repository.create_project(project_in, storage_path)
        
        return self._map_to_response(new_project)

    async def list_projects(self, skip: int = 0, limit: int = 100) -> List[ProjectResponse]:
        """List all projects."""
        projects = await self.repository.list_projects(skip, limit)
        return [self._map_to_response(p) for p in projects]

    async def get_project(self, project_id: str) -> ProjectResponse:
        """Get a specific project."""
        project = await self.repository.get_project_by_id(project_id)
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        return self._map_to_response(project)
    
    async def get_project_by_name(self, name: str) -> Optional[ProjectResponse]:
        """Get a project by name."""
        project = await self.repository.get_project_by_name(name)
        if not project:
            return None
        return self._map_to_response(project)

    def _map_to_response(self, project: Project) -> ProjectResponse:
        """Map DB model to Pydantic response model."""
        return ProjectResponse(
            id=project.id,
            project_name=project.name,
            description=project.description,
            storage_path=project.storage_path,
            config=project.project_metadata or {},
            created_at=project.created_at,
            updated_at=project.updated_at,
            status="active"
        )

project_service = ProjectService()
