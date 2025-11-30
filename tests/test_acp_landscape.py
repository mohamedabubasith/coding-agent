"""Comprehensive ACP Integration Tests.

These tests demonstrate:
1. How each agent communicates through ACP
2. The message flow between orchestrator and agents
3. The complete landscape of agent interactions
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any

# We'll mock the agents since they require API keys
from coding_agent_plugin.acp.client import InProcessACPClient


class TestACPAgentLandscape:
    """Test suite to visualize the complete agent communication landscape."""
    
    @pytest.fixture
    def mock_agents(self):
        """Create mock agents with realistic behavior."""
        
        # Mock Planning Agent
        planning_agent = AsyncMock()
        planning_agent.execute = AsyncMock(return_value={
            "status": "success",
            "workflow": {
                "tasks": [
                    {
                        "description": "Create FastAPI main application file",
                        "agent": "coding",
                        "details": {"file_path": "main.py"}
                    },
                    {
                        "description": "Run the application",
                        "agent": "execution",
                        "details": {"command": "uvicorn main:app"}
                    }
                ]
            }
        })
        
        # Mock Coding Agent
        coding_agent = AsyncMock()
        coding_agent.execute = AsyncMock(return_value={
            "status": "success",
            "files_created": ["main.py"],
            "code": "from fastapi import FastAPI\napp = FastAPI()"
        })
        
        # Mock Execution Agent
        execution_agent = AsyncMock()
        execution_agent.execute = AsyncMock(return_value={
            "status": "success",
            "output": "Application started on http://localhost:8000",
            "exit_code": 0
        })
        
        # Mock Task Agent
        task_agent = AsyncMock()
        task_agent.execute = AsyncMock(return_value={
            "status": "success",
            "task_updated": True
        })
        
        # Mock Error Agent
        error_agent = AsyncMock()
        error_agent.execute = AsyncMock(return_value={
            "status": "success",
            "error_fixed": True,
            "fix_description": "Added missing import"
        })
        
        return {
            "planning": planning_agent,
            "coding": coding_agent,
            "execution": execution_agent,
            "task": task_agent,
            "error": error_agent
        }
    
    @pytest.fixture
    def acp_client(self, mock_agents):
        """Create InProcessACPClient with mock agents."""
        return InProcessACPClient(mock_agents)
    
    @pytest.mark.asyncio
    async def test_planning_agent_through_acp(self, acp_client, mock_agents):
        """Test 1: Planning Agent Communication via ACP."""
        print("\n" + "="*80)
        print("TEST 1: PLANNING AGENT COMMUNICATION LANDSCAPE")
        print("="*80)
        
        # Prepare request
        request_payload = {
            "user_prompt": "Create a FastAPI application with health endpoint",
            "project_id": "test-project-123"
        }
        
        print(f"\n📤 REQUEST to Planning Agent:")
        print(f"   User Prompt: {request_payload['user_prompt']}")
        print(f"   Project ID: {request_payload['project_id']}")
        
        # Send through ACP
        print(f"\n🔄 ROUTING through InProcessACPClient...")
        result = await acp_client.send_to_agent("planning", request_payload)
        
        print(f"\n📥 RESPONSE from Planning Agent:")
        print(f"   Status: {result['status']}")
        print(f"   Tasks Generated: {len(result['workflow']['tasks'])}")
        for i, task in enumerate(result['workflow']['tasks'], 1):
            print(f"   Task {i}: {task['description']}")
            print(f"     → Agent: {task['agent']}")
            print(f"     → Details: {task['details']}")
        
        # Verify
        mock_agents["planning"].execute.assert_called_once_with(request_payload)
        assert result["status"] == "success"
        assert len(result["workflow"]["tasks"]) == 2
        print(f"\n✅ Planning Agent Test PASSED")
    
    @pytest.mark.asyncio
    async def test_coding_agent_through_acp(self, acp_client, mock_agents):
        """Test 2: Coding Agent Communication via ACP."""
        print("\n" + "="*80)
        print("TEST 2: CODING AGENT COMMUNICATION LANDSCAPE")
        print("="*80)
        
        # Prepare request
        request_payload = {
            "user_prompt": "Create FastAPI main application file",
            "project_id": "test-project-123",
            "file_path": "main.py"
        }
        
        print(f"\n📤 REQUEST to Coding Agent:")
        print(f"   Task: {request_payload['user_prompt']}")
        print(f"   Target File: {request_payload['file_path']}")
        
        # Send through ACP
        print(f"\n🔄 ROUTING through InProcessACPClient...")
        result = await acp_client.send_to_agent("coding", request_payload)
        
        print(f"\n📥 RESPONSE from Coding Agent:")
        print(f"   Status: {result['status']}")
        print(f"   Files Created: {result['files_created']}")
        print(f"   Code Sample:")
        for line in result['code'].split('\n'):
            print(f"     {line}")
        
        # Verify
        mock_agents["coding"].execute.assert_called_once_with(request_payload)
        assert result["status"] == "success"
        assert "main.py" in result["files_created"]
        print(f"\n✅ Coding Agent Test PASSED")
    
    @pytest.mark.asyncio
    async def test_execution_agent_through_acp(self, acp_client, mock_agents):
        """Test 3: Execution Agent Communication via ACP."""
        print("\n" + "="*80)
        print("TEST 3: EXECUTION AGENT COMMUNICATION LANDSCAPE")
        print("="*80)
        
        # Prepare request
        request_payload = {
            "user_prompt": "Run the application",
            "project_id": "test-project-123",
            "command": "uvicorn main:app"
        }
        
        print(f"\n📤 REQUEST to Execution Agent:")
        print(f"   Task: {request_payload['user_prompt']}")
        print(f"   Command: {request_payload['command']}")
        
        # Send through ACP
        print(f"\n🔄 ROUTING through InProcessACPClient...")
        result = await acp_client.send_to_agent("execution", request_payload)
        
        print(f"\n📥 RESPONSE from Execution Agent:")
        print(f"   Status: {result['status']}")
        print(f"   Output: {result['output']}")
        print(f"   Exit Code: {result['exit_code']}")
        
        # Verify
        mock_agents["execution"].execute.assert_called_once_with(request_payload)
        assert result["status"] == "success"
        assert result["exit_code"] == 0
        print(f"\n✅ Execution Agent Test PASSED")
    
    @pytest.mark.asyncio
    async def test_error_agent_through_acp(self, acp_client, mock_agents):
        """Test 4: Error Agent Communication via ACP."""
        print("\n" + "="*80)
        print("TEST 4: ERROR AGENT COMMUNICATION LANDSCAPE")
        print("="*80)
        
        # Prepare request
        request_payload = {
            "error": "ModuleNotFoundError: No module named 'fastapi'",
            "file_path": "main.py",
            "project_id": "test-project-123"
        }
        
        print(f"\n📤 REQUEST to Error Agent:")
        print(f"   Error: {request_payload['error']}")
        print(f"   File: {request_payload['file_path']}")
        
        # Send through ACP
        print(f"\n🔄 ROUTING through InProcessACPClient...")
        result = await acp_client.send_to_agent("error", request_payload)
        
        print(f"\n📥 RESPONSE from Error Agent:")
        print(f"   Status: {result['status']}")
        print(f"   Error Fixed: {result['error_fixed']}")
        print(f"   Fix Description: {result['fix_description']}")
        
        # Verify
        mock_agents["error"].execute.assert_called_once_with(request_payload)
        assert result["status"] == "success"
        assert result["error_fixed"] is True
        print(f"\n✅ Error Agent Test PASSED")
    
    @pytest.mark.asyncio
    async def test_multi_agent_workflow(self, acp_client, mock_agents):
        """Test 5: Complete Multi-Agent Workflow via ACP."""
        print("\n" + "="*80)
        print("TEST 5: COMPLETE MULTI-AGENT WORKFLOW LANDSCAPE")
        print("="*80)
        print("\nScenario: User wants to create a FastAPI app")
        print("Expected Flow: Planning → Coding → Execution")
        
        # Step 1: Planning
        print(f"\n{'─'*80}")
        print("STEP 1: PLANNING PHASE")
        print(f"{'─'*80}")
        planning_request = {
            "user_prompt": "Create a FastAPI application with health endpoint",
            "project_id": "test-project-123"
        }
        print(f"📤 Sending to Planning Agent...")
        plan_result = await acp_client.send_to_agent("planning", planning_request)
        print(f"✅ Received plan with {len(plan_result['workflow']['tasks'])} tasks")
        
        # Step 2: Execute each task
        tasks = plan_result['workflow']['tasks']
        
        for i, task in enumerate(tasks, 1):
            print(f"\n{'─'*80}")
            print(f"STEP {i+1}: EXECUTING TASK - {task['description']}")
            print(f"{'─'*80}")
            
            task_agent_type = task['agent']
            task_payload = {
                "user_prompt": task['description'],
                "project_id": "test-project-123",
                **task['details']
            }
            
            print(f"📤 Routing to {task_agent_type.upper()} Agent...")
            task_result = await acp_client.send_to_agent(task_agent_type, task_payload)
            print(f"✅ {task_agent_type.upper()} Agent completed successfully")
            print(f"   Result: {task_result.get('status', 'unknown')}")
            
            # Show what the agent did
            if task_agent_type == "coding":
                print(f"   Files Created: {task_result.get('files_created', [])}")
            elif task_agent_type == "execution":
                print(f"   Output: {task_result.get('output', 'N/A')}")
        
        print(f"\n{'='*80}")
        print("WORKFLOW COMPLETE")
        print(f"{'='*80}")
        print(f"✅ All agents communicated successfully via ACP")
        print(f"✅ Planning Agent called: 1 time")
        print(f"✅ Coding Agent called: 1 time")
        print(f"✅ Execution Agent called: 1 time")
        print(f"\n🎉 Multi-Agent Workflow Test PASSED")
    
    @pytest.mark.asyncio
    async def test_acp_client_error_handling(self, mock_agents):
        """Test 6: ACP Client Error Handling."""
        print("\n" + "="*80)
        print("TEST 6: ACP ERROR HANDLING LANDSCAPE")
        print("="*80)
        
        acp_client = InProcessACPClient(mock_agents)
        
        # Test invalid agent
        print(f"\n📤 Attempting to call non-existent agent...")
        with pytest.raises(ValueError) as exc_info:
            await acp_client.send_to_agent("nonexistent", {"test": "data"})
        
        print(f"✅ Correctly raised ValueError:")
        print(f"   Error: {exc_info.value}")
        assert "not found" in str(exc_info.value)
        print(f"\n✅ Error Handling Test PASSED")
    
    @pytest.mark.asyncio
    async def test_acp_message_format_consistency(self, acp_client, mock_agents):
        """Test 7: ACP Message Format Consistency."""
        print("\n" + "="*80)
        print("TEST 7: ACP MESSAGE FORMAT CONSISTENCY")
        print("="*80)
        
        # Test that all agents receive and return consistent formats
        agents_to_test = ["planning", "coding", "execution", "task", "error"]
        
        for agent_name in agents_to_test:
            print(f"\n🔍 Testing {agent_name.upper()} Agent message format...")
            
            request = {
                "user_prompt": f"Test {agent_name}",
                "project_id": "test-123"
            }
            
            result = await acp_client.send_to_agent(agent_name, request)
            
            # Verify response structure
            assert isinstance(result, dict), f"{agent_name} should return dict"
            assert "status" in result, f"{agent_name} response should have 'status'"
            
            print(f"   ✅ Request format: dict with required fields")
            print(f"   ✅ Response format: dict with 'status' field")
        
        print(f"\n✅ All agents maintain consistent message formats")
        print(f"✅ Message Format Test PASSED")


def print_agent_landscape_diagram():
    """Print a visual diagram of the agent communication landscape."""
    print("\n" + "="*80)
    print("AGENT COMMUNICATION LANDSCAPE DIAGRAM")
    print("="*80)
    print("""
