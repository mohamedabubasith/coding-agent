# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v0.4.0
- **MCP Server Integration**: Connect custom Model Context Protocol servers for extended capabilities
- **Project Templates**: Pre-built templates for FastAPI, Next.js, React, Django, Flask, Express
- **Cost Tracking**: Monitor and control LLM costs with budgets
- **Undo/Redo**: Revert changes easily
- **GitHub Integration**: Direct integration with GitHub repositories

### Under Consideration
- Web UI for visual project creation
- Automatic test generation
- Code review agent
- Multi-agent collaboration
- IDE extensions (VS Code, JetBrains, Vim)
- Multi-language support
- Cloud deployment integration

## [0.3.23] - 2024-11-30

### Improved
- **Architectural Awareness**: Agents now analyze existing project structure to maintain consistency in naming and patterns (e.g., using `routers.py` if established).
- **Import Logic**: `CodingAgent` now uses the actual file list to generate correct relative imports, preventing hallucinated modules.
- **Iterative Workflow**: Fixed a bug where follow-up tasks would overwrite files instead of modifying them.

### Fixed
- **DB Path**: Fixed `db_path` property to correctly handle non-SQLite database URLs.
- **Task Execution**: Fixed `file_path` extraction in `CodingAgent` to handle nested task details.

## [0.3.22] - 2024-11-30

### Added
- **CLI Restructuring**: Introduced `agentic-coder init` and `agentic-coder project run` commands.
- **Project-Centric Workflow**: Decoupled project creation from agent execution for better control.
- **Environment Initialization**: `init` command now sets up the database and project directories.

## [0.3.21] - 2024-11-30

### Fixed
- **PyPI Upload**: Bumped version to 0.3.21 to resolve potential version conflict.

## [0.3.20] - 2024-11-30

### Fixed
- **PyPI Upload**: Bumped version to resolve TestPyPI upload conflict.

## [0.3.19] - 2024-11-30

### Added
- **Task Tracking**: Upgraded `TaskAgent` to create and maintain a `tasks.md` checklist in the project's `.agentic` directory. The `Orchestrator` now updates this file in real-time (marking tasks as `[/]` in progress and `[x]` completed), providing a live progress log similar to the Antigravity workflow.

## [0.3.18] - 2024-11-30

### Fixed
- **Artifact Generation**: Fixed `PlanningAgent` to correctly resolve the project path using `ProjectManager` when saving `planning.md`. This ensures artifacts are saved in the correct `.agentic` directory even when using custom project locations.

## [0.3.17] - 2024-11-30

### Fixed
- **Indentation Error**: Fixed an `IndentationError` in `PlanningAgent` that caused the CLI to crash in autonomous mode.

## [0.3.16] - 2024-11-30

### Refactored
- **Default Configuration**: Simplified `AGENTIC_PROJECTS_DIR` logic. It now defaults to `~/.agentic-coder/projects` directly in `config.py` if the environment variable is not set, ensuring a valid path is always available without complex fallback logic in `ProjectManager`.

## [0.3.15] - 2024-11-30

### Refactored
- **Configuration**: Moved `AGENTIC_PROJECTS_DIR` handling to `core/config.py` to maintain clean code structure and centralization of configuration settings.

## [0.3.14] - 2024-11-30

### Added
- **Configurable Project Location**: Added support for `AGENTIC_PROJECTS_DIR` environment variable. Users can now specify exactly where projects should be stored (e.g., `./projects` for local storage) instead of the default `~/.agentic-coder/projects`.

## [0.3.13] - 2024-11-30

### Changed
- **Project ID Format**: Removed `proj_` prefix and truncation from Project ID generation. Now uses standard full UUID string (e.g., `550e8400-e29b-41d4-a716-446655440000`) for both database ID and folder name.

## [0.3.12] - 2024-11-30

### Fixed
- **Planning Agent**: Updated system prompt to strictly define agent roles. `TaskAgent` is no longer assigned file creation tasks, preventing "Missing user_prompt" errors during autonomous execution.

## [0.3.11] - 2024-11-30

### Changed
- **Project Folder Naming**: Changed project folder naming convention to use the database-generated **Project ID** (e.g., `proj_xyz123`) instead of the sanitized project name. This ensures guaranteed uniqueness and avoids any filesystem naming conflicts.

## [0.3.10] - 2024-11-30

### Added
- **Retry Logic**: Added configurable retry logic for LLM calls with exponential backoff.
  - `AGENT_MAX_RETRIES`: Configurable via env (default: 3).
  - `AGENT_RETRY_DELAY`: Configurable via env (default: 2s).
- **Robust Sanitization**: Enhanced project name sanitization to strictly allow only alphanumeric characters and hyphens, preventing filesystem issues.

## [0.3.9] - 2024-11-30

### Fixed
- **File Saving**: Fixed `CodingAgent.save_code` still using hardcoded relative path. Now correctly uses `ProjectManager` to resolve the absolute storage path.

## [0.3.8] - 2024-11-30

### Fixed
- **Execution Agent**: Fixed `object str can't be used in 'await' expression` by making `run_command` and `run_code` asynchronous and using `run_in_executor` to prevent blocking the event loop.

## [0.3.7] - 2024-11-30

### Fixed
- **Orchestrator Import**: Fixed `NameError: name 'ProjectManager' is not defined` in `OrchestratorAgent` by adding missing import.

## [0.3.6] - 2024-11-30

### Fixed
- **File Storage Paths**: Fixed critical issue where files were being written to relative `projects/` directory instead of the configured `~/.agentic-coder/projects/` directory. Updated `CodingAgent`, `OrchestratorAgent`, and `ExecutionAgent` to use absolute paths from `ProjectManager`.

