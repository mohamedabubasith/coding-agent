import asyncio
import os
import shutil
from unittest.mock import MagicMock, patch
from coding_agent_plugin.agents.orchestrator import OrchestratorAgent

async def test_orchestrator():
    project_id = "test_project_123"
    
    # Mock ChatOpenAI
    with patch("coding_agent_plugin.agents.planning.ChatOpenAI") as MockPlanningLLM, \
         patch("coding_agent_plugin.agents.coding.ChatOpenAI") as MockCodingLLM, \
         patch("coding_agent_plugin.agents.error.ChatOpenAI") as MockErrorLLM:
        
        # Setup mocks
        mock_planning_instance = MockPlanningLLM.return_value
        mock_planning_instance.stream.return_value = [{"content": "Mock plan"}] # For planning agent stream
        
        mock_coding_instance = MockCodingLLM.return_value
        # Make ainvoke awaitable
        future_coding = asyncio.Future()
        future_coding.set_result(MagicMock(content="print('Hello World')"))
        mock_coding_instance.ainvoke.return_value = future_coding
        
        mock_error_instance = MockErrorLLM.return_value
        # Make ainvoke awaitable
        future_error = asyncio.Future()
        future_error.set_result(MagicMock(content="print('Hello World Fixed')"))
        mock_error_instance.ainvoke.return_value = future_error

        # Need to patch create_agent in planning.py as well since it uses it
        with patch("coding_agent_plugin.agents.planning.create_agent") as mock_create_agent:
            mock_agent_executor = MagicMock()
            mock_agent_executor.stream.return_value = [{"content": "Mock plan"}]
            mock_create_agent.return_value = mock_agent_executor
            
            orchestrator = OrchestratorAgent()

            # Clean up previous run
            if os.path.exists(f"projects/{project_id}"):
                shutil.rmtree(f"projects/{project_id}")

            print("Testing Planning Agent...")
            # We need to mock the plan method return value because we mocked the internal agent
            # Actually, let's just mock the plan method of PlanningAgent to simplify
            with patch.object(orchestrator.agents["planning"], "plan", return_value=[{"task": "test", "agent": "coding"}]) as mock_plan:
                await orchestrator.execute("planning", "Create a simple calculator", project_id)
                if os.path.exists(f"projects/{project_id}/planning.md"):
                    print("Planning Agent: SUCCESS")
                else:
                    print("Planning Agent: FAILED")

            print("Testing Coding Agent...")
            await orchestrator.execute("coding", "Write a python function to add two numbers", project_id)
            if os.path.exists(f"projects/{project_id}/generated_code.py"):
                print("Coding Agent: SUCCESS")
            else:
                print("Coding Agent: FAILED")

            print("Testing Task Agent...")
            await orchestrator.execute("task", "Implement addition function", project_id)
            if os.path.exists(f"projects/{project_id}/tasks.md"):
                print("Task Agent: SUCCESS")
            else:
                print("Task Agent: FAILED")
                
            print("Testing Error Agent...")
            # Introduce an error first (manually for test)
            with open(f"projects/{project_id}/generated_code.py", "w") as f:
                f.write("def add(a, b): return a + b + 'error'")
                
            await orchestrator.execute("error", "Fix syntax error", project_id)
            # Since we mocked the return value to "print('Hello World Fixed')", checking for that
            with open(f"projects/{project_id}/generated_code.py", "r") as f:
                content = f.read()
                if "Fixed" in content:
                     print("Error Agent: SUCCESS")
                else:
                     print(f"Error Agent: FAILED. Content: {content}")

            print("Testing Execution Agent...")
            # Write valid code for execution test
            with open(f"projects/{project_id}/generated_code.py", "w") as f:
                f.write("print('Hello from Execution Agent')")
                
            await orchestrator.execute("execution", "Run the code", project_id)
            if os.path.exists(f"projects/{project_id}/execution.md"):
                print("Execution Agent: SUCCESS")
            else:
                print("Execution Agent: FAILED")

if __name__ == "__main__":
    asyncio.run(test_orchestrator())
