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
        from coding_agent_plugin.core.config import LLM_MODEL, LLM_BASE_URL, LLM_API_KEY
        model_name = LLM_MODEL or "gpt-4o"
        
        # Set up ChatOpenAI with custom base_url and api_key if using NVIDIA or other providers
        kwargs = {"model": model_name, "temperature": 0.2}
        if LLM_API_KEY:
            kwargs["api_key"] = LLM_API_KEY
        if LLM_BASE_URL:
            kwargs["base_url"] = LLM_BASE_URL
            
        self.model = ChatOpenAI(**kwargs)

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the planning task."""
        user_prompt = task.get("user_prompt")
        project_id = task.get("project_id")

        if not user_prompt or not project_id:
            raise ValueError("Missing user_prompt or project_id")

        self.log(f"Executing planning task: {user_prompt}")
        workflow = await self.plan(user_prompt)
        
        self.save_plan(project_id, workflow)
        
        return {"workflow": workflow}

    async def plan(self, user_input: str) -> Dict[str, Any]:
        """Plan the workflow for the user's input using LangChain."""
        self.log(f"Planning workflow for: {user_input}")
        
        system_prompt = SystemMessage(content="""You are a software architect. Create a comprehensive plan for the user's request.
        Return a JSON object with the following structure:
        {
            "architecture": {
                "component_name": ["file1", "file2"]
            },
            "tasks": [
                {
                    "id": 1,
                    "phase": "scaffold|coding|verification",
                    "description": "Task description",
                    "agent": "task|coding|execution",
                    "details": {
                        "action": "create_dirs", 
                        "paths": ["dir1"],
                        "file_path": "path/to/file",
                        "prompt": "Instructions for coding agent",
                        "command": "Shell command for execution agent"
                    }
                }
            ]
        }
        Ensure the plan is detailed and covers scaffolding, coding, and verification.
        IMPORTANT: Return ONLY the JSON object. Do not include any markdown formatting or explanation.
        """)
        input_prompt = HumanMessage(content=f"Request: {user_input}")
        
        messages = [system_prompt, input_prompt]
        
        response = await self.model.ainvoke(messages)
        content = response.content
        
        import json
        import re
        
        # Robust JSON extraction
        try:
            # Find the first { and the last }
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                json_str = match.group(0)
                plan = json.loads(json_str)
                return plan
            else:
                raise ValueError("No JSON object found in response")
                
        except (json.JSONDecodeError, ValueError) as e:
            self.log(f"Failed to decode JSON plan: {e}")
            # Save raw content for debugging
            # We can't pass project_id here easily without changing signature, 
            # but the orchestrator calls save_plan later.
            # We will return a special error dict that save_plan can recognize, or just empty.
            # Better: return a dict with a "error" key and "raw_content"
            return {"error": str(e), "raw_content": content, "architecture": {}, "tasks": []}

    def save_plan(self, project_id: str, workflow: Dict[str, Any]) -> None:
        """Save planning details to a file."""
        import os
        directory = f"projects/{project_id}/.agent_context"
        os.makedirs(directory, exist_ok=True)
        
        file_path = os.path.join(directory, "planning.md")
        
        with open(file_path, "w") as f:
            f.write("# Project Plan\n\n")
            
            if "error" in workflow:
                f.write("## ⚠️ Planning Error\n\n")
                f.write(f"**Error**: {workflow['error']}\n\n")
                f.write("### Raw LLM Output\n\n")
                f.write("```\n")
                f.write(workflow.get("raw_content", ""))
                f.write("\n```\n")
                return

            f.write("## Architecture\n")
            for component, files in workflow.get("architecture", {}).items():
                f.write(f"- **{component}**\n")
                for file in files:
                    f.write(f"  - {file}\n")
            
            f.write("\n## Tasks\n")
            for task in workflow.get("tasks", []):
                f.write(f"- **{task['description']}** (Agent: {task['agent']})\n")
                if "details" in task:
                    f.write(f"  - Details: {task['details']}\n")
