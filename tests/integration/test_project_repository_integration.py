"""Integration tests for ProjectRepository with real PostgreSQL."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from coding_agent_plugin.repositories.project import ProjectRepository
from coding_agent_plugin.schemas.project import ProjectSchema


@pytest.mark.asyncio
async def test_create_and_get_project(session: AsyncSession):
    repo = ProjectRepository(session)

    data = {
        "id": "int-test-1",
        "project_name": "Integration Project",
        "description": "Repo integration test",
        "config": {"k": "v"},
    }

    created = await repo.create(data)
    await session.commit()

    assert isinstance(created, ProjectSchema)
    assert created.id == "int-test-1"

    fetched = await repo.get_by_id("int-test-1")
    assert fetched is not None
    assert fetched.project_name == "Integration Project"
    assert fetched.config == {"k": "v"}


@pytest.mark.asyncio
async def test_update_and_delete_project(session: AsyncSession):
    repo = ProjectRepository(session)

    created = await repo.create(
        {
            "id": "int-test-2",
            "project_name": "Before",
            "description": None,
            "config": {},
        }
    )
    await session.commit()

    updated = await repo.update(
        "int-test-2",
        {"project_name": "After", "description": "Updated"},
    )
    await session.commit()

    assert updated is not None
    assert updated.project_name == "After"
    assert updated.description == "Updated"

    deleted = await repo.delete("int-test-2")
    await session.commit()

    assert deleted is True
    assert await repo.get_by_id("int-test-2") is None
