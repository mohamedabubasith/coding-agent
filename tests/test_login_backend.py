import asyncio
import os
import shutil
import json
from unittest.mock import MagicMock, patch
from coding_agent_plugin.agents.orchestrator import OrchestratorAgent

async def test_login_backend():
    project_id = "login_backend_demo"
    
    # Mock ChatOpenAI
    with patch("coding_agent_plugin.agents.planning.ChatOpenAI") as MockPlanningLLM, \
         patch("coding_agent_plugin.agents.coding.ChatOpenAI") as MockCodingLLM, \
         patch("coding_agent_plugin.agents.error.ChatOpenAI") as MockErrorLLM:
        
        # Setup mocks
        mock_planning_instance = MockPlanningLLM.return_value
        
        # Define a realistic plan for a Login/Register Backend
        mock_plan = {
            "architecture": {
                "backend": ["main.py", "auth.py", "models.py", "database.py", "requirements.txt"]
            },
            "tasks": [
                {
                    "id": 1,
                    "phase": "scaffold",
                    "description": "Initialize backend directory",
                    "agent": "task",
                    "details": {"action": "create_dirs", "paths": ["backend"]}
                },
                {
                    "id": 2,
                    "phase": "coding",
                    "description": "Create requirements.txt",
                    "agent": "coding",
                    "details": {"file_path": "backend/requirements.txt", "prompt": "Create requirements.txt for FastAPI, SQLAlchemy, Pydantic, and PyJWT"}
                },
                {
                    "id": 3,
                    "phase": "coding",
                    "description": "Create Database Config",
                    "agent": "coding",
                    "details": {"file_path": "backend/database.py", "prompt": "Create SQLAlchemy database setup with SQLite"}
                },
                {
                    "id": 4,
                    "phase": "coding",
                    "description": "Create User Model",
                    "agent": "coding",
                    "details": {"file_path": "backend/models.py", "prompt": "Create User model with id, email, hashed_password"}
                },
                {
                    "id": 5,
                    "phase": "coding",
                    "description": "Create Auth Logic",
                    "agent": "coding",
                    "details": {"file_path": "backend/auth.py", "prompt": "Create JWT token handling and password hashing functions"}
                },
                {
                    "id": 6,
                    "phase": "coding",
                    "description": "Create Main API",
                    "agent": "coding",
                    "details": {"file_path": "backend/main.py", "prompt": "Create FastAPI app with /register and /login endpoints using auth.py and models.py"}
                },
                {
                    "id": 7,
                    "phase": "verification",
                    "description": "Verify Main API file exists",
                    "agent": "execution",
                    "details": {"command": f"ls projects/{project_id}/backend/main.py"}
                }
            ]
        }
        
        future_planning = asyncio.Future()
        future_planning.set_result(MagicMock(content=json.dumps(mock_plan)))
        mock_planning_instance.ainvoke.return_value = future_planning
        
        # Mock Coding Agent to return dummy code based on prompt
        mock_coding_instance = MockCodingLLM.return_value
        
        def coding_side_effect(messages):
            prompt = messages[1].content
            future = asyncio.Future()
            if "requirements.txt" in prompt:
                content = "fastapi\nuvicorn\nsqlalchemy\npydantic\npyjwt\npasslib"
            elif "database.py" in prompt:
                content = "from sqlalchemy import create_engine\nengine = create_engine('sqlite:///./test.db')"
            elif "models.py" in prompt:
                content = "from sqlalchemy import Column, Integer, String\nfrom .database import Base\nclass User(Base):\n    __tablename__ = 'users'\n    id = Column(Integer, primary_key=True)\n    email = Column(String)\n    hashed_password = Column(String)"
            elif "auth.py" in prompt:
                content = "import jwt\ndef create_token(data): return jwt.encode(data, 'secret')"
            elif "main.py" in prompt:
                content = "from fastapi import FastAPI\napp = FastAPI()\n@app.post('/login')\ndef login(): pass"
            else:
                content = "# Generated code"
            future.set_result(MagicMock(content=content))
            return future

        mock_coding_instance.ainvoke.side_effect = coding_side_effect
        
        orchestrator = OrchestratorAgent()

        # Clean up previous run
        if os.path.exists(f"projects/{project_id}"):
            shutil.rmtree(f"projects/{project_id}")

        print(f"🚀 Testing Login/Register Backend Generation for project: {project_id}")
        
        await orchestrator.execute("autonomous", "Create a login/register python api backend", project_id)
        
        # Verification
        expected_files = [
            "backend/requirements.txt",
            "backend/database.py",
            "backend/models.py",
            "backend/auth.py",
            "backend/main.py"
        ]
        
        all_exist = True
        for f in expected_files:
            path = f"projects/{project_id}/{f}"
            if os.path.exists(path):
                print(f"  ✅ Created: {f}")
            else:
                print(f"  ❌ Missing: {f}")
                all_exist = False
                
        if all_exist:
            print("\n🎉 Login Backend Test Passed!")
        else:
            print("\n⚠️ Login Backend Test Failed - Missing files.")

if __name__ == "__main__":
    asyncio.run(test_login_backend())
