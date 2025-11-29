import asyncio
import os
import sys

# Add src to path
sys.path.append(os.path.abspath("src"))

from coding_agent_plugin.managers.project_manager import ProjectManager
from coding_agent_plugin.agents.coding import CodingAgent
from coding_agent_plugin.agents.orchestrator import OrchestratorAgent

async def test_package():
    print("--- Package Test ---")
    pm = ProjectManager()
    
    # 1. Testing Direct Mode (CodingAgent)...
    print("\n1. Testing Direct Mode (CodingAgent)...")
    try:
        proj_direct = pm.create_project("Pkg Direct Final", "Package Direct Final Test")
    except ValueError:
        print("Project 'Pkg Direct Final' exists, retrieving...")
        projects = pm.list_projects()
        proj_direct = next(p for p in projects if p['name'] == "Pkg Direct Final")
        
    print(f"Using project: {proj_direct['id']}")
    coding_agent = CodingAgent(name="coding")
    
    # Task 1: Creation
    print("\n[Direct] Task 1: Creation")
    result = await coding_agent.execute({
        "user_prompt": "create a file final_direct.py with print('v1')",
        "project_id": proj_direct['id']
    })
    print(f"Direct Result 1: {result}")

    # Task 2: Follow-up Modification
    print("\n[Direct] Task 2: Modification")
    result = await coding_agent.execute({
        "user_prompt": "modify final_direct.py to print('v2 updated')",
        "project_id": proj_direct['id']
    })
    print(f"Direct Result 2: {result}")

    # 2. Testing Autonomous Mode (OrchestratorAgent)...
    print("\n2. Testing Autonomous Mode (OrchestratorAgent)...")
    try:
        proj_auto = pm.create_project("Pkg Auto Final", "Package Auto Final Test")
    except ValueError:
        print("Project 'Pkg Auto Final' exists, retrieving...")
        projects = pm.list_projects()
        proj_auto = next(p for p in projects if p['name'] == "Pkg Auto Final")
        
    orch = OrchestratorAgent()
    
    # Task 1: Creation
    print("\n[Auto] Task 1: Creation")
    await orch.run_project(
        user_prompt="create a file final_auto.py with print('auto v1')",
        project_id=proj_auto['id']
    )
    
    # Task 2: Follow-up (Add new feature)
    print("\n[Auto] Task 2: Follow-up (Add file)")
    await orch.run_project(
        user_prompt="create another file final_auto_2.py with print('auto v2')",
        project_id=proj_auto['id']
    )
    
    print("Autonomous Run Complete")

if __name__ == "__main__":
    asyncio.run(test_package())
