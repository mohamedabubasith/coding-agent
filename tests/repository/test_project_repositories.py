"""Tests for repositories."""

from unittest.mock import AsyncMock, MagicMock, patch, call
import pytest

from coding_agent_plugin.repositories.project import ProjectRepository
from coding_agent_plugin.schemas.project import ProjectSchema


@pytest.fixture
def mock_session():
    """Create a mock AsyncSession."""
    session = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def mock_project():
    """Create a mock ProjectSchema."""
    project = MagicMock(spec=ProjectSchema)
    project.id = "test-id-123"
    project.project_name = "Test Project"
    project.description = "Test Description"
    project.config = {"test": True}
    project.status = "active"
    return project


@pytest.mark.asyncio
async def test_repository_create_async(mock_session, mock_project):
    """Test creating a project through repository (async)."""
    repo = ProjectRepository(mock_session)

    with patch(
        "coding_agent_plugin.repositories.project.ProjectSchema",
        return_value=mock_project,
    ):
        project_data = {
            "id": "test-id-123",
            "project_name": "Test Project",
        }

        result = await repo.create(project_data)

        assert result == mock_project
        # session.add was called
        assert mock_session.add.call_count == 1
        # flush and refresh were awaited
        mock_session.flush.assert_awaited_once()
        mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_repository_get_by_id(mock_session, mock_project):
    """Test retrieving a project by ID."""
    repo = ProjectRepository(mock_session)

    # Mock execute result
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_project
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await repo.get_by_id("test-id-123")

    assert result == mock_project
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_repository_get_by_id_not_found(mock_session):
    """Test retrieving a non-existent project."""
    repo = ProjectRepository(mock_session)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await repo.get_by_id("non-existent")

    assert result is None


@pytest.mark.asyncio
async def test_repository_get_by_name(mock_session, mock_project):
    """Test retrieving a project by name."""
    repo = ProjectRepository(mock_session)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_project
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await repo.get_by_name("Test Project")

    assert result == mock_project


@pytest.mark.asyncio
async def test_repository_list_all(mock_session):
    """Test listing all projects."""
    repo = ProjectRepository(mock_session)

    mock_projects = [MagicMock(spec=ProjectSchema) for _ in range(3)]
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = mock_projects
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await repo.list_all()

    assert len(result) == 3


@pytest.mark.asyncio
async def test_repository_update(mock_session, mock_project):
    """Test updating a project."""
    repo = ProjectRepository(mock_session)

    # Mock get_by_id
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_project
    mock_session.execute = AsyncMock(return_value=mock_result)

    update_data = {"project_name": "Updated Name"}
    result = await repo.update("test-id-123", update_data)

    assert result == mock_project
    mock_session.flush.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_repository_update_not_found(mock_session):
    """Test updating a non-existent project."""
    repo = ProjectRepository(mock_session)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await repo.update("non-existent", {"project_name": "New"})

    assert result is None


@pytest.mark.asyncio
async def test_repository_delete(mock_session, mock_project):
    """Test deleting a project."""
    repo = ProjectRepository(mock_session)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_project
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await repo.delete("test-id-123")

    assert result is True
    # Check delete was awaited
    assert mock_session.delete.call_count == 1
    mock_session.flush.assert_awaited_once()


@pytest.mark.asyncio
async def test_repository_delete_not_found(mock_session):
    """Test deleting a non-existent project."""
    repo = ProjectRepository(mock_session)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await repo.delete("non-existent")

    assert result is False
