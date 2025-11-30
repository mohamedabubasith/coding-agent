
import asyncio
import os
import sys
from pathlib import Path

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from coding_agent_plugin.agents.orchestrator import OrchestratorAgent
from coding_agent_plugin.managers import ProjectManager

async def test_error_recovery():
    print("🚀 Starting Error Recovery Test")
    
    # 1. Setup Project
    pm = ProjectManager()
    project_name = "error_recovery_test"
    
    # Clean up existing
    existing = pm.get_project(project_name)
    if existing:
        pm.delete_project(existing['id'])
        
    project = pm.create_project(project_name)
    project_id = project['id']
    print(f"✅ Project created: {project_id}")
    
    # 2. Create a broken file manually
    broken_code = """
def hello():
    print("Missing closing parenthesis"
"""
    file_path = os.path.join(project['storage_path'], "broken.py")
    with open(file_path, "w") as f:
        f.write(broken_code)
    print(f"✅ Created broken file: {file_path}")
    
    # 3. Simulate Orchestrator Task Execution Failure
    # We will manually invoke the Orchestrator's internal logic or just use the agents directly
    # to simulate the loop. But to test the REAL loop, we should try to run a task via Orchestrator
    # that involves running this file.
    
    orchestrator = OrchestratorAgent()
    
    # We'll construct a task that asks to RUN this file.
    # The ExecutionAgent should fail, and Orchestrator should catch it.
    
    # However, Orchestrator.run_project does the whole planning loop.
    # Let's try to use the Orchestrator to run a specific "execution" task directly?
    # No, Orchestrator.run_project is the main loop.
    
    # Let's create a fake plan that has an execution task for this file.
    # But we can't easily inject a plan into run_project without mocking.
    
    # Alternative: We can verify the components individually work as expected.
    
    # A. Execution Agent fails
    print("\nTesting ExecutionAgent failure...")
    exec_agent = orchestrator.agents["execution"]
    try:
        await exec_agent.execute({
            "project_id": project_id,
            "project_path": project['storage_path'],
            "file_path": "broken.py" # ExecutionAgent uses this to find file
        })
        print("❌ ExecutionAgent should have failed but didn't")
    except Exception as e:
        print(f"✅ ExecutionAgent failed as expected: {e}")
        
        # B. Error Agent fixes
        print("\nTesting ErrorAgent fix...")
        error_agent = orchestrator.agents["error"]
        
        # This matches what Orchestrator passes
        error_task = {
            "user_prompt": f"Fix error in broken.py: {str(e)}",
            "error": str(e),
            "file_path": "broken.py",
            "project_id": project_id,
            "project_path": project['storage_path']
        }
        
        await error_agent.execute(error_task)
        
        # C. Verify Fix
        with open(file_path, "r") as f:
            content = f.read()
        
        print(f"\nFixed Content:\n{content}")
        
        if 'print("Missing closing parenthesis")' in content:
             print("✅ ErrorAgent successfully fixed the code!")
        else:
             print("❌ ErrorAgent failed to fix the code.")

if __name__ == "__main__":
    asyncio.run(test_error_recovery())
