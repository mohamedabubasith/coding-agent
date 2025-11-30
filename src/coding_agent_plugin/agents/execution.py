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
            # Run specific file
            file_path_relative = task.get("file_path")
            if not file_path_relative:
                # Fallback
                file_path_relative = "generated_code.py"
                
            file_path = os.path.join(cwd, file_path_relative)
            if not os.path.exists(file_path):
                 return {"status": "error", "message": f"File not found: {file_path}"}
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
        """Run the code file based on extension."""
        try:
            # Security warning: executing arbitrary code is dangerous.
            # In a real system, this should be sandboxed.
            
            ext = os.path.splitext(file_path)[1].lower()
            command = []
            
            if ext == ".py":
                command = ["python3", file_path]
            elif ext == ".js":
                command = ["node", file_path]
            elif ext == ".ts":
                command = ["ts-node", file_path]
            elif ext == ".sh":
                command = ["bash", file_path]
            elif ext == ".c":
                # Compile and run
                exe_path = os.path.splitext(file_path)[0]
                command = ["sh", "-c", f"gcc {file_path} -o {exe_path} && {exe_path}"]
            elif ext == ".cpp":
                # Compile and run
                exe_path = os.path.splitext(file_path)[0]
                command = ["sh", "-c", f"g++ {file_path} -o {exe_path} && {exe_path}"]
            elif ext == ".go":
                command = ["go", "run", file_path]
            elif ext == ".rs":
                # Compile and run
                exe_path = os.path.splitext(file_path)[0]
                command = ["sh", "-c", f"rustc {file_path} && {exe_path}"]
            else:
                return f"Unsupported file type: {ext}"
            
            import asyncio
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: subprocess.run(command, capture_output=True, text=True, timeout=30)
            )
            
            output = ""
            if result.stdout:
                output += f"Stdout:\n{result.stdout}\n"
            if result.stderr:
                output += f"Stderr:\n{result.stderr}\n"
                
            if result.returncode != 0:
                # Raise exception to trigger ErrorAgent in Orchestrator
                raise Exception(f"Execution failed with code {result.returncode}:\n{output}")
                
            return output
        except subprocess.TimeoutExpired:
            raise Exception("Execution timed out after 30 seconds")
        except Exception as e:
            # Re-raise to be caught by Orchestrator
            raise e

    def log_execution(self, project_id: str, result: str) -> str:
        """Log execution results."""
        directory = f"projects/{project_id}/.agent_context"
        os.makedirs(directory, exist_ok=True)
        
        file_path = os.path.join(directory, "execution.md")
        
        with open(file_path, "a") as f:
            f.write(f"\n## Execution Result\n```\n{result}\n```\n")
            
        return file_path
