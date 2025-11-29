"""SQLAlchemy database schemas."""

from datetime import datetime, timezone
from typing import Any
from sqlalchemy import Column, String, DateTime, Text, JSON, Integer
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class ProjectSchema(Base):
    """Database schema for projects."""

    __tablename__: str = "projects"

    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True, index=True)
    project_name: Column[str] = Column(String(length=255), nullable=False, index=True)
    description: Column[str] = Column(Text, nullable=True)
    config: Column[Any] = Column(JSON, nullable=False, default=dict)
    created_at: Column[datetime] = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=timezone.utc),
    )
    updated_at: Column[datetime] = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=timezone.utc),
        onupdate=lambda: datetime.now(tz=timezone.utc),
    )
    status: Column[str] = Column(String(length=50), nullable=False, default="active")

    def __repr__(self) -> str:
        return f"<ProjectSchema(id={self.id}, name='{self.project_name}')>"
