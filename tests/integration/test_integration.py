"""Real-world integration test for setup() and create()."""

import asyncio
import os
from coding_agent_plugin import setup, create


async def main():
    # Set the DATABASE_URL environment variable
    os.environ["DATABASE_URL"] = (
        "postgresql+asyncpg://admin:admin@localhost:5432/coding_agent"
    )

    # Initialize the database
    await setup()

    # Create a project
    project = await create(
        project_name="Integration Test",
        description="This is a real-world integration test",
        config={"mode": "test"},
    )

    print(f"Project created: {project}")


if __name__ == "__main__":
    asyncio.run(main())
