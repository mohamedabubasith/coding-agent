"""Orchestration agent for routing tasks to other agents."""

from coding_agent_plugin.agents.planning import PlanningAgent
from typing import Dict, Any
from .coding import CodingAgent


class OrchestratorAgent:
    """Agent responsible for orchestrating tasks to other agents."""

    def __init__(self) -> None:
        self.agents = {
            "planning": PlanningAgent(name="planning"),
            "coding": CodingAgent(name="coding"),
        }

    async def execute(self, mode: str, user_prompt: str) -> Dict[str, Any]:
        """Execute the task based on the mode."""
        if mode not in self.agents:
            raise ValueError(f"Unsupported mode: {mode}")

        agent: PlanningAgent | Any = self.agents[mode]
        return await agent.execute(user_prompt)