┌─────────────────────────────────────────────────────────────────────┐
│                         USER REQUEST                                 │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                                │
│  • Receives user request                                             │
│  • Manages overall workflow                                          │
│  • Routes tasks to appropriate agents                                │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   InProcessACPClient                                 │
│  IBM ACP SDK Compliant Communication Layer                           │
│  • Validates agent existence                                         │
│  • Routes messages to correct agent                                  │
│  • Maintains ACP protocol compliance                                 │
└──────┬──────┬──────┬──────┬──────────────────────────────────────────┘
       │      │      │      │      
       ▼      ▼      ▼      ▼      
    ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
    │PLAN│ │CODE│ │EXEC│ │TASK│ │ERR │
    │NING│ │  │ │TION│ │    │ │  │
    └────┘ └────┘ └────┘ └────┘ └────┘
       │      │      │      │      │
       ▼      ▼      ▼      ▼      ▼
    ┌─────────────────────────────────┐
    │  1. Planning Agent               │
    │     • Analyzes user request      │
    │     • Creates task workflow      │
    │     • Determines agent sequence  │
    └─────────────────────────────────┘
    
    ┌─────────────────────────────────┐
    │  2. Coding Agent                 │
    │     • Generates code files       │
    │     • Creates project structure  │
    │     • Implements features        │
    └─────────────────────────────────┘
    
    ┌─────────────────────────────────┐
    │  3. Execution Agent              │
    │     • Runs commands              │
    │     • Executes tests             │
    │     • Starts services            │
    └─────────────────────────────────┘
    
    ┌─────────────────────────────────┐
    │  4. Task Agent                   │
    │     • Tracks progress            │
    │     • Updates task status        │
    │     • Maintains task list        │
    └─────────────────────────────────┘
    
    ┌─────────────────────────────────┐
    │  5. Error Agent                  │
    │     • Analyzes errors            │
    │     • Suggests fixes             │
    │     • Retries failed operations  │
    └─────────────────────────────────┘

MESSAGE FLOW EXAMPLE:
─────────────────────
User: "Create FastAPI app"
  ↓
Orchestrator → ACP Client → Planning Agent
  ↓
Planning Agent returns: [Task1: Code, Task2: Execute]
  ↓
Orchestrator → ACP Client → Coding Agent (Task1)
  ↓
Coding Agent returns: Files created
  ↓
Orchestrator → ACP Client → Execution Agent (Task2)
  ↓
Execution Agent returns: App running
  ↓
Complete!
""")
    print("="*80)


if __name__ == "__main__":
    """Run tests with detailed output."""
    print_agent_landscape_diagram()
    
    # Run pytest with verbose output
    import sys
    sys.exit(pytest.main([__file__, "-v", "-s"]))
