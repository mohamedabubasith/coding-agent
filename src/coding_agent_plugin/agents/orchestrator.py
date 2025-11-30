"""Orchestration agent for routing tasks to other agents."""

from coding_agent_plugin.agents.planning import PlanningAgent
from typing import Dict, Any
from .coding import CodingAgent
from .task import TaskAgent
from .error import ErrorAgent
from .execution import ExecutionAgent
from coding_agent_plugin.acp.client import InProcessACPClient


class OrchestratorAgent:
    """Agent responsible for orchestrating tasks to other agents using IBM ACP SDK."""

    def __init__(self) -> None:
        # Initialize all agents
        self.agents = {
            "planning": PlanningAgent(name="planning"),
            "coding": CodingAgent(name="coding"),
            "task": TaskAgent(name="task"),
            "error": ErrorAgent(name="error"),
            "execution": ExecutionAgent(name="execution"),
        }
        
        # Initialize ACP client for in-process communication
        # This follows IBM's ACP protocol but keeps agents in-process for performance
        self.acp_client = InProcessACPClient(self.agents)

    async def send_to_agent(self, agent_name: str, payload: dict) -> dict:
        """Send a message to an agent using IBM ACP SDK client.
        
        Args:
            agent_name: Name of the agent to invoke
            payload: The request payload
            
        Returns:
            Agent's response
        """
        return await self.acp_client.send_to_agent(agent_name, payload)

    async def execute(self, mode: str, user_prompt: str, project_id: str) -> Dict[str, Any]:
        """Execute the task based on the mode."""
        if mode == "autonomous":
            return await self.run_project(user_prompt, project_id)

        if mode not in self.agents:
            raise ValueError(f"Unsupported mode: {mode}")

        agent = self.agents[mode]
        task = {
            "user_prompt": user_prompt,
            "project_id": project_id
        }
        return await agent.execute(task)

    async def run_project(self, user_prompt: str, project_id: str) -> Dict[str, Any]:
        """Run the full autonomous project creation loop."""
        print(f"🚀 Starting autonomous project: {project_id}")
        
        # 1. Planning Phase
        print("📋 Phase 1: Planning")
        planning_task = {
            "user_prompt": user_prompt,
            "project_id": project_id
        }
        plan_result = await self.send_to_agent("planning", planning_task)
        
        workflow = plan_result.get("workflow", {})
        tasks = workflow.get("tasks", [])
        
        if not tasks:
            print("⚠️ No tasks generated in plan.")
            return {"status": "failed", "error": "No tasks in plan"}

        # Initialize tasks.md via TaskAgent
        await self.agents["task"].execute({
            "project_id": project_id,
            "action": "init_tasks",
            "tasks": tasks
        })

        print(f"⚙️ Phase 2: Execution ({len(tasks)} tasks)")
        results = []
        MAX_RETRIES = 2
        
        from coding_agent_plugin.services.project import project_service
        
        # Get project details using service
        try:
            project = await project_service.get_project(project_id)
        except Exception:
            # Fallback: try by name if ID fails (though run_project usually gets ID)
            # Or handle error appropriately
             raise ValueError(f"Project '{project_id}' not found")

        project_path = project.storage_path
        
        for i, task in enumerate(tasks, 1):
            description = task.get("description")
            agent_type = task.get("agent", "coding")
            
            print(f"  👉 Task {i}: {description} (Agent: {agent_type})")
            
            # Mark as in-progress
            await self.agents["task"].execute({
                "project_id": project_id,
                "action": "update_status",
                "task_description": description,
                "status": "in_progress"
            })
            
            task_input = {
                "user_prompt": description,
                "project_id": project_id,
                "project_path": project_path,
                **task.get("details", {})
            }
            
            retry_count = 0
            while retry_count <= MAX_RETRIES:
                try:
                    result = None
                    if agent_type == "coding":
                        result = await self.send_to_agent("coding", task_input)
                    elif agent_type == "execution":
                        result = await self.send_to_agent("execution", task_input)
                    elif agent_type == "task":
                        # TaskAgent is now mostly for tracking, but if plan assigns it work,
                        # we treat it as a generic log or maybe file op if implemented.
                        # For now, just log it.
                        result = {"status": "completed", "message": "Task tracked"}
                    else:
                        print(f"     ⚠️ Unknown agent type: {agent_type}")
                        result = {"status": "skipped"}
                    
                    results.append({"task": description, "status": "completed", "result": result})
                    print(f"     ✅ Success")
                    
                    # Mark as completed
                    await self.agents["task"].execute({
                        "project_id": project_id,
                        "action": "update_status",
                        "task_description": description,
                        "status": "completed"
                    })
                    break
                    
                except Exception as e:
                    retry_count += 1
                    print(f"     ❌ Error: {e} (attempt {retry_count})")
                    
                    # Trigger ErrorAgent if this wasn't the ErrorAgent itself and we haven't exceeded retries
                    if agent_type != "error" and retry_count < MAX_RETRIES: # Changed to < MAX_RETRIES to allow one more retry after error fix attempt
                        print(f"     🚑 Attempting recovery with ErrorAgent...")
                        
                        try:
                            error_agent = self.agents["error"]
                            error_task_input = {
                                "user_prompt": f"Fix error in {task_input.get('file_path')}: {str(e)}",
                                "error": str(e),
                                "file_path": task_input.get("file_path"), # Might be None
                                "project_id": project_id,
                                "project_path": project_path
                            }
                            
                            error_result = await error_agent.execute(error_task_input)
                            print(f"     🔧 Error fixed, retrying task...")
                            
                        except Exception as error_fix_exception:
                            print(f"     ⚠️ Error recovery failed: {error_fix_exception}")
                            
                    else:
                        # No more retries or this was the ErrorAgent itself
                        results.append({"task": description, "status": "failed", "error": str(e), "retries": retry_count})
                        print(f"     💀 Task failed after {retry_count} attempts")
                        break
                    
        return {"status": "completed", "results": results}
