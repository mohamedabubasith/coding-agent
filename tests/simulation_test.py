
import asyncio
import os
import sys
import shutil
from pathlib import Path

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from coding_agent_plugin.managers import ProjectManager
from coding_agent_plugin.agents.orchestrator import OrchestratorAgent
from coding_agent_plugin.agents.file_modifier import FileModifierAgent
from coding_agent_plugin.core.config import validate_db_config, validate_llm_config

async def simulate_user_workflow():
    print("🚀 Starting Realtime User Simulation")
    
    # 1. Initialization Check
    print("\n[1] Checking Environment...")
    try:
        validate_db_config()
        validate_llm_config()
        print("✅ Environment Valid")
    except Exception as e:
        print(f"❌ Environment Invalid: {e}")
        return

    pm = ProjectManager()
    project_name = "simulation_test_project"
    
    # Cleanup previous run
    existing = pm.get_project(project_name)
    if existing:
        pm.delete_project(existing['id'])
        
    # 2. Create Project (Autonomous Mode)
    print(f"\n[2] Creating Project '{project_name}'...")
    prompt = "Create a simple Python script 'app.py' that prints 'Hello World' and a 'requirements.txt' with 'requests'."
    
    try:
        project = pm.create_project(project_name, prompt)
        project_id = project['id']
        project_path = project['storage_path']
        
        orchestrator = OrchestratorAgent()
        result = await orchestrator.run_project(prompt, project_id)
        
        if result['status'] != 'completed':
            print(f"❌ Project creation failed: {result}")
            return
            
        # Verify files
        if os.path.exists(os.path.join(project_path, "app.py")) and os.path.exists(os.path.join(project_path, "requirements.txt")):
            print("✅ Project created successfully with expected files")
        else:
            print("❌ Missing expected files")
            return
            
    except Exception as e:
        print(f"❌ Create failed: {e}")
        return

    # 3. Improve Project (Update Line)
    print("\n[3] Improving Project (Update Line)...")
    modifier = FileModifierAgent("modifier")
    
    app_path = "app.py"
    full_app_path = os.path.join(project_path, app_path)
    
    with open(full_app_path, "r") as f:
        content = f.read()
        
    try:
        await modifier.execute({
            "instruction": "Change 'Hello World' to 'Hello Simulation'",
            "file_path": app_path,
            "project_id": project_id,
            "existing_content": content
        })
        
        with open(full_app_path, "r") as f:
            new_content = f.read()
            
        if "Hello Simulation" in new_content:
            print("✅ File updated successfully")
        else:
            print(f"❌ File update failed. Content:\n{new_content}")
            
    except Exception as e:
        print(f"❌ Improve failed: {e}")

    # 4. Install Package (Simulated via Improve)
    print("\n[4] Installing Package (Adding to requirements)...")
    req_path = "requirements.txt"
    full_req_path = os.path.join(project_path, req_path)
    
    with open(full_req_path, "r") as f:
        req_content = f.read()
        
    try:
        await modifier.execute({
            "instruction": "Add 'pandas' to requirements",
            "file_path": req_path,
            "project_id": project_id,
            "existing_content": req_content
        })
        
        with open(full_req_path, "r") as f:
            new_req_content = f.read()
            
        if "pandas" in new_req_content:
            print("✅ Requirements updated successfully")
        else:
            print("❌ Requirements update failed")
            
    except Exception as e:
        print(f"❌ Package install failed: {e}")

    # 5. Delete Project
    print("\n[5] Deleting Project...")
    if pm.delete_project(project_id):
        if not os.path.exists(project_path):
            print("✅ Project deleted successfully")
        else:
            print("❌ Project folder still exists")
    else:
        print("❌ Failed to delete project")

if __name__ == "__main__":
    asyncio.run(simulate_user_workflow())
