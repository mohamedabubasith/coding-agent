"""Coding Agent Plugin - Multi-agent orchestration for code generation."""

__version__ = "0.1.0"

from typing import Any

from .core.database import db_manager
from .services.project import ProjectService
from .models.project import ProjectCreate, ProjectResponse


async def setup() -> None:
    """
    Initialize the database.

    Raises:
        ValueError: If DATABASE_URL not configured
    """
    await db_manager.setup()


async def create(
    project_name: str,
    description: str | None = None,
    config: dict[str, Any] | None = None,
) -> ProjectResponse:
    """
    Create a new coding project.

    Args:
        project_name: Name of the project
        description: Optional description
        config: Optional configuration dict

    Returns:
        ProjectResponse with id, created_at, etc.

    Raises:
        ValueError: If DATABASE_URL not configured

    Example:
        >>> project = await create(project_name="Test")
        >>> print(project.id)
        >>> print(project.project_name)
    """
    await db_manager.setup()

    project_data: ProjectCreate = ProjectCreate(
        project_name=project_name,
        description=description,
        config=config,
    )

    return await ProjectService.create(project_data)
