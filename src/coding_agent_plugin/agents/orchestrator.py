"""Orchestration agent for routing tasks to other agents."""

from coding_agent_plugin.agents.planning import PlanningAgent
from typing import Dict, Any
from .coding import CodingAgent
from .task import TaskAgent
from .error import ErrorAgent
from .execution import ExecutionAgent


class OrchestratorAgent:
    """Agent responsible for orchestrating tasks to other agents."""

    def __init__(self) -> None:
        self.agents = {
            "planning": PlanningAgent(name="planning"),
            "coding": CodingAgent(name="coding"),
            "task": TaskAgent(name="task"),
            "error": ErrorAgent(name="error"),
            "execution": ExecutionAgent(name="execution"),
        }

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
        planning_agent = self.agents["planning"]
        plan_result = await planning_agent.execute({
            "user_prompt": user_prompt, 
            "project_id": project_id
        })
        workflow = plan_result["workflow"]
        
        # Extract tasks from the plan (assuming new structured format)
        # If workflow is just a list of dicts (old format), we might need to adapt.
        # But we updated PlanningAgent to return a dict with "tasks" key.
        # Wait, PlanningAgent.execute returns {"workflow": workflow}, where workflow is the return of plan().
        # And plan() now returns a dict with "architecture" and "tasks".
        
        tasks = workflow.get("tasks", [])
        
        # 2. Execution Loop
        print(f"⚙️ Phase 2: Execution ({len(tasks)} tasks)")
        results = []
        MAX_RETRIES = 2
        
        for task in tasks:
            agent_name = task.get("agent")
            description = task.get("description")
            details = task.get("details", {})
            task_id = task.get("id", "unknown")
            
            print(f"  👉 Task {task_id}: {description} (Agent: {agent_name})")
            
            if agent_name not in self.agents:
                print(f"  ⚠️ Unknown agent: {agent_name}, skipping.")
                continue
                
            agent = self.agents[agent_name]
            
            # Prepare task input
            task_input = {
                "user_prompt": details.get("prompt", description),
                "project_id": project_id,
                **details # Merge other details like file_path, command, etc.
            }
            
            # Execute with retry logic
            retry_count = 0
            success = False
            
            while retry_count <= MAX_RETRIES and not success:
                try:
                    result = await agent.execute(task_input)
                    results.append({"task": description, "status": "success", "result": result})
                    print("     ✅ Success")
                    success = True
                    
                except Exception as e:
                    retry_count += 1
                    print(f"     ❌ Failed (attempt {retry_count}): {e}")
                    
                    # Trigger ErrorAgent if this wasn't the ErrorAgent itself and we haven't exceeded retries
                    if agent_name != "error" and retry_count <= MAX_RETRIES:
                        print(f"     🚑 Attempting recovery with ErrorAgent...")
                        
                        try:
                            error_agent = self.agents["error"]
                            error_task_input = {
                                "user_prompt": f"Fix the following error in the code: {str(e)}",
                                "project_id": project_id,
                                "file_path": details.get("file_path", "generated_code.py"),
                                "error_message": str(e)
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
