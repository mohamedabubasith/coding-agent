from unittest.mock import patch
from datetime import datetime
from coding_agent_plugin.models.project import ProjectResponse

def test_create_project(client):
    project_data = {
        "project_name": "test_project",
        "description": "Test Description",
        "config": {"key": "value"}
    }
    
    mock_response = ProjectResponse(
        id="123",
        project_name="test_project",
        description="Test Description",
        storage_path="/tmp/test_project",
        config={"key": "value"},
        created_at=datetime.now(),
        updated_at=datetime.now(),
        status="active"
    )

    with patch("coding_agent_plugin.api.v1.routers.project_routes.project_service.create_project") as mock_create:
        mock_create.return_value = mock_response
        
        response = client.post("/api/v1/projects/", json=project_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["project_name"] == "test_project"
        assert data["id"] == "123"
        mock_create.assert_called_once()

def test_list_projects(client):
    mock_response = ProjectResponse(
        id="123",
        project_name="test_project",
        description="Test Description",
        storage_path="/tmp/test_project",
        config={},
        created_at=datetime.now(),
        updated_at=datetime.now(),
        status="active"
    )

    with patch("coding_agent_plugin.api.v1.routers.project_routes.project_service.list_projects") as mock_list:
        mock_list.return_value = [mock_response]
        
        response = client.get("/api/v1/projects/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["project_name"] == "test_project"

def test_get_project(client):
    mock_response = ProjectResponse(
        id="123",
        project_name="test_project",
        description="Test Description",
        storage_path="/tmp/test_project",
        config={},
        created_at=datetime.now(),
        updated_at=datetime.now(),
        status="active"
    )

    with patch("coding_agent_plugin.api.v1.routers.project_routes.project_service.get_project") as mock_get:
        mock_get.return_value = mock_response
        
        response = client.get("/api/v1/projects/123")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "123"
        assert data["project_name"] == "test_project"
