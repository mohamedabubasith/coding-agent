from unittest.mock import patch
from datetime import datetime
from coding_agent_plugin.models.audit import AuditLogResponse

def test_create_audit_log(client):
    audit_data = {
        "project_id": "123",
        "event_type": "TEST_EVENT",
        "data": {"info": "test"},
        "source": "test_client"
    }
    
    mock_response = AuditLogResponse(
        id=1,
        project_id="123",
        event_type="TEST_EVENT",
        data={"info": "test"},
        timestamp=datetime.now(),
        source="test_client"
    )

    with patch("coding_agent_plugin.api.v1.routers.audit_routes.audit_service.create_audit_log") as mock_create:
        mock_create.return_value = mock_response
        
        response = client.post("/api/v1/audit/", json=audit_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["event_type"] == "TEST_EVENT"
        assert data["project_id"] == "123"

def test_list_audit_logs(client):
    mock_response = AuditLogResponse(
        id=1,
        project_id="123",
        event_type="TEST_EVENT",
        data={"info": "test"},
        timestamp=datetime.now(),
        source="test_client"
    )

    with patch("coding_agent_plugin.api.v1.routers.audit_routes.audit_service.list_audit_logs") as mock_list:
        mock_list.return_value = [mock_response]
        
        response = client.get("/api/v1/audit/?project_id=123")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["event_type"] == "TEST_EVENT"
