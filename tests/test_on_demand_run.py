
import asyncio
import os
import sys
from pathlib import Path

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from coding_agent_plugin.managers import ProjectManager
from coding_agent_plugin.agents.orchestrator import OrchestratorAgent

async def test_on_demand_run():
    print("🚀 Starting On-Demand Run & Fix Test")
    
    # 1. Setup Project with a failing script
    pm = ProjectManager()
    project_name = "on_demand_fix_test"
    
    existing = pm.get_project(project_name)
    if existing:
        pm.delete_project(existing['id'])
        
    project = pm.create_project(project_name)
    project_id = project['id']
    project_path = project['storage_path']
    
    # Create a script that fails (division by zero)
    script_content = """
def calculate():
    print("Calculating...")
    return 10 / 0

if __name__ == "__main__":
    calculate()
"""
    with open(os.path.join(project_path, "calc.py"), "w") as f:
        f.write(script_content)
        
    print(f"✅ Created project with failing script: {os.path.join(project_path, 'calc.py')}")
    
    # 2. Simulate User Command: "Run the calculation script and fix any errors"
    print("\n[User Command] 'Run the calculation script and fix any errors'")
    
    orchestrator = OrchestratorAgent()
    
    # This mimics 'agentic-coder project run "Run the calculation script and fix any errors"'
    # The Planner should create a plan: 1. Run script.
    # The Orchestrator should: Execute -> Fail -> ErrorAgent -> Fix -> Retry -> Success.
    
    result = await orchestrator.run_project("Run the calculation script 'calc.py' and fix any errors if it fails.", project_id)
    
    # 3. Verify Result
    print("\n[Verification]")
    
    # Check if file was modified
    with open(os.path.join(project_path, "calc.py"), "r") as f:
        new_content = f.read()
        
    print(f"New Content:\n{new_content}")
    
    if "return 10 / 0" not in new_content and ("if 0" in new_content or "try" in new_content or "return" in new_content):
        # Heuristic: ErrorAgent usually fixes div by zero by checking denominator or handling exception
        # But since it's hardcoded 10/0, it might just change it to 10/1 or remove it.
        # Let's see what it does.
        print("✅ Script appears to be modified/fixed")
    else:
        print("⚠️ Script might not be fixed (check content)")
        
    # Check execution logs
    if result['status'] == 'completed':
        print("✅ Orchestrator completed successfully")
    else:
        print(f"❌ Orchestrator failed: {result}")

if __name__ == "__main__":
    asyncio.run(test_on_demand_run())
