"""Coding Agent Plugin - Multi-agent orchestration for code generation."""

__version__ = "0.1.0"

from typing import Any

from .core.database import db_manager

async def setup() -> None:
    """
    Initialize the database.

    Raises:
        ValueError: If DATABASE_URL not configured
    """
    await db_manager.setup()