## [0.3.5] - 2024-11-30

### Fixed
- **Autonomous Mode Output**: Fixed `TypeError: 'Project' object is not subscriptable` in autonomous mode success message.

## [0.3.4] - 2024-11-30

### Fixed
- **Autonomous Mode**: Fixed `TypeError: 'Project' object is not subscriptable` in autonomous mode by correctly accessing project attributes.

## [0.3.3] - 2024-11-30

### Fixed
- **Direct Mode Output**: Fixed `TypeError: 'Project' object is not subscriptable` by correctly accessing project attributes in the success message.

## [0.3.2] - 2024-11-30

### Fixed
- **Direct Mode Execution**: Fixed `ValueError: Missing user_prompt` by correctly passing `user_prompt` instead of `description` to `CodingAgent`.

## [0.3.1] - 2024-11-30

### Added
- **Two-Mode System** for project creation:
  - `direct` mode: Quick code generation without planning (skips `PlanningAgent`).
  - `autonomous` mode: Full planning and orchestration (default).
- **CLI Updates**: Added `--mode` flag to `create` command.
- **Smart Filename Inference**: Automatically infers target filename from prompt in `direct` mode.

### Fixed
- **Git Initialization Path**: Fixed issue where git init was trying to use a hardcoded path instead of the project's storage path.
- **Success Message**: Updated success message to show correct project location.

## [0.3.0] - 2024-11-30

### Added
- **Project Management System** - Complete project lifecycle management
  - `agentic-coder init` - First-time setup
  - `agentic-coder project create` - Create new projects
  - `agentic-coder project list` - List all projects
  - `agentic-coder project switch` - Switch between projects
  - `agentic-coder project delete` - Delete projects
  - `agentic-coder project info` - Show project details
- **Database Layer** - SQLite-based persistent storage
  - Projects table with metadata
  - Project files tracking with hashes
  - Project versions for history
  - User settings storage
- **Project Isolation** - Each project in separate directory
  - Located in `~/.agentic-coder/projects/`
  - Database-backed file tracking
  - Project-specific metadata
- **Storage Manager** - File operations within projects
  - Save/retrieve files
  - Content hashing (SHA-256)
  - Size tracking
  - List project files
- **Developer Documentation** - Complete DEVELOPER_DOC.md
  - Architecture overview
  - All agents explained
  - Database schema
  - Development workflow

### Changed
- Projects now stored in `~/.agentic-coder/projects/` instead of `./projects/`
- CLI commands now support `--project` flag
- Current project context tracking

### Fixed
- CLI command name correctly set to `agentic-coder`
- SQLAlchemy reserved word conflict (`metadata` → `project_metadata`)
- Session detachment issues with ORM objects

## [0.2.1] - 2024-11-30

### Fixed
- **CRITICAL**: Fixed CLI command name from `coding-agent` to `agentic-coder`
  - Package now correctly installs `agentic-coder` command
  - Previous version (0.2.0) had incorrect command name

## [0.2.0] - 2024-11-30

### Changed
- Improved README with cleaner, more focused content
- Added comprehensive .gitignore file
- Added project logo and banner
- Updated GitHub repository URLs to correct repository
- Enhanced roadmap section with detailed upcoming features
- Cleaned up documentation files

### Added
- Professional branding (logo.png, banner.png)
- MIT License information in README
- Comprehensive .gitignore for Python projects

## [0.1.0] - 2024-11-29

### Added
- **Autonomous Project Creation**: Create complete projects from natural language prompts
- **Interactive Planning Review**: Review and approve architectural plans before generation
- **Iterative Improvement System**: Continuously improve existing projects with `improve` command
- **Multi-Agent Orchestration**: Specialized agents for planning, coding, execution, and error fixing
- **Beautiful CLI Interface**: Rich terminal UI with progress bars, colors, and interactive prompts
- **Git Integration**: Automatic repository initialization and commit tracking
- **Multi-Provider Support**: Works with OpenAI, NVIDIA, Groq, OpenRouter, and local models
- **Context-Aware Coding**: Agents understand existing code for intelligent modifications
- **Error Handling & Retry Logic**: Automatic error detection and recovery up to 2 retries
- **Input Validation**: Comprehensive validation of user inputs for safety
- **Logging System**: Structured logging with file outputs for debugging
- **Project Context Management**: Understands and analyzes existing project structures
- **Conversation History**: Tracks all improvements in `.agent_context/conversation.json`
- **Hidden Internal Files**: Clean workspace with internal files in `.agent_context/`

### Features
- CLI commands:
  - `create`: Generate new projects
  - `improve`: Iteratively enhance existing projects
  - `templates`: List available templates (coming soon)
- Command options:
  - `--interactive`: Review plans before execution
  - `--model`: Specify LLM model
  - `--provider`: Specify LLM provider
  - `--git` / `--no-git`: Control git initialization
  - `--verbose`: Detailed logging output
  - `--dry-run`: Preview changes without applying (improve command)
  - `--file`: Target specific files (improve command)

### Documentation
- Comprehensive README with examples
- User Guide for complete workflows
- Product Roadmap for future features
- PyPI Publishing Guide
- Contributing Guidelines (coming soon)

### Internal Improvements
- Type hints throughout codebase
- Proper error handling with try-catch blocks
- Validation utilities for user inputs
- Centralized logging system
- Clean code organization
- Git-based version control for projects

### Dependencies
- langchain >= 1.1.0
- langchain-openai >= 1.1.0
- click >= 8.1.0
- rich >= 13.7.0
- gitpython >= 3.1.0
- python-dotenv >= 1.0.0
- pydantic >= 2.8.0

[0.1.0]: https://github.com/mohamedabubasith/coding-agent/releases/tag/v0.1.0
