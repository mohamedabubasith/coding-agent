from unittest.mock import patch, AsyncMock

def test_run_agent_http(client):
    request_data = {
        "project_id": "123",
        "prompt": "Do something",
        "mode": "autonomous"
    }
    
    mock_result = {"status": "completed", "tasks": []}

    with patch("coding_agent_plugin.api.v1.routers.agent_routes.agent_service.run_agent", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = mock_result
        
        response = client.post("/api/v1/agent/run", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["project_id"] == "123"
        mock_run.assert_called_once()

def test_agent_websocket(client):
    # Note: TestClient supports WebSocket testing
    
    mock_result = {"status": "completed", "result": "done"}
    
    with patch("coding_agent_plugin.api.v1.routers.agent_routes.agent_service") as mock_service:
        mock_service.run_agent = AsyncMock(return_value=mock_result)
        
        with client.websocket_connect("/api/v1/agent/ws") as websocket:
            # Test Ping
            websocket.send_json({"action": "ping"})
            data = websocket.receive_json()
            assert data == {"status": "pong"}
            
            # Test Run
            websocket.send_json({
                "action": "run",
                "project_id": "123",
                "prompt": "test",
                "mode": "autonomous"
            })
            
            # Should receive "started"
            data = websocket.receive_json()
            assert data["status"] == "started"
            
            # Should receive "completed"
            data = websocket.receive_json()
            assert data["status"] == "completed"
            assert data["project_id"] == "123"
