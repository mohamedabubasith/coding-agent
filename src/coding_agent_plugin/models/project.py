"""Pydantic models for project data validation."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel


class ProjectCreate(BaseModel):
    """Model for creating a new project."""

    project_name: str
    description: str | None = None
    config: dict[str, Any] | None = None


class ProjectUpdate(BaseModel):
    """Model for updating a project."""

    project_name: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None
    status: str | None = None


class ProjectResponse(BaseModel):
    """Model for project response."""

    id: int
    project_name: str
    description: str | None
    config: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    status: str
