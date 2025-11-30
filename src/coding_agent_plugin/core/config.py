"""Configuration - Load from .env file."""

import os
from pathlib import Path
from dotenv import load_dotenv


_ = load_dotenv()

DATABASE_URL: str | None = os.getenv("DATABASE_URL")
DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"

LLM_BASE_URL: str | None = os.getenv("LLM_BASE_URL")
LLM_MODEL: str | None = os.getenv("LLM_MODEL")
LLM_API_KEY: str | None = os.getenv("LLM_API_KEY")


# Retry Configuration
AGENT_MAX_RETRIES = int(os.getenv("AGENT_MAX_RETRIES", "3"))
AGENT_RETRY_DELAY = int(os.getenv("AGENT_RETRY_DELAY", "2"))  # Seconds

# Project Configuration
AGENTIC_PROJECTS_DIR = os.getenv("AGENTIC_PROJECTS_DIR", str(Path.home() / ".agentic-coder" / "projects"))

# Backend Configuration
BACKEND_SERVER_REQUIRED: bool = os.getenv("BACKEND_SERVER_REQUIRED", "false").lower() == "true"


def validate_llm_config():
    """Validate that LLM configuration is present."""
    missing = []
    if not LLM_API_KEY:
        missing.append("LLM_API_KEY")
    if not LLM_MODEL:
        missing.append("LLM_MODEL")
    if not LLM_BASE_URL:
        # LLM_BASE_URL might be optional depending on provider, but user requested it to be required
        missing.append("LLM_BASE_URL")
        
    if missing:
        raise ValueError(
            f"Missing required environment variables for LLM: {', '.join(missing)}\n"
            "Please set them in your .env file or environment."
        )

def validate_db_config():
    """Validate that Database configuration is present."""
    if not DATABASE_URL:
        raise ValueError(
            "Missing required environment variable: DATABASE_URL\n"
            "Please set it in your .env file or environment."
        )
