"""Integration test for real-world project creation using ACP agents.

This test simulates the creation of a production-ready FastAPI application
using the actual Orchestrator and Agents, with mocked LLM responses to
avoid API costs and dependency on external keys.

It verifies:
1. The full ACP communication flow (Orchestrator -> Client -> Agent)
2. The Planning Agent's ability to structure a project
3. The Coding Agent's ability to write files to disk
4. The ProjectManager's ability to handle file operations
"""

import pytest
import os
import shutil
import json
from unittest.mock import MagicMock, patch
from coding_agent_plugin.agents.orchestrator import OrchestratorAgent
from coding_agent_plugin.managers import ProjectManager

# Define the mock project structure and content
MOCK_PLAN = {
    "architecture": {
        "Core": ["requirements.txt", "Dockerfile"],
        "Application": ["app/main.py", "app/models.py"]
    },
    "tasks": [
        {
            "id": 1,
            "phase": "scaffold",
            "description": "Create project dependencies",
            "agent": "coding",
            "details": {
                "file_path": "requirements.txt",
                "prompt": "Create requirements.txt for FastAPI with Uvicorn and SQLAlchemy"
            }
        },
        {
            "id": 2,
            "phase": "coding",
            "description": "Create Dockerfile",
            "agent": "coding",
            "details": {
                "file_path": "Dockerfile",
                "prompt": "Create a production-ready Dockerfile for python:3.11-slim"
            }
        },
        {
            "id": 3,
            "phase": "coding",
            "description": "Create main application entry point",
            "agent": "coding",
            "details": {
                "file_path": "app/main.py",
                "prompt": "Create app/main.py with FastAPI app and health check"
            }
        },
        {
            "id": 4,
            "phase": "coding",
            "description": "Create database models",
            "agent": "coding",
            "details": {
                "file_path": "app/models.py",
                "prompt": "Create app/models.py with User and Product models using SQLAlchemy"
            }
        }
    ]
}

MOCK_CODE_RESPONSES = {
    "requirements.txt": "fastapi==0.109.0\nuvicorn==0.27.0\nsqlalchemy==2.0.25\n",
    "Dockerfile": "FROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nRUN pip install -r requirements.txt\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\"]",
    "app/main.py": """from fastapi import FastAPI
from app.models import Base

app = FastAPI(title="E-commerce API")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
""",
    "app/models.py": """from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
"""
}

@pytest.mark.asyncio
async def test_create_production_fastapi_project():
    """Test creating a full FastAPI project via ACP agents."""
    print("\n" + "="*80)
    print("🚀 STARTING REAL-WORLD PROJECT CREATION SIMULATION")
    print("="*80)
    
    project_id = "ecommerce-backend-prod"
    project_dir = f"/tmp/{project_id}"
    
    # Clean up previous run
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    os.makedirs(project_dir)
    
    print(f"📂 Project Directory: {project_dir}")
    
    # Set dummy API key to allow agents to initialize
    os.environ["OPENAI_API_KEY"] = "sk-dummy-key-for-testing"
    
    # Mock ProjectManager to return our temp directory
    with patch("coding_agent_plugin.managers.ProjectManager.get_project") as mock_get_project, \
         patch("coding_agent_plugin.managers.ProjectManager.list_files") as mock_list_files:
        
        # Setup Project Mock
        mock_project = MagicMock()
        mock_project.storage_path = project_dir
        mock_get_project.return_value = mock_project
        mock_list_files.return_value = [] # Initially empty
        
        # Initialize Orchestrator (uses Real Agents & Real ACP Client)
        orchestrator = OrchestratorAgent()
        
        # Mock LLM Responses
        async def mock_llm_ainvoke(messages, **kwargs):
            content = messages[-1].content
            system_msg = messages[0].content if messages else ""
            
            # 1. Planning Request
            if "Create a comprehensive plan" in str(system_msg):
                print("\n🧠 [Mock LLM] Generating Project Plan...")
                return MagicMock(content=json.dumps(MOCK_PLAN))
            
            # 2. Coding Requests
            # Check which file is being requested based on the prompt content
            for filename, code in MOCK_CODE_RESPONSES.items():
                # The prompt usually contains the file path or description
                # We need to match keywords from the task description
                is_match = False
                if filename in content:
                    is_match = True
                elif filename == "requirements.txt" and "dependencies" in content:
                    is_match = True
                elif filename == "app/main.py" and "main application" in content:
                    is_match = True
                elif filename == "app/models.py" and "database models" in content:
                    is_match = True
                    
                if is_match:
                    print(f"\n💻 [Mock LLM] Generating code for: {filename}")
                    return MagicMock(content=f"```python\n{code}\n```" if filename.endswith(".py") else f"```\n{code}\n```")
            
            # Default fallback
            return MagicMock(content="OK")

        # Patch ChatOpenAI to use our mock
        with patch("langchain_openai.ChatOpenAI.ainvoke", side_effect=mock_llm_ainvoke):
            
            user_prompt = "Create a production-ready FastAPI E-commerce backend with Docker and SQLAlchemy"
            print(f"\n👤 User Prompt: {user_prompt}")
            
            # RUN THE PROJECT
            await orchestrator.run_project(user_prompt, project_id)
            
    # VERIFICATION
    print("\n" + "="*80)
    print("✅ VERIFYING GENERATED ARTIFACTS")
    print("="*80)
    
    # 1. Check requirements.txt
    req_path = os.path.join(project_dir, "requirements.txt")
    assert os.path.exists(req_path), "requirements.txt not created"
    with open(req_path) as f:
        content = f.read()
        print(f"📄 requirements.txt:\n{content.strip()}")
        assert "fastapi" in content
        assert "sqlalchemy" in content
        
    # 2. Check Dockerfile
    docker_path = os.path.join(project_dir, "Dockerfile")
    assert os.path.exists(docker_path), "Dockerfile not created"
    with open(docker_path) as f:
        content = f.read()
        print(f"\n🐳 Dockerfile:\n{content.strip()}")
        assert "FROM python:3.11" in content
        
    # 3. Check app/main.py
    main_path = os.path.join(project_dir, "app", "main.py")
    assert os.path.exists(main_path), "app/main.py not created"
    with open(main_path) as f:
        content = f.read()
        print(f"\n🐍 app/main.py:\n{content.strip()}")
        assert "FastAPI" in content
        assert "/health" in content
        
    # 4. Check app/models.py
    models_path = os.path.join(project_dir, "app", "models.py")
    assert os.path.exists(models_path), "app/models.py not created"
    with open(models_path) as f:
        content = f.read()
        print(f"\n🗄️ app/models.py:\n{content.strip()}")
        assert "class User" in content
        assert "class Product" in content
        
    print("\n" + "="*80)
    print("🎉 REAL-WORLD PROJECT CREATION SUCCESSFUL!")
    print("="*80)
    print(f"✅ Project created at: {project_dir}")
    print(f"✅ All 4 files generated correctly")
    print(f"✅ Architecture verified: FastAPI + SQLAlchemy + Docker")

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v", "-s"]))
