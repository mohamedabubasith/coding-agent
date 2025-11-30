"""Task agent for managing task context."""

from typing import Dict, Any, List
from pathlib import Path
from .base_agent import BaseAgent


class TaskAgent(BaseAgent):
    """Agent responsible for managing and executing specific tasks."""

    def __init__(self, name: str = "task", model: str = None):
        super().__init__(name, model)
        super().__init__(name, model)
        from coding_agent_plugin.services.project import project_service
        self.project_service = project_service

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task management operations."""
        project_id = task.get("project_id")
        action = task.get("action")
        
        if not project_id:
            raise ValueError("Missing project_id")

        if action == "init_tasks":
            tasks_list = task.get("tasks", [])
            return await self.init_tasks(project_id, tasks_list)
        elif action == "update_status":
            task_desc = task.get("task_description")
            status = task.get("status", "completed")
            return await self.update_task_status(project_id, task_desc, status)
        else:
            # Default/Legacy behavior: just log
            user_prompt = task.get("user_prompt")
            if user_prompt:
                self.log(f"Managing task: {user_prompt}")
                # We could append to tasks.md here if it's a new ad-hoc task
                return {"status": "logged"}
            return {"status": "no_action"}

    async def _get_tasks_file(self, project_id: str) -> Path:
        """Resolve tasks.md path."""
        from pathlib import Path
        try:
            project = await self.project_service.get_project(project_id)
        except Exception:
             # Fallback or error
             raise ValueError(f"Project {project_id} not found")
             
        context_dir = Path(project.storage_path) / ".agentic"
        context_dir.mkdir(parents=True, exist_ok=True)
        return context_dir / "tasks.md"

    async def init_tasks(self, project_id: str, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Initialize tasks.md with the plan."""
        try:
            file_path = await self._get_tasks_file(project_id)
            
            with open(file_path, "w") as f:
                f.write("# Project Tasks\n\n")
                for t in tasks:
                    desc = t.get("description", "Unknown task")
                    agent = t.get("agent", "unknown")
                    f.write(f"- [ ] {desc} (Agent: {agent})\n")
            
            self.log(f"Initialized tasks.md at {file_path}")
            return {"status": "initialized", "file_path": str(file_path)}
        except Exception as e:
            self.log(f"Failed to init tasks: {e}")
            return {"status": "error", "error": str(e)}

    async def update_task_status(self, project_id: str, task_desc: str, status: str) -> Dict[str, Any]:
        """Mark a task as completed in tasks.md."""
        try:
            file_path = await self._get_tasks_file(project_id)
            if not file_path.exists():
                return {"status": "error", "error": "tasks.md not found"}
            
            lines = []
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            updated = False
            new_lines = []
            for line in lines:
                if task_desc in line:
                    if status == "completed":
                        if "- [ ]" in line:
                            new_lines.append(line.replace("- [ ]", "- [x]"))
                            updated = True
                        elif "- [/]" in line:
                            new_lines.append(line.replace("- [/]", "- [x]"))
                            updated = True
                        else:
                            new_lines.append(line)
                    elif status == "in_progress":
                        if "- [ ]" in line:
                            new_lines.append(line.replace("- [ ]", "- [/]"))
                            updated = True
                        else:
                            new_lines.append(line)
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            
            if updated:
                with open(file_path, "w") as f:
                    f.writelines(new_lines)
                self.log(f"Updated task status: {task_desc} -> {status}")
            
            return {"status": "updated" if updated else "not_found"}
        except Exception as e:
            self.log(f"Failed to update task: {e}")
            return {"status": "error", "error": str(e)}
