"""Base agent class for agent orchestration."""

from typing import Any, Dict
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Base class for all agents."""

    def __init__(self, name: str, openapi_instance: Any = None):
        self.name = name
        self.openapi_instance = openapi_instance

    @abstractmethod
    async def execute(self, task: Any) -> Dict[str, Any]:
        """Execute the agent's task."""
        pass

    def log(self, message: str) -> None:
        """Log a message."""
        print(f"[{self.name}] {message}")

    async def retry_operation(self, func, *args, **kwargs):
        """Execute an operation with retry logic."""
        from coding_agent_plugin.core.config import AGENT_MAX_RETRIES, AGENT_RETRY_DELAY
        from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
        import openai
        
        # Define retry strategy
        @retry(
            stop=stop_after_attempt(AGENT_MAX_RETRIES),
            wait=wait_exponential(multiplier=AGENT_RETRY_DELAY, min=AGENT_RETRY_DELAY, max=10),
            retry=retry_if_exception_type((
                openai.RateLimitError,
                openai.APIConnectionError,
                openai.InternalServerError,
                TimeoutError
            )),
            reraise=True
        )
        async def _execute():
            return await func(*args, **kwargs)
            
        return await _execute()
