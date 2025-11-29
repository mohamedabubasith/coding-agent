"""Project repository for database operations."""

from sqlalchemy.engine.result import Result
from coding_agent_plugin.schemas.project import ProjectSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.project import ProjectCreate, ProjectUpdate


class ProjectRepository:
    """Repository for project data access."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, project_data: ProjectCreate) -> ProjectSchema:
        """
        Create a new project in database.

        Args:
            project_data: ProjectCreate pydantic model

        Returns:
            Created ProjectSchema instance
        """
        project: ProjectSchema = ProjectSchema(
            project_name=project_data.project_name,
            description=project_data.description,
            config=project_data.config or {},
        )
        self.session.add(instance=project)
        await self.session.flush()
        await self.session.refresh(instance=project)
        return project

    async def get_by_id(self, project_id: int) -> ProjectSchema | None:
        """Get project by ID."""
        result: Result[tuple[ProjectSchema]] = await self.session.execute(
            select(ProjectSchema).where(ProjectSchema.id == project_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, project_name: str) -> ProjectSchema | None:
        """Get project by name."""
        result: Result[tuple[ProjectSchema]] = await self.session.execute(
            select(ProjectSchema).where(ProjectSchema.project_name == project_name)
        )
        return result.scalar_one_or_none()

    async def list_all(self) -> list[ProjectSchema]:
        """List all projects."""
        result: Result[tuple[ProjectSchema]] = await self.session.execute(
            select(ProjectSchema)
        )
        return list(result.scalars().all())

    async def update(
        self, project_id: int, update_data: ProjectUpdate
    ) -> ProjectSchema | None:
        """Update project by ID."""
        project: ProjectSchema | None = await self.get_by_id(project_id)
        if not project:
            return None

        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(project, key, value)

        await self.session.flush()
        await self.session.refresh(instance=project)
        return project

    async def delete(self, project_id: int) -> bool:
        """Delete project by ID."""
        project: ProjectSchema | None = await self.get_by_id(project_id)
        if not project:
            return False

        await self.session.delete(instance=project)
        await self.session.flush()
        return True
