from typing import Any, Dict
from coding_agent_plugin.agents.orchestrator import OrchestratorAgent

class AgentService:
    """Service for managing agent execution."""

    def __init__(self):
        # Singleton orchestrator instance
        self.orchestrator = OrchestratorAgent()

    async def run_agent(self, mode: str, prompt: str, project_id: str) -> Dict[str, Any]:
        """Run the agent."""
        return await self.orchestrator.execute(
            mode=mode,
            user_prompt=prompt,
            project_id=project_id
        )

agent_service = AgentService()
