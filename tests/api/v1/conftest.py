import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import sys
import os

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../src"))

# Mock acp_sdk before importing app
import types
acp_sdk = types.ModuleType("acp_sdk")
sys.modules["acp_sdk"] = acp_sdk
sys.modules["acp_sdk.client"] = MagicMock()
acp_sdk_models = types.ModuleType("acp_sdk.models")
sys.modules["acp_sdk.models"] = acp_sdk_models
acp_sdk_models.Message = MagicMock()
sys.modules["acp_sdk.models.models"] = MagicMock()

from coding_agent_plugin.app import app
from coding_agent_plugin.services.project import project_service
from coding_agent_plugin.services.audit import audit_service
from coding_agent_plugin.services.agent import agent_service

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_project_service():
    original_service = project_service
    mock = MagicMock()
    # Replace global instance methods with mock
    # Note: We can't easily replace the instance itself in the imported module 
    # unless we patch it where it's used.
    # But since we are using `project_service` imported in routers, 
    # we can patch `coding_agent_plugin.api.v1.routers.project_routes.project_service`
    yield mock

@pytest.fixture
def mock_audit_service():
    mock = MagicMock()
    yield mock

@pytest.fixture
def mock_agent_service():
    mock = MagicMock()
    yield mock
