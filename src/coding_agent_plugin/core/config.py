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

def validate_llm_config() -> None:
    """
    Validate that required LLM configuration is present.
    
    Raises:
        ValueError: If LLM_API_KEY is missing
    """
    if not LLM_API_KEY:
        raise ValueError(
            "LLM_API_KEY is required but not set.\n\n"
            "Please set it in your .env file:\n"
            "  LLM_API_KEY=your_api_key_here\n\n"
            "Or export it as an environment variable:\n"
            "  export LLM_API_KEY=your_api_key_here"
        )
