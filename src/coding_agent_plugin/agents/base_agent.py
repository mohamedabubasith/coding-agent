"""Base agent class for agent orchestration."""

from typing import Any, Dict
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Base class for all agents."""

    def __init__(self, name: str, openapi_instance: Any = None):
        self.name = name
        self.openapi_instance = openapi_instance

    @abstractmethod
    async def execute(self, task: str) -> Dict[str, Any]:
        """Execute the agent's task."""
        pass

    def log(self, message: str) -> None:
        """Log a message."""
        print(f"[{self.name}] {message}")
