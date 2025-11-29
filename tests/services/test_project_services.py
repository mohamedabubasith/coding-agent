"""Tests for services."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from coding_agent_plugin.models.project import ProjectCreate, ProjectResponse
from coding_agent_plugin.services.project import ProjectService


@pytest.mark.asyncio
async def test_create_project_service():
    """Test creating a project through service."""
    project_data = ProjectCreate(
        project_name="Service Test",
        description="Testing service layer",
        config={"env": "test"},
    )

    # Create expected response
    expected_response = ProjectResponse(
        id="service-test-1",
        project_name="Service Test",
        description="Testing service layer",
        config={"env": "test"},
        status="active",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    mock_schema = MagicMock()

    with patch("coding_agent_plugin.services.project.db_manager") as mock_db:
        with patch(
            "coding_agent_plugin.services.project.ProjectRepository"
        ) as mock_repo_class:
            with patch(
                "coding_agent_plugin.services.project.ProjectResponse.model_validate",
                return_value=expected_response,
            ):
                # Setup context manager
                mock_session = MagicMock()
                mock_context = MagicMock()
                mock_context.__aenter__ = AsyncMock(return_value=mock_session)
                mock_context.__aexit__ = AsyncMock(return_value=None)
                mock_db.get_session.return_value = mock_context

                # Setup repository
                mock_repo = MagicMock()
                mock_repo.create = AsyncMock(return_value=mock_schema)
                mock_repo_class.return_value = mock_repo

                # Call service
                result = await ProjectService.create(project_data)

                # Assertions
                assert isinstance(result, ProjectResponse)
                assert result.project_name == "Service Test"
                assert result.description == "Testing service layer"
                mock_repo.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_project_with_empty_config():
    """Test creating a project with None config defaults to empty dict."""
    expected_response = ProjectResponse(
        id="config-test-1",
        project_name="Empty Config Test",
        description=None,
        config={},
        status="active",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    mock_schema = MagicMock()

    project_data = ProjectCreate(
        project_name="Empty Config Test",
        config=None,
    )

    with patch("coding_agent_plugin.services.project.db_manager") as mock_db:
        with patch(
            "coding_agent_plugin.services.project.ProjectRepository"
        ) as mock_repo_class:
            with patch(
                "coding_agent_plugin.services.project.ProjectResponse.model_validate",
                return_value=expected_response,
            ):
                mock_session = MagicMock()
                mock_context = MagicMock()
                mock_context.__aenter__ = AsyncMock(return_value=mock_session)
                mock_context.__aexit__ = AsyncMock(return_value=None)
                mock_db.get_session.return_value = mock_context

                mock_repo = MagicMock()
                mock_repo.create = AsyncMock(return_value=mock_schema)
                mock_repo_class.return_value = mock_repo

                result = await ProjectService.create(project_data)

                assert result.config == {}


@pytest.mark.asyncio
async def test_get_project_by_id():
    """Test getting project by ID."""
    expected_response = ProjectResponse(
        id="service-test-1",
        project_name="Service Test",
        description="Testing",
        config={},
        status="active",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    mock_schema = MagicMock()

    with patch("coding_agent_plugin.services.project.db_manager") as mock_db:
        with patch(
            "coding_agent_plugin.services.project.ProjectRepository"
        ) as mock_repo_class:
            with patch(
                "coding_agent_plugin.services.project.ProjectResponse.model_validate",
                return_value=expected_response,
            ):
                mock_session = MagicMock()
                mock_context = MagicMock()
                mock_context.__aenter__ = AsyncMock(return_value=mock_session)
                mock_context.__aexit__ = AsyncMock(return_value=None)
                mock_db.get_session.return_value = mock_context

                mock_repo = MagicMock()
                mock_repo.get_by_id = AsyncMock(return_value=mock_schema)
                mock_repo_class.return_value = mock_repo

                result = await ProjectService.get_by_id("service-test-1")

                assert result is not None
                assert result.id == "service-test-1"


@pytest.mark.asyncio
async def test_get_project_by_id_not_found():
    """Test getting non-existent project."""
    with patch("coding_agent_plugin.services.project.db_manager") as mock_db:
        with patch(
            "coding_agent_plugin.services.project.ProjectRepository"
        ) as mock_repo_class:
            mock_session = MagicMock()
            mock_context = MagicMock()
            mock_context.__aenter__ = AsyncMock(return_value=mock_session)
            mock_context.__aexit__ = AsyncMock(return_value=None)
            mock_db.get_session.return_value = mock_context

            mock_repo = MagicMock()
            mock_repo.get_by_id = AsyncMock(return_value=None)
            mock_repo_class.return_value = mock_repo

            result = await ProjectService.get_by_id("non-existent")

            assert result is None


@pytest.mark.asyncio
async def test_list_all_projects():
    """Test listing all projects."""
    expected_responses = [
        ProjectResponse(
            id=f"project-{i}",
            project_name=f"Project {i}",
            description=None,
            config={},
            status="active",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        for i in range(3)
    ]

    mock_schemas = [MagicMock() for _ in range(3)]

    with patch("coding_agent_plugin.services.project.db_manager") as mock_db:
        with patch(
            "coding_agent_plugin.services.project.ProjectRepository"
        ) as mock_repo_class:
            with patch(
                "coding_agent_plugin.services.project.ProjectResponse.model_validate",
                side_effect=expected_responses,
            ):
                mock_session = MagicMock()
                mock_context = MagicMock()
                mock_context.__aenter__ = AsyncMock(return_value=mock_session)
                mock_context.__aexit__ = AsyncMock(return_value=None)
                mock_db.get_session.return_value = mock_context

                mock_repo = MagicMock()
                mock_repo.list_all = AsyncMock(return_value=mock_schemas)
                mock_repo_class.return_value = mock_repo

                result = await ProjectService.list_all()

                assert len(result) == 3
                assert all(isinstance(r, ProjectResponse) for r in result)
