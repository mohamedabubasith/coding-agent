"""Project service for business logic."""

from coding_agent_plugin.schemas.project import ProjectSchema
from coding_agent_plugin.repositories.project import ProjectRepository
from ..core.database import db_manager
from ..models.project import ProjectCreate, ProjectUpdate, ProjectResponse


class ProjectService:
    """Service for project business logic."""

    @staticmethod
    async def create(project_data: ProjectCreate) -> ProjectResponse:
        """
        Create a new project.

        Args:
            project_data: ProjectCreate pydantic model

        Returns:
            ProjectResponse with created project
        """
        async with db_manager.get_session() as session:
            repo: ProjectRepository = ProjectRepository(session)

            # Create in database
            project_schema: ProjectSchema = await repo.create(project_data=project_data)

            # Convert to response model
            return ProjectResponse(**project_schema.__dict__)

    @staticmethod
    async def get_by_id(project_id: int) -> ProjectResponse | None:
        """Get project by ID."""
        async with db_manager.get_session() as session:
            repo: ProjectRepository = ProjectRepository(session)
            project_schema: ProjectSchema | None = await repo.get_by_id(project_id)

            if not project_schema:
                return None

            return ProjectResponse(**project_schema.__dict__)

    @staticmethod
    async def get_by_name(project_name: str) -> ProjectResponse | None:
        """Get project by name."""
        async with db_manager.get_session() as session:
            repo: ProjectRepository = ProjectRepository(session)
            project_schema: ProjectSchema | None = await repo.get_by_name(project_name)

            if not project_schema:
                return None

            return ProjectResponse(**project_schema.__dict__)

    @staticmethod
    async def list_all() -> list[ProjectResponse]:
        """List all projects."""
        async with db_manager.get_session() as session:
            repo: ProjectRepository = ProjectRepository(session)
            projects: list[ProjectSchema] = await repo.list_all()

            return [ProjectResponse(**project.__dict__) for project in projects]

    @staticmethod
    async def update(
        project_id: int, update_data: ProjectUpdate
    ) -> ProjectResponse | None:
        """Update project."""
        async with db_manager.get_session() as session:
            repo: ProjectRepository = ProjectRepository(session)

            project_schema: ProjectSchema | None = await repo.update(
                project_id, update_data=update_data
            )

            if not project_schema:
                return None

            return ProjectResponse(**project_schema.__dict__)

    @staticmethod
    async def delete(project_id: int) -> bool:
        """Delete project."""
        async with db_manager.get_session() as session:
            repo: ProjectRepository = ProjectRepository(session)
            return await repo.delete(project_id)
