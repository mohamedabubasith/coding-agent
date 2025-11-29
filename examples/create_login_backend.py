"""
Real execution script for testing the autonomous flow with actual LLM API calls.
This script creates a FastAPI login/register backend.

IMPORTANT: Ensure you have a valid OPENAI_API_KEY in your .env file.
"""

import asyncio
import os
import shutil
from coding_agent_plugin.agents.orchestrator import OrchestratorAgent

async def create_login_backend():
    project_id = "real_login_backend"
    
    # Clean up previous run
    if os.path.exists(f"projects/{project_id}"):
        print(f"🗑️ Cleaning up previous project: {project_id}")
        shutil.rmtree(f"projects/{project_id}")
    
    print(f"\n{'='*60}")
    print(f"🚀 Creating Login/Register Backend with REAL LLM")
    print(f"{'='*60}\n")
    
    orchestrator = OrchestratorAgent()
    
    user_prompt = """Create a FastAPI backend with login and register endpoints.

Requirements:
- Use FastAPI for the web framework
- Use SQLAlchemy with SQLite for the database
- Implement JWT token-based authentication
- Create the following files:
  1. requirements.txt - List all dependencies
  2. database.py - Database connection setup
  3. models.py - User model with id, email, hashed_password
  4. auth.py - JWT token creation, password hashing functions
  5. main.py - FastAPI app with /register and /login endpoints

The code should be production-ready and follow best practices."""
    
    try:
        result = await orchestrator.execute(
            mode="autonomous",
            user_prompt=user_prompt,
            project_id=project_id
        )
        
        print(f"\n{'='*60}")
        print(f"✅ Project Creation Complete!")
        print(f"{'='*60}\n")
        
        # Verify files
        print("📁 Checking generated files:\n")
        expected_files = [
            "backend/requirements.txt",
            "backend/database.py",
            "backend/models.py",
            "backend/auth.py",
            "backend/main.py"
        ]
        
        for file in expected_files:
            path = f"projects/{project_id}/{file}"
            if os.path.exists(path):
                size = os.path.getsize(path)
                status = "✅" if size > 0 else "⚠️ (EMPTY)"
                print(f"  {status} {file} ({size} bytes)")
                
                # Show first few lines if not empty
                if size > 0:
                    with open(path, 'r') as f:
                        lines = f.readlines()[:3]
                        for line in lines:
                            print(f"      {line.rstrip()}")
                    if len(lines) >= 3:
                        print(f"      ...")
                    print()
            else:
                print(f"  ❌ {file} (NOT FOUND)")
        
        # Check planning
        planning_path = f"projects/{project_id}/.agent_context/planning.md"
        if os.path.exists(planning_path):
            print(f"\n📋 Planning file created: {planning_path}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\n⚠️  IMPORTANT: This script requires a valid OPENAI_API_KEY in your .env file\n")
    asyncio.run(create_login_backend())
