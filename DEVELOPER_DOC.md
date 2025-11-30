# Developer Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Agent System](#agent-system)
5. [Project Management](#project-management)
6. [Storage System](#storage-system)
7. [CLI Interface](#cli-interface)
8. [Database Schema](#database-schema)
9. [Development Workflow](#development-workflow)
10. [Testing](#testing)
11. [Deployment](#deployment)

---

## Architecture Overview

Agentic Coder is an autonomous AI-powered project creation and improvement system built around a **multi-agent architecture**. The system uses LLMs (Language Models) to plan, generate, execute, and improve code autonomously.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLI Interface                           │
│            (User Commands via Click/Typer)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                  Project Manager                             │
│          (Database, Storage, Context)                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                 Orchestrator Agent                           │
│            (Coordinates all other agents)                    │
└─────┬─────┬──────┬──────┬──────┬─────────────────────────┬─┘
      │     │      │      │      │                         │
      ▼     ▼      ▼      ▼      ▼                         ▼
   Planning Coding  Task  Exec  Error                  File Modifier
   Agent   Agent   Agent Agent  Agent                     Agent
```

### Key Design Principles

1. **Modularity**: Each agent is self-contained and focused on one task
2. **Persistence**: All projects stored in database with file tracking
3. **Isolation**: Projects are completely isolated from each other
4. **Extensibility**: Easy to add new agents or LLM providers
5. **User Control**: Interactive modes allow human oversight

---

## Project Structure

```
coding-agent-plugin/
├── src/coding_agent_plugin/
│   ├── __init__.py
│   ├── agents/              # All agent implementations
│   │   ├── base_agent.py    # Abstract base class
│   │   ├── orchestrator.py  # Main orchestrator
│   │   ├── planning.py      # Planning agent
│   │   ├── coding.py        # Code generation agent
│   │   ├── task.py          # Task management agent
│   │   ├── execution.py     # Code execution agent
│   │   ├── error.py         # Error fixing agent
│   │   └── file_modifier.py # File modification agent
│   ├── cli/                 # CLI implementation
│   │   └── main.py          # Click commands
│   ├── context/             # Project context management
│   │   └── project_context.py
│   ├── core/                # Core configuration
│   │   ├── config.py        # LLM config & validation
│   │   └── llm_service.py   # LLM interface
│   ├── integrations/        # External integrations
│   │   └── git_manager.py   # Git operations
│   ├── managers/            # Business logic managers
│   │   ├── project_manager.py  # Project CRUD
│   │   └── storage_manager.py  # File storage
│   ├── models/              # Database models
│   │   ├── db_models.py     # SQLAlchemy models
│   │   ├── database.py      # DB connection
│   │   └── project.py       # Pydantic models
│   ├── ui/                  # User interface components
│   │   └── plan_review.py   # Interactive plan review
│   └── utils/               # Utility functions
│       ├── logger.py        # Logging utilities
│       └── validation.py    # Input validation
├── tests/                   # Test suite
├── .env.example            # Environment template
├── pyproject.toml          # Package configuration
└── README.md               # User documentation
```

---

## Core Components

### 1. Configuration System

**Location**: `src/coding_agent_plugin/core/config.py`

**Purpose**: Manage LLM configuration and validate environment variables.

**Key Functions**:
- `validate_llm_config()`: Ensures `LLM_API_KEY` is set
- Environment variables:
  - `LLM_API_KEY`: Required API key
  - `LLM_MODEL`: Model name (default: gpt-4o)
  - `LLM_BASE_URL`: Optional custom endpoint

**Example**:
```python
from coding_agent_plugin.core.config import validate_llm_config

# Validate before LLM operations
validate_llm_config()  # Raises ValueError if missing
```

### 2. LLM Service

**Location**: `src/coding_agent_plugin/core/llm_service.py`

**Purpose**: Abstract interface for LLM providers.

**Supported Providers**:
- OpenAI (GPT-4, GPT-3.5)
- NVIDIA (Qwen, Llama)
- Groq (Llama variants)
- Any OpenAI-compatible API

**Usage**:
```python
from coding_agent_plugin.core.llm_service import create_llm

llm = create_llm()  # Uses environment config
response = await llm.ainvoke("Generate a FastAPI app")
```

---

## Agent System

### Base Agent

**Location**: `src/coding_agent_plugin/agents/base_agent.py`

**Purpose**: Abstract base class for all agents.

**Interface**:
```python
class BaseAgent(ABC):
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
    
    @abstractmethod
    async def execute(self, task: Any) -> Dict:
        """Execute agent task"""
        pass
```

## 🏗️ Agent Architecture

### Core Components

- **`ProjectManager`**: Handles project creation, retrieval, and storage paths. Uses SQLite for metadata and filesystem for code.
- **`OrchestratorAgent`**: The brain of Autonomous Mode. Coordinates other agents.
- **`CodingAgent`**: The worker. Generates and modifies code. Used directly in Direct Mode.
- **`PlanningAgent`**: Creates architectural plans and workflows (`planning.md`).
- **`TaskAgent`**: Manages the project checklist (`tasks.md`), tracking progress in real-time.
- **`ExecutionAgent`**: Runs shell commands and validates outputs.

### Data Flow (Autonomous)

1.  **User Request** -> `OrchestratorAgent`
2.  `Orchestrator` -> `PlanningAgent` (Generates Plan)
3.  `Orchestrator` -> `TaskAgent` (Initializes `tasks.md`)
4.  **Loop**:
    - `Orchestrator` picks next task.
    - `TaskAgent` marks as In Progress.
    - `Orchestrator` -> `CodingAgent` / `ExecutionAgent` (Do work).
    - `TaskAgent` marks as Completed.
5.  **Completion** -> User notified.

### 1. Planning Agent

**Location**: `src/coding_agent_plugin/agents/planning.py`

**Purpose**: Analyze user prompts and create structured project plans.

**What it does**:
1. Takes natural language description
2. Uses LLM to generate:
   - Project architecture
   - File structure
   - Task list with dependencies
3. Outputs JSON plan with tasks

**Input**:
```python
{
    "user_prompt": "Create a FastAPI backend with JWT auth",
    "project_id": "my-api"
}
```

**Output**:
```python
{
    "workflow": {
        "architecture": {...},
        "tasks": [
            {"file": "main.py", "description": "..."},
            {"file": "auth.py", "description": "..."}
        ]
    }
}
```

**LLM Prompt Strategy**:
- System prompt: Instructs to output structured JSON
- User prompt: Contains requirements
- Parsing: Regex extraction of JSON from response

### 2. Coding Agent

**Location**: `src/coding_agent_plugin/agents/coding.py`

**Purpose**: Generate code for individual files based on task descriptions.

**What it does**:
1. Receives file path and description
2. Reads existing file (if exists) for context
3. Uses LLM to generate/update code
4. Saves to project storage via StorageManager

**Key Features**:
- Context-aware (reads existing code)
- Supports multiple languages
- Creates parent directories automatically

**Example Task**:
```python
{
    "file_path": "src/auth.py",
    "description": "JWT authentication with FastAPI",
    "project_id": "my-api",
    "existing_content": "# Previous code..."  # Optional
}
```

### 3. Task Agent

**Location**: `src/coding_agent_plugin/agents/task.py`

**Purpose**: Maintain project task list and track progress.

**What it does**:
- Creates `.agentic/tasks.md` in project
- Logs all tasks from planning
- Can be used to resume interrupted projects

### 4. Execution Agent

**Location**: `src/coding_agent_plugin/agents/execution.py`

**Purpose**: Execute code and shell commands, log results.

**What it does**:
1. Runs Python files or shell commands
2. Captures stdout/stderr
3. Logs to `.agentic/execution.log`
4. Returns success/failure status

**Use Cases**:
- Testing generated code
- Running build scripts
- Installing dependencies

### 5. Error Agent

**Location**: `src/coding_agent_plugin/agents/error.py`

**Purpose**: Automatically fix code errors.

**What it does**:
1. Reads code with errors
2. Takes error message/stack trace
3. Uses LLM to generate fix
4. Updates the file

**Automatic Retry Loop** (in Orchestrator):
- Tries to run code
- If error → Error Agent fixes
- Retries up to 3 times

### 6. File Modifier Agent

**Location**: `src/coding_agent_plugin/agents/file_modifier.py`

**Purpose**: Make surgical modifications to existing files.

**What it does**:
- Takes instruction (e.g., "add type hints")
- Reads existing file
- Generates modified version
- Updates file

**Used by**: `improve` command for iterative improvements

### 7. Orchestrator Agent

**Location**: `src/coding_agent_plugin/agents/orchestrator.py`

**Purpose**: Coordinate all other agents in proper sequence.

**Workflow**:
1. **Planning Phase**:
   - Calls PlanningAgent
   - Gets structured task list

2. **Execution Phase**:
   - For each task:
     - CodingAgent generates code
     - TaskAgent logs task
     - ExecutionAgent tests (optional)
     - ErrorAgent fixes if needed

3. **Completion**:
   - Git commit (if enabled)
   - Return summary

**Key Method**: `run_project(prompt, project_id)`

---

## Project Management

### Project Manager

**Location**: `src/coding_agent_plugin/managers/project_manager.py`

**Purpose**: CRUD operations for projects.

**Database**: SQLite at `~/.agentic-coder/data.db`

**Key Operations**:

#### Create Project
```python
pm = ProjectManager()
project = pm.create_project(
    name="my-api",
    description="FastAPI backend"
)
# Creates:
# - Database entry
# - Directory: ~/.agentic-coder/projects/my-api/
# - Metadata dir: ~/.agentic-coder/projects/my-api/.agentic/
```

#### List Projects
```python
projects = pm.list_projects()
# Returns list of project dictionaries
```

#### Get Project
```python
project = pm.get_project("my-api")  # By name
project = pm.get_project("proj_abc123")  # By ID
```

#### Delete Project
```python
pm.delete_project("my-api")
# Deletes:
# - Database entries (cascades to files/versions)
# - Project directory and all files
```

#### Current Project Context
```python
# Set current project
pm.set_current_project("my-api")

# Get current project
current = pm.get_current_project()
```

---

## Storage System

### Storage Manager

**Location**: `src/coding_agent_plugin/managers/storage_manager.py`

**Purpose**: Manage files within projects.

**File Tracking**: All files tracked in database with:
- Path (relative to project)
- SHA-256 hash
- Size in bytes
- Timestamps

**Key Operations**:

#### Save File
```python
sm = StorageManager()
sm.save_file(
    project_name_or_id="my-api",
    file_path="src/main.py",
    content="print('hello')"
)
# Saves to: ~/.agentic-coder/projects/my-api/src/main.py
# Updates database with hash and size
```

#### Get File
```python
content = sm.get_file("my-api", "src/main.py")
```

#### List Files
```python
files = sm.list_files("my-api")
# Returns: ['src/main.py', 'src/auth.py', 'README.md']
```

#### Delete File
```python
sm.delete_file("my-api", "src/main.py")
```

---

## CLI Interface

### Command Structure

**Framework**: Typer (command-line framework)

**Main Commands**:

#### 1. `init`
Initialize agentic-coder for first use:
```bash
agentic-coder init
```
Creates:
- `~/.agentic-coder/` directory
- SQLite database
- Projects directory

#### 2. `project create`
Create a new project entry:
```bash
agentic-coder project create "my-api"
```

#### 3. `project run`
Execute agent tasks on a project (Autonomous or Direct):
```bash
# Autonomous Mode (Planning -> Coding -> Verification)
agentic-coder project run "Create Login API" --mode autonomous

# Direct Mode (Single file edit)
agentic-coder project run "Fix bug in auth.py" --mode direct --file app/auth.py
```

#### 4. `project list`
List all projects:
```bash
agentic-coder project list
```

#### 8. `project info`
Show project details:
```bash
agentic-coder project info [project-name]
```

---

## Database Schema

### Projects Table
```sql
CREATE TABLE projects (
    id TEXT PRIMARY KEY,              -- proj_abc123
    name TEXT UNIQUE NOT NULL,         -- User-friendly name
    description TEXT,                  -- Optional description
    storage_path TEXT NOT NULL,        -- Full path to project dir
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    project_metadata JSON              -- Extra metadata
);
```

### Project Files Table
```sql
CREATE TABLE project_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,          -- FK to projects
    file_path TEXT NOT NULL,           -- Relative path
    content_hash TEXT,                 -- SHA-256
    size_bytes INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE(project_id, file_path)      -- One entry per file
);
```

### Project Versions Table
```sql
CREATE TABLE project_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,          -- FK to projects
    version INTEGER NOT NULL,
    description TEXT,
    changes JSON,                      -- Change details
    created_at TIMESTAMP
);
```

### User Settings Table
```sql
CREATE TABLE user_settings (
    key TEXT PRIMARY KEY,              -- Setting name
    value TEXT NOT NULL                -- Setting value
);

-- Example row:
-- key='current_project', value='my-api'
```

---

## Development Workflow

### Adding a New Agent

1. **Create agent file**:
```python
# src/coding_agent_plugin/agents/my_agent.py
from coding_agent_plugin.agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    async def execute(self, task):
        # Implementation
        return {"result": "success"}
```

2. **Register in Orchestrator**:
```python
# src/coding_agent_plugin/agents/orchestrator.py
self.agents["my_agent"] = MyAgent("my_agent")
```

3. **Use in workflow**:
```python
result = await self.agents["my_agent"].execute(task_data)
```

### Adding a New CLI Command

1. **Add to CLI**:
```python
# src/coding_agent_plugin/cli/main.py
@app.command()
@click.argument("name")
def my_command(name):
    """Command description"""
    # Implementation
```

2. **Test locally**:
```bash
python -m coding_agent_plugin.cli.main my-command test
```

### Environment Setup

1. **Clone repository**
2. **Create virtual environment**:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. **Install in development mode**:
```bash
pip install -e ".[dev]"
```

4. **Set up environment**:
```bash
cp .env.example .env
# Edit .env with your API keys
```

---

## Testing

### Test Structure
```
tests/
├── test_agents/
│   ├── test_planning.py
│   ├── test_coding.py
│   └── test_orchestrator.py
├── test_managers/
│   ├── test_project_manager.py
│   └── test_storage_manager.py
└── test_cli/
    └── test_commands.py
```

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=coding_agent_plugin

# Specific test
pytest tests/test_agents/test_planning.py

# Verbose
pytest -v
```

### Mocking LLM Calls
```python
from unittest.mock import AsyncMock, patch

@patch('coding_agent_plugin.core.llm_service.ChatOpenAI')
def test_planning_agent(mock_llm):
    mock_llm.return_value.ainvoke = AsyncMock(
        return_value="```json\n{...}\n```"
    )
    # Test logic
```

---

## Deployment

### Building Package
```bash
# Clean previous builds
rm -rf dist/ build/

# Build
python -m build

# Check
twine check dist/*
```

### Publishing to PyPI
```bash
# Test PyPI (optional)
twine upload --repository testpypi dist/*

# Production PyPI
twine upload dist/*
```

### Version Bumping
1. Update `version` in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit and tag:
```bash
git add .
git commit -m "chore: bump version to 0.3.0"
git tag v0.3.0
git push origin main --tags
```

---

## Key Design Decisions

### Why SQLite?
- **Simple**: No separate database server
- **Portable**: Single file database
- **Sufficient**: For single-user local use
- **Upgradeable**: Can migrate to PostgreSQL later

### Why Separate Agents?
- **Modularity**: Easy to test/modify individual agents
- **Reusability**: Agents can be used in different workflows
- **Clarity**: Each agent has single responsibility
- **Extensibility**: Easy to add new agents

### Why Project Isolation?
- **Clean Workspace**: No file conflicts between projects
- **Version Control**: Each project has own Git repo
- **Scalability**: Easy to add cloud storage support
- **Organization**: Natural project boundaries

---

## Future Enhancements

### Planned (v0.4.0+)
- Cloud storage support (MinIO/S3)
- Multi-user support with authentication
- Web UI for project management
- MCP server integration for custom tools
- Project templates library
- CI/CD integration
- Cost tracking per project
- Team collaboration features

### Architecture Changes Needed
- **Auth layer**: User authentication and authorization
- **API layer**: REST API for web UI
- **Cloud storage**: S3-compatible storage interface
- **Real-time updates**: WebSocket support
- **Permissions**: Role-based access control

---

## Troubleshooting

### Common Issues

**Issue**: `NameError: name 'ProjectContext' is not defined`
**Solution**: Import missing at top of file

**Issue**: Database locked
**Solution**: Only one process should access SQLite at a time

**Issue**: LLM API quota exceeded
**Solution**: Use cheaper model or local LLM

**Issue**: Git conflicts
**Solution**: Each project has separate repo, shouldn't conflict

### Debug Mode
```bash
# Set verbose logging
export LOG_LEVEL=DEBUG
agentic-coder create "..." --verbose
```

### Database Inspection
```bash
# Open database
sqlite3 ~/.agentic-coder/data.db

# List projects
SELECT * FROM projects;

# List files for project
SELECT * FROM project_files WHERE project_id = 'proj_abc123';
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

### Code Style
- **Format**: Black formatter
- **Linting**: Ruff
- **Type hints**: Encouraged but not required
- **Docstrings**: Google style

### Pull Request Process
1. Fork repository
2. Create feature branch
3. Make changes with tests
4. Run tests and linting
5. Submit PR with description

---

## License

MIT License - see [LICENSE](LICENSE) file.

---

**Last Updated**: 2024-11-30  
**Version**: 0.3.0  
**Maintainer**: Mohamed Abu Basith
