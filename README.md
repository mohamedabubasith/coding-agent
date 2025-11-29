# Coding Agent Plugin

A modular, autonomous agent orchestration system for end-to-end software development. This plugin orchestrates multiple specialized agents (Planning, Coding, Task, Error, Execution) to generate, plan, code, fix, and execute entire software projects.

## Features

- **Autonomous Orchestration**: Automatically manages the full software development lifecycle (Planning -> Scaffolding -> Coding -> Verification).
- **Self-Healing**: Automatic error detection and recovery using the ErrorAgent. Failed tasks are automatically retried after fixes.
- **Multi-Agent System**:
    -   **Planning Agent**: Architects the solution and creates a detailed task list using LLMs.
    -   **Coding Agent**: Generates code and updates existing files (context-aware).
    -   **Task Agent**: Manages project structure and task tracking.
    -   **Error Agent**: Identifies and fixes errors in code automatically.
    -   **Execution Agent**: Runs builds, tests, and shell commands to verify functionality.
- **Persistent Storage**: All project files are stored in a `projects/{project_id}` directory.
- **Hidden Context Files**: Internal files (`.agent_context/planning.md`, `tasks.md`, `execution.md`) are hidden to keep the workspace clean.
- **Configurable Models**: Support for different LLM models (e.g., `gpt-4o`, `gpt-3.5-turbo`) via environment variables.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-repo/coding-agent-plugin.git
    cd coding-agent-plugin
    ```

2.  Install dependencies:
    ```bash
    pip install -e .
    ```

3.  Set up environment variables:
    Create a `.env` file in the root directory:
    ```env
    OPENAI_API_KEY=your_api_key_here
    LLM_MODEL=gpt-4o  # Optional: Defaults to gpt-4o, use gpt-3.5-turbo for lower cost
    ```

## Usage

### Autonomous Mode (Recommended)

The autonomous mode automatically plans, scaffolds, codes, verifies, and fixes errors:

```python
import asyncio
from coding_agent_plugin.agents.orchestrator import OrchestratorAgent

async def main():
    orchestrator = OrchestratorAgent()
    
    # Create a full-stack Todo App with automatic error handling
    await orchestrator.execute(
        mode="autonomous",
        user_prompt="Create a FastAPI backend with login and register endpoints",
        project_id="auth_backend_v1"
    )

if __name__ == "__main__":
    asyncio.run(main())
```

**What happens:**
1. **Planning**: LLM generates a comprehensive plan with architecture and task list
2. **Execution**: Each task is executed step-by-step (scaffolding, coding, verification)
3. **Error Handling**: If any task fails, ErrorAgent automatically attempts to fix it (up to 2 retries)
4. **Results**: All generated files are saved in `projects/auth_backend_v1/`

### Manual Mode

You can also interact with specific agents:

```python
# Generate a plan
await orchestrator.execute("planning", "Create a calculator", "calc_project")

# Generate code
await orchestrator.execute("coding", "Write a python function to add numbers", "calc_project")
```

## Project Structure

Projects are created in the `projects/` directory:

```
projects/
  ├── todo_app_v1/
  │   ├── planning.md       # Project plan and architecture
  │   ├── tasks.md          # Task tracking
  │   ├── execution.md      # Execution logs
  │   ├── backend/          # Generated backend code
  │   │   └── main.py
  │   └── frontend/         # Generated frontend code
  │       └── index.html
```

## Contributing

Contributions are welcome! Please submit a pull request.
