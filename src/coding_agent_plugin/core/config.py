"""Configuration - Load from .env file."""

import os
from dotenv import load_dotenv

from coding_agent_plugin.services.llm_service import LLMService

_ = load_dotenv()

DATABASE_URL: str | None = os.getenv("DATABASE_URL")
DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"

LLM_BASE_URL: str | None = os.getenv("LLM_BASE_URL")
LLM_MODEL: str | None = os.getenv("LLM_MODEL")
LLM_API_KEY: str | None = os.getenv("LLM_API_KEY")
