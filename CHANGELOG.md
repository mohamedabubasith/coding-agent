# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v0.2.0
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
