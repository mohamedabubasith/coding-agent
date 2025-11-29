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
