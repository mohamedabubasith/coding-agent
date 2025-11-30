import pytest
import os
import sys
from pathlib import Path

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from coding_agent_plugin.managers.project_manager import ProjectManager
from coding_agent_plugin.agents.orchestrator import OrchestratorAgent

def test_project_manager_initialization():
    pm = ProjectManager()
    assert pm.projects_dir.exists()
    assert pm.db_path is not None

def test_orchestrator_agent_initialization():
    agent = OrchestratorAgent()
    assert agent is not None
