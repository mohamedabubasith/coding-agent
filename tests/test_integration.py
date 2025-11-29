"""Integration tests for the main API."""

from unittest.mock import AsyncMock, patch
import pytest

from coding_agent_plugin import setup, create


@pytest.mark.asyncio
async def test_setup_without_database_url():
    """Test setup fails without DATABASE_URL."""
    with patch("coding_agent_plugin.db_manager") as mock_db:
        mock_db.setup = AsyncMock(side_effect=ValueError("DATABASE_URL not found!"))

        with pytest.raises(ValueError, match="DATABASE_URL not found"):
            await setup()


@pytest.mark.asyncio
async def test_setup_success():
    """Test successful setup."""
    with patch("coding_agent_plugin.db_manager") as mock_db:
        mock_db.setup = AsyncMock()

        await setup()

        mock_db.setup.assert_called_once()


@pytest.mark.asyncio
async def test_create_project_integration():
    """Test creating a project through main API."""
    from datetime import datetime, timezone

    mock_response = type(
        "MockResponse",
        (),
        {
            "id": "integration-test-1",
            "project_name": "Integration Test",
            "description": "Test description",
            "config": {"test": True},
            "status": "active",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
    )()

    with patch("coding_agent_plugin.db_manager") as mock_db:
        with patch("coding_agent_plugin.ProjectService") as mock_service:
            mock_db.setup = AsyncMock()
            mock_service.create = AsyncMock(return_value=mock_response)

            result = await create(
                project_name="Integration Test",
                description="Test description",
                config={"test": True},
            )

            assert result.project_name == "Integration Test"
            assert result.description == "Test description"
            mock_db.setup.assert_called_once()
