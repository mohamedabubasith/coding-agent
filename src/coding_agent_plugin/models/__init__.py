"""Pydantic models for project data validation."""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Any


class ProjectCreate(BaseModel):
    """Model for creating a new project."""

    project_name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    config: dict[str, Any] | None = None


class ProjectUpdate(BaseModel):
    """Model for updating a project."""

    project_name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    config: dict[str, Any] | None = None
    status: str | None = None


class ProjectResponse(BaseModel):
    """Model for project response."""

    id: UUID
    project_name: str
    description: str | None
    config: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    status: str
