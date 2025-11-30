"""Planning agent for task planning and workflow design using LangChain."""

from typing import List, Dict, Any
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .base_agent import BaseAgent


class PlanningAgent(BaseAgent):
    """Agent responsible for task planning and workflow design."""

    def __init__(self, name: str = "planning", model: str = None):
        super().__init__(name, model)
        from coding_agent_plugin.managers import ProjectManager
        self.pm = ProjectManager()
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

        await self.audit.log_event(
            event_type="planning_start",
            data={"user_prompt": user_prompt},
            project_id=project_id
        )

        self.log(f"Executing planning task: {user_prompt}")
        
        # Get existing files
        existing_files = self.pm.list_files(project_id)
        
        workflow = await self.plan(user_prompt, existing_files)
        
        self.save_plan(project_id, workflow)
        
        await self.audit.log_event(
            event_type="planning_complete",
            data={"workflow_tasks": len(workflow.get("tasks", []))},
            project_id=project_id
        )
        
        return {"workflow": workflow}

    async def plan(self, user_input: str, existing_files: List[str] = None) -> Dict[str, Any]:
        """Plan the workflow for the user's input using LangChain."""
        self.log(f"Planning workflow for: {user_input}")
        
        files_context = ""
        if existing_files:
            files_context = f"\nExisting Project Files:\n{', '.join(existing_files)}\n"
            files_context += """
IMPORTANT GUIDELINES FOR EXISTING PROJECTS:
1. ANALYZE the existing file structure and naming conventions carefully.
2. FOLLOW the established patterns for new modules (e.g., if 'routers.py' is used for routes in one module, use 'routers.py' for new modules too).
3. DO NOT create redundant files if shared utilities already exist (e.g., use existing database/crud.py if applicable).
4. INTEGRATE new files seamlessly into the existing architecture (e.g., ensure main.py imports new routers correctly).
5. MAINTAIN consistency in coding style and structure.
"""
        
        from coding_agent_plugin.services.prompt_service import PromptService
        system_prompt = SystemMessage(content=PromptService.get_planning_system_prompt(files_context))
        input_prompt = HumanMessage(content=f"Request: {user_input}")
        
        messages = [system_prompt, input_prompt]
        # Call LLM with retry
        response = await self.retry_operation(self.model.ainvoke, messages)
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
        from pathlib import Path
        
        # Resolve project path using ProjectManager
        project = self.pm.get_project(project_id)
        if not project:
            self.log(f"Project {project_id} not found, cannot save plan")
            return
            
        storage_path = Path(project['storage_path'])
        context_dir = storage_path / ".agentic"
        context_dir.mkdir(parents=True, exist_ok=True)
        
        plan_path = context_dir / "planning.md"
        self.log(f"Saving plan to: {plan_path}")
        
        try:
            with open(plan_path, "w") as f:
                f.write(f"# Implementation Plan\n\n")
                
                if "error" in workflow:
                    f.write("## ⚠️ Planning Error\n\n")
                    f.write(f"**Error**: {workflow['error']}\n\n")
                    f.write("### Raw LLM Output\n\n")
                    f.write("```\n")
                    f.write(workflow.get("raw_content", ""))
                    f.write("\n```\n")
                else:
                    f.write(f"## Architecture\n")
                    arch = workflow.get("architecture", {})
                    for component, files in arch.items():
                        f.write(f"### {component}\n")
                        for file in files:
                            f.write(f"- {file}\n")
                    
                    f.write(f"\n## Tasks\n")
                    for task in workflow.get("tasks", []):
                        f.write(f"- [{task.get('phase')}] {task.get('description')} (Agent: {task.get('agent')})\n")
            self.log(f"Plan saved successfully")
        except Exception as e:
            self.log(f"Failed to save plan: {e}")
