"""Service for handling LLM calls."""

from httpx._models import Response
from typing import Any
import httpx
from ..core.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL


class LLMService:
    """Service for handling LLM calls."""

    url: str
    model: str
    api_key: str

    def __init__(self) -> None:
        if not LLM_BASE_URL:
            raise ValueError("LLM_BASE_URL not configured")
        if not LLM_API_KEY:
            raise ValueError("LLM_API_KEY not configured")
        if not LLM_MODEL:
            raise ValueError("LLM_MODEL not configured")
        self.url = LLM_BASE_URL
        self.model = LLM_MODEL
        self.api_key = LLM_API_KEY

    async def call_llm(self, prompt: str) -> dict[str, Any]:
        """Call the LLM with the given prompt."""
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data: dict[str, str] = {
            "model": self.model,
            "prompt": prompt,
        }
        async with httpx.AsyncClient() as client:
            response: Response = await client.post(self.url, headers=headers, json=data)
            _ = response.raise_for_status()
            result = response.json()
            # Example token count (adjust based on your LLM response format)
            tokens_used = result.get("usage", {}).get("total_tokens", 0)
            return {
                "response": result,
                "tokens_used": tokens_used,
            }
