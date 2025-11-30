"""Error agent for fixing code errors."""

import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .base_agent import BaseAgent


class ErrorAgent(BaseAgent):
    """Agent responsible for identifying and fixing errors in code."""

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
        """Execute the error fixing task."""
        project_id = task.get("project_id")
        error_details = task.get("user_prompt") # Assuming user prompt contains error details
        
        if not project_id:
            raise ValueError("Missing project_id")

        self.log(f"Fixing errors for project: {project_id}")
        
        # Resolve project path
        from coding_agent_plugin.managers import ProjectManager
        pm = ProjectManager()
        project = pm.get_project(project_id)
        if not project:
            raise ValueError(f"Project '{project_id}' not found")
            
        project_path = project['storage_path']
        
        # Determine file to fix
        file_path_relative = task.get("file_path")
        if not file_path_relative:
             # If no specific file provided, we might need to infer or fail
             # For now, let's try to find 'generated_code.py' as fallback, or fail
             file_path_relative = "generated_code.py"
             
        file_path = os.path.join(project_path, file_path_relative)
        
        if not os.path.exists(file_path):
             return {"status": "error", "message": f"File not found: {file_path}"}
             
        with open(file_path, "r") as f:
            code_content = f.read()
            
        fixed_code = await self.fix_code(code_content, error_details)
        
        with open(file_path, "w") as f:
            f.write(fixed_code)
            
        return {"file_path": file_path, "status": "fixed"}

    async def fix_code(self, code: str, error: str) -> str:
        """Fix code using LLM."""
        from coding_agent_plugin.services.prompt_service import PromptService
        messages = [
            SystemMessage(content=PromptService.get_error_fixing_system_prompt()),
            HumanMessage(content=f"Code:\n{code}\n\nError:\n{error}")
        ]
        response = await self.model.ainvoke(messages)
        return response.content
