"""Integration test configuration - real PostgreSQL."""

import asyncio
import os
from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from coding_agent_plugin.schemas.project import Base


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL not set! Set it in .env or environment variable.\n"
        "Example: DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/coding_agent"
    )


@pytest.fixture(scope="session")
def event_loop():
    """Use the default event loop."""
    loop = asyncio.get_event_loop()
    yield loop


@pytest.fixture(scope="session")
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    """Real async engine against PostgreSQL."""
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_size=1,
        max_overflow=0,
        pool_pre_ping=False,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Real DB session, rolled back and closed per test."""
    factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    async with factory() as sess:
        try:
            yield sess
        finally:
            await sess.rollback()
            await sess.close()
