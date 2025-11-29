# Agentic Coder 🤖

<p align="center">
  <img src="banner.png" alt="Agentic Coder Banner" width="100%"/>
</p>

<p align="center">
  <img src="logo.png" alt="Agentic Coder Logo" width="200"/>
</p>

<p align="center">
  <strong>Your AI-Powered Project Creator & Iterative Developer</strong>
</p>

<p align="center">
  <a href="https://github.com/abuabbasit/agentic-coder"><img src="https://img.shields.io/github/stars/abuabbasit/agentic-coder?style=social" alt="GitHub stars"></a>
  <a href="https://pypi.org/project/agentic-coder/"><img src="https://img.shields.io/pypi/v/agentic-coder" alt="PyPI version"></a>
  <a href="https://pypi.org/project/agentic-coder/"><img src="https://img.shields.io/pypi/dm/agentic-coder" alt="Downloads"></a>
  <a href="https://github.com/abuabbasit/agentic-coder/blob/main/LICENSE"><img src="https://img.shields.io/github/license/abuabbasit/agentic-coder" alt="License"></a>
</p>

---

## 🚀 What is Coding Agent Plugin?

**Coding Agent Plugin** is an autonomous AI-powered tool that creates complete, production-ready projects from natural language descriptions. Unlike traditional code generators, it doesn't just scaffold - it **thinks, plans, codes, verifies, and iteratively improves** your projects.

Think of it as having an AI pair programmer that:
- 🧠 **Understands** your requirements
- 📋 **Plans** the architecture
- 💻 **Writes** production-ready code
- ✅ **Tests** and verifies everything works
- 🔄 **Iteratively improves** based on your feedback

## ✨ Key Features

### 🎯 Autonomous Project Creation
Create complete projects from a single prompt. No manual scaffolding, no boilerplate copying.

```bash
agentic-coder create "FastAPI backend with JWT auth, PostgreSQL, and OAuth"
```

### 🔄 Iterative Improvement
Continuously improve your project with natural language requests.

```bash
agentic-coder improve "add email verification"
agentic-coder improve "add comprehensive tests"
agentic-coder improve "optimize database queries"
```

### 🎨 Interactive Planning
Review and approve plans before generation. See what will be built before committing.

```bash
agentic-coder create "My App" --interactive
```

### 📦 Multi-Agent System
- **Planning Agent**: Architects your solution
- **Coding Agent**: Writes context-aware code
- **File Modifier**: Makes surgical edits to existing files
- **Execution Agent**: Runs and verifies your code
- **Error Agent**: Automatically fixes issues

### 🎭 Beautiful CLI
- Rich terminal UI with progress bars
- Color-coded output
- Clear error messages
- Interactive prompts

### 🔐 Version Control Built-in
- Auto-initializes Git repository
- Commits each change automatically
- Easy rollback with `git revert`
- Full change history

### 🌐 Multi-Provider Support
Works with any OpenAI-compatible API:
- OpenAI (GPT-4, GPT-3.5)
- NVIDIA AI
- Groq
- OpenRouter
- Local models (Ollama, LM Studio)

## 📦 Installation

```bash
pip install agentic-coder
```

Or install from source:

```bash
git clone https://github.com/abuabbasit/agentic-coder.git
cd agentic-coder
pip install -e .
```

## ⚙️ Configuration

Create a `.env` file in your project root:

```env
# Required
LLM_API_KEY=your_api_key_here

# Optional
LLM_MODEL=gpt-4o                          # Default model
LLM_BASE_URL=https://api.openai.com/v1   # API endpoint
```

## 🎯 Quick Start

### Create Your First Project

```bash
# Simple creation
agentic-coder create "FastAPI Todo App with SQLite"

# With interactive planning
agentic-coder create "React Dashboard" --interactive

# Using specific model
agentic-coder create "Django Blog" --model gpt-3.5-turbo
```

### Improve Existing Project

```bash
# Navigate to your project
cd projects/my_project/

# Make improvements
agentic-coder improve "add authentication"
agentic-coder improve "add comprehensive logging"

# Interactive mode
agentic-coder improve --interactive
```

## 📚 Usage Examples

### Example 1: Create a Complete Backend

```bash
agentic-coder create "FastAPI backend with:
- User authentication (JWT)
- CRUD operations for todos
- PostgreSQL database
- Pydantic validation
- Comprehensive tests
- API documentation" --interactive
```

**Result:**
```
projects/fastapi_backend/
├── app/
│   ├── main.py          # FastAPI app with all endpoints
│   ├── auth.py          # JWT authentication
│   ├── models.py        # SQLAlchemy models
│   ├── database.py      # DB connection
│   ├── crud.py          # CRUD operations
│   └── requirements.txt # All dependencies
├── tests/
│   └── test_main.py     # Comprehensive tests
└── .git/                # Git repository initialized
```

### Example 2: Iterative Development

```bash
# Create initial project
agentic-coder create "Simple Flask API"

# Navigate to project
cd projects/simple_flask_api/

# Add features incrementally
agentic-coder improve "add user registration endpoint"
agentic-coder improve "add email validation"
agentic-coder improve "add rate limiting"
agentic-coder improve "add comprehensive error handling"

# Check what changed
git log --oneline
```

### Example 3: Use with Different Providers

**OpenAI:**
```bash
# .env
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4o
```

**NVIDIA:**
```bash
# .env
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_API_KEY=nvapi-...
LLM_MODEL=qwen/qwen3-next-80b-a3b-instruct
```

