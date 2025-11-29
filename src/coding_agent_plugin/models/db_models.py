"""SQLAlchemy database models for agentic-coder."""

from sqlalchemy import Column, String, Integer, Text, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()


class Project(Base):
    """Project model for database storage."""
    
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text)
    storage_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    project_metadata = Column(JSON, default=dict)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "storage_path": self.storage_path,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "project_metadata": self.project_metadata or {}
        }


class ProjectFile(Base):
    """Project file tracking model."""
    
    __tablename__ = "project_files"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String, nullable=False)
    content_hash = Column(String)
    size_bytes = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class ProjectVersion(Base):
    """Project version history model."""
    
    __tablename__ = "project_versions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    version = Column(Integer, nullable=False)
    description = Column(Text)
    changes = Column(JSON)
    created_at = Column(DateTime, default=func.now())


class UserSettings(Base):
    """User settings storage model."""
    
    __tablename__ = "user_settings"
    
    key = Column(String, primary_key=True)
    value = Column(Text, nullable=False)
