"""Tests for Pydantic models."""

import pytest

from coding_agent_plugin.models.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
)


def test_project_create_valid():
    """Test creating a valid ProjectCreate model."""
    project = ProjectCreate(
        project_name="Valid Project",
        description="A valid project",
        config={"key": "value"},
    )

    assert project.project_name == "Valid Project"
    assert project.description == "A valid project"
    assert project.config == {"key": "value"}


def test_project_create_minimal():
    """Test creating a ProjectCreate with minimal data."""
    project = ProjectCreate(project_name="Minimal")

    assert project.project_name == "Minimal"
    assert project.description is None
    assert project.config is None


def test_project_create_empty_name():
    """Test that empty project name is allowed (no Field constraints)."""
    # Without Field constraints, empty strings are valid
    project = ProjectCreate(project_name="")
    assert project.project_name == ""


def test_project_create_name_long():
    """Test that long project names are allowed (no Field constraints)."""
    # Without Field constraints, long strings are valid
    long_name = "x" * 1000
    project = ProjectCreate(project_name=long_name)
    assert project.project_name == long_name


def test_project_update_partial():
    """Test partial update model."""
    update = ProjectUpdate(project_name="Updated Name")

    assert update.project_name == "Updated Name"
    assert update.description is None
    assert update.config is None
    assert update.status is None


def test_project_update_exclude_unset():
    """Test that unset fields are excluded from model_dump."""
    update = ProjectUpdate(project_name="Only Name")
    data = update.model_dump(exclude_unset=True)

    assert data == {"project_name": "Only Name"}
    assert "description" not in data
    assert "config" not in data


def test_project_create_with_all_fields():
    """Test creating ProjectCreate with all fields."""
    project = ProjectCreate(
        project_name="Full Project",
        description="Complete description",
        config={"env": "prod", "debug": False},
    )

    assert project.project_name == "Full Project"
    assert project.description == "Complete description"
    assert project.config == {"env": "prod", "debug": False}


def test_project_update_all_fields():
    """Test updating all fields."""
    update = ProjectUpdate(
        project_name="New Name",
        description="New Description",
        config={"updated": True},
        status="inactive",
    )

    assert update.project_name == "New Name"
    assert update.description == "New Description"
    assert update.config == {"updated": True}
    assert update.status == "inactive"