**Groq:**
```bash
# .env
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_API_KEY=gsk_...
LLM_MODEL=llama-3.3-70b-versatile
```

## 🎓 Documentation

- [User Guide](USER_GUIDE.md) - Complete walkthrough
- [Roadmap](ROADMAP.md) - Future features
- [Contributing](CONTRIBUTING.md) - How to contribute

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           CLI (User Interface)              │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Orchestrator Agent                  │
│  (Manages workflow and agent coordination)  │
└─────┬─────┬─────┬─────┬─────┬──────────────┘
      │     │     │     │     │
      ▼     ▼     ▼     ▼     ▼
    Plan  Code  Task  Exec  Error
    Agent Agent Agent Agent Agent
```

## 💰 Cost Estimation

Typical costs with GPT-4:
- **Create Project**: $0.10 - $0.30 per project
- **Improve**: $0.04 - $0.10 per improvement

Use cheaper models to reduce costs:
- GPT-3.5-turbo: ~10x cheaper
- NVIDIA/Groq: Often free or very cheap
- Local models: Free!

## 🤝 Contributing

We love contributions! Please read our [Contributing Guide](CONTRIBUTING.md) to get started.

### Development Setup

```bash
# Clone repository
git clone https://github.com/abuabbasit/agentic-coder.git
cd agentic-coder

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run CLI locally
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python3 -m coding_agent_plugin.cli.main --help
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- CLI powered by [Click](https://click.palletsprojects.com/)
- Beautiful UI with [Rich](https://github.com/Textualize/rich)
- Inspired by [Devin](https://www.cognition.ai/), [v0](https://v0.dev/), and [Bolt.new](https://bolt.new/)

## 📧 Support

- 🐛 [Report a bug](https://github.com/abuabbasit/agentic-coder/issues)
- 💡 [Request a feature](https://github.com/abuabbasit/agentic-coder/issues)
- 💬 [Join discussions](https://github.com/abuabbasit/agentic-coder/discussions)

## 🎯 Roadmap & Upcoming Features

We're constantly improving Agentic Coder! Here's what's coming next:

### 🚀 Version 0.2.0 (Next Release)

#### 🔌 MCP Server Integration
**Add your own tools and context!** Connect custom [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers to extend agent capabilities:

```bash
# .env
MCP_SERVERS=filesystem,database,slack

# Configure MCP servers
[mcp.filesystem]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed"]

[mcp.database]
command = "npx" 
args = ["-y", "@modelcontextprotocol/server-postgres", "postgresql://..."]
```

**Use Cases:**
- 📁 **File System Access**: Read/write project files
- 🗄️ **Database**: Query your database for context
- 💬 **Slack/Discord**: Fetch team discussions
- 🌐 **Web Scraping**: Get real-time documentation
- 🔧 **Custom Tools**: Build your own MCP servers

#### 📦 Project Templates
Pre-built templates for common project types:
- FastAPI CRUD API
- Next.js with Auth
- React Dashboard
- Django Blog
- Flask Microservice
- Express.js API

```bash
agentic-coder create --template fastapi-crud "My API"
agentic-coder templates list
```

#### 📊 Cost Tracking & Budgets
Monitor and control LLM costs:
```bash
agentic-coder create "App" --max-cost 1.00
agentic-coder cost show  # View usage
```

### 🔮 Version 0.3.0 (Future)

#### 🌐 Web UI
Browser-based interface:
- Visual project creation
- Real-time code preview
- Interactive planning
- Deployment integration

#### 🧪 Automatic Test Generation
AI-powered test creation:
- Unit tests
- Integration tests  
- E2E tests
- Test coverage optimization

#### 🔍 Code Review Agent
Automated code quality checks:
- Security vulnerability scanning
- Performance optimization suggestions
- Best practices enforcement
- Documentation quality checks

### 🎨 Version 0.4.0 (Further Out)

#### 🤖 Multi-Agent Collaboration
Multiple specialized agents working together:
- Frontend specialist
- Backend specialist
- Database architect
- DevOps engineer

#### 📱 IDE Extensions
- VS Code extension
- JetBrains plugin
- Vim/Neovim plugin

#### 🌍 Language Support
Beyond Python:
- JavaScript/TypeScript
- Go
- Rust
- Java
- C#

#### ☁️ Cloud Deployment Integration
One-command deployment:
```bash
agentic-coder deploy --platform vercel
agentic-coder deploy --platform aws
```

### 💡 Community Requested Features

Vote for features you want on our [GitHub Discussions](https://github.com/abuabbasit/agentic-coder/discussions)!

**Top Requests:**
1. ⭐ **MCP Server Support** (In Progress - v0.2.0)
2. ⭐ **Project Templates** (In Progress - v0.2.0)
3. 🔄 **Undo/Redo Changes**
4. 📸 **Project Snapshots**
5. 🔗 **GitHub Integration**
6. 🎨 **Custom Themes**
7. 🌐 **Multi-language Support**

### 🛠️ How to Contribute

Want to help build these features? Check out our [Contributing Guide](CONTRIBUTING.md)!

---


<p align="center">
  Made with ❤️ by <a href="https://github.com/abuabbasit">Mohamed Abu Basith</a>
</p>

<p align="center">
  <a href="https://github.com/abuabbasit/agentic-coder">⭐ Star us on GitHub</a> • 
  <a href="https://pypi.org/project/agentic-coder/">📦 Install from PyPI</a>
</p>
