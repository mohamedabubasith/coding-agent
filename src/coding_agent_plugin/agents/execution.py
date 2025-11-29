"""Execution agent for executing code."""

import os
import subprocess
from typing import Dict, Any
from .base_agent import BaseAgent


class ExecutionAgent(BaseAgent):
    """Agent responsible for executing and testing code."""

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the code execution task."""
        project_id = task.get("project_id")
        command = task.get("command")
        
        if not project_id:
            raise ValueError("Missing project_id")

        self.log(f"Executing for project: {project_id}")
        
        if command:
            # Execute shell command
            self.log(f"Running command: {command}")
            result = self.run_command(command, cwd=f"projects/{project_id}")
        else:
            # Default behavior: run generated_code.py
            file_path = os.path.join(f"projects/{project_id}", "generated_code.py")
            if not os.path.exists(file_path):
                 return {"status": "error", "message": "File not found"}
            result = self.run_code(file_path)
            
        log_path = self.log_execution(project_id, result)
        
        return {"status": "executed", "log_path": log_path, "output": result}

    def run_command(self, command: str, cwd: str) -> str:
        """Run a shell command."""
        try:
            # Ensure cwd exists
            os.makedirs(cwd, exist_ok=True)
            result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True, timeout=30)
            return f"Command: {command}\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"
        except Exception as e:
            return f"Command execution failed: {str(e)}"

    def run_code(self, file_path: str) -> str:
        """Run the code file."""
        try:
            # Security warning: executing arbitrary code is dangerous.
            # In a real system, this should be sandboxed.
            result = subprocess.run(["python3", file_path], capture_output=True, text=True, timeout=10)
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
