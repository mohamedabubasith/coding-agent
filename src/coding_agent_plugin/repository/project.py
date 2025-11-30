from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from coding_agent_plugin.core.database import db_manager
from coding_agent_plugin.schemas.project import Project
from coding_agent_plugin.models.project import ProjectCreate

class ProjectRepository:
    """Repository for Project database operations."""

    async def create_project(self, project_data: ProjectCreate, storage_path: str) -> Project:
        """Create a new project in the database."""
        async with db_manager.session_factory() as session:
            new_project = Project(
                name=project_data.project_name,
                description=project_data.description,
                storage_path=storage_path,
                project_metadata=project_data.config
            )
            session.add(new_project)
            await session.commit()
            await session.refresh(new_project)
            return new_project

    async def get_project_by_name(self, name: str) -> Optional[Project]:
        """Get a project by name."""
        async with db_manager.session_factory() as session:
            stmt = select(Project).where(Project.name == name)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Get a project by ID."""
        async with db_manager.session_factory() as session:
            stmt = select(Project).where(Project.id == project_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def list_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """List all projects."""
        async with db_manager.session_factory() as session:
            stmt = select(Project).offset(skip).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()

project_repository = ProjectRepository()
