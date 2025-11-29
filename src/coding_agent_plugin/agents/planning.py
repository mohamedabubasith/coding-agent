"""Planning agent for task planning and workflow design using LangChain."""

from typing import List, Dict, Any
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .base_agent import BaseAgent


class PlanningAgent(BaseAgent):
    """Agent responsible for task planning and workflow design."""

    def __init__(self, name: str, openapi_instance: Any = None):
        super().__init__(name, openapi_instance)
        self.model = ChatOpenAI(model="gpt-4o", temperature=0.2)

    async def execute(self, task: str) -> Dict[str, Any]:
        """Execute the planning task."""
        self.log(f"Executing planning task: {task}")
        workflow = await self.plan(task)
        return {"workflow": workflow}

    async def plan(self, user_input: str) -> List[Dict[str, str]]:
        """Plan the workflow for the user's input using LangChain."""
        self.log(f"Planning workflow for: {user_input}")
        system_prompt = SystemMessage(content="You are a planning agent responsible for breaking down tasks into sub-tasks.")
        input_prompt = HumanMessage(content=f"Break down the following task into sub-tasks: {user_input}")

        # Create the agent
        agent = create_agent(
            model=self.model,
            tools=[],
            system_prompt=system_prompt,
            middleware=[],
            response_format=None,
        )

        # Run the agent with the input prompt
        inputs = {"messages": [input_prompt]}
        result = ""
        for chunk in agent.stream(inputs, stream_mode="updates"):
            result += chunk.get("content", "")

        # Example response parsing (adjust based on your LLM response format)
        sub_tasks = [
            {"task": "Write code for feature X", "agent": "coding"},
            {"task": "Fix any errors in the code", "agent": "error_fixing"},
            {"task": "Execute and test the code", "agent": "execution"},
        ]
        return sub_tasks
