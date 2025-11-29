"""Task agent for managing task context."""

import os
from typing import Dict, Any
from .base_agent import BaseAgent


class TaskAgent(BaseAgent):
    """Agent responsible for managing and executing specific tasks."""

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the task management."""
        user_prompt = task.get("user_prompt")
        project_id = task.get("project_id")
        
        if not user_prompt or not project_id:
            raise ValueError("Missing user_prompt or project_id")

        self.log(f"Managing task: {user_prompt}")
        
        file_path = self.update_task_context(project_id, user_prompt)
        
        return {"file_path": file_path, "status": "updated"}

    def update_task_context(self, project_id: str, content: str) -> str:
        """Update task context file."""
        directory = f"projects/{project_id}/.agent_context"
        os.makedirs(directory, exist_ok=True)
        
        file_path = os.path.join(directory, "tasks.md")
        
        # Append to existing file or create new
        with open(file_path, "a") as f:
            f.write(f"\n- [ ] {content}\n")
            
        return file_path
