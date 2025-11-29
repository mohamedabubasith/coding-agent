"""Execution agent for executing code."""

import os
import subprocess
from typing import Dict, Any
from .base_agent import BaseAgent


class ExecutionAgent(BaseAgent):
    """Agent responsible for executing and testing code."""

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute command or code."""
        project_id = task.get("project_id")
        command = task.get("command")
        
        if not project_id:
            raise ValueError("Missing project_id")
            
        self.log(f"Executing for project: {project_id}")
        
        # Determine working directory
        cwd = task.get("project_path")
        if not cwd:
            from coding_agent_plugin.managers import ProjectManager
            pm = ProjectManager()
            project = pm.get_project(project_id)
            if project:
                cwd = project.storage_path
            else:
                cwd = os.path.abspath(f"projects/{project_id}")
        
        if command:
            self.log(f"Running command: {command} in {cwd}")
            result = await self.run_command(command, cwd=cwd)
        else:
            # Default behavior: run generated_code.py
            file_path = os.path.join(cwd, "generated_code.py")
            if not os.path.exists(file_path):
                 return {"status": "error", "message": "File not found"}
            result = await self.run_code(file_path)
            
        log_path = self.log_execution(project_id, result)
        
        return {"status": "executed", "log_path": log_path, "output": result}

    async def run_command(self, command: str, cwd: str) -> str:
        """Run a shell command."""
        try:
            # Ensure cwd exists
            os.makedirs(cwd, exist_ok=True)
            # Use asyncio to run blocking subprocess in executor
            import asyncio
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True, timeout=30)
            )
            return f"Command: {command}\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"
        except Exception as e:
            return f"Command execution failed: {str(e)}"

    async def run_code(self, file_path: str) -> str:
        """Run the code file."""
        try:
            # Security warning: executing arbitrary code is dangerous.
            # In a real system, this should be sandboxed.
            import asyncio
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: subprocess.run(["python3", file_path], capture_output=True, text=True, timeout=10)
            )
            return f"Stdout:\n{result.stdout}\nStderr:\n{result.stderr}"
        except Exception as e:
            return f"Execution failed: {str(e)}"

    def log_execution(self, project_id: str, result: str) -> str:
        """Log execution results."""
        directory = f"projects/{project_id}/.agent_context"
        os.makedirs(directory, exist_ok=True)
        
        file_path = os.path.join(directory, "execution.md")
        
        with open(file_path, "a") as f:
            f.write(f"\n## Execution Result\n```\n{result}\n```\n")
            
        return file_path
