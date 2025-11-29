"""Database connection and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool
from pathlib import Path
from contextlib import contextmanager
import os

from coding_agent_plugin.models.db_models import Base


# Database configuration
AGENTIC_HOME = Path.home() / ".agentic-coder"
DATABASE_PATH = AGENTIC_HOME / "data.db"

# Ensure directory exists
AGENTIC_HOME.mkdir(parents=True, exist_ok=True)

# Create engine
engine = create_engine(
    f"sqlite:///{DATABASE_PATH}",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

# Create session factory
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db_session():
    """Get database session context manager."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db():
    """Get database session (for dependency injection)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
