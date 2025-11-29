# Coding Agent Plugin 🤖

<p align="center">
  <img src="artifacts/coding_agent_logo.webp" alt="Coding Agent Plugin Logo" width="200"/>
</p>

<p align="center">
  <strong>Your AI-Powered Project Creator & Iterative Developer</strong>
</p>

<p align="center">
  <a href="https://github.com/abuabbasit/coding-agent-plugin"><img src="https://img.shields.io/github/stars/abuabbasit/coding-agent-plugin?style=social" alt="GitHub stars"></a>
  <a href="https://pypi.org/project/coding-agent-plugin/"><img src="https://img.shields.io/pypi/v/coding-agent-plugin" alt="PyPI version"></a>
  <a href="https://pypi.org/project/coding-agent-plugin/"><img src="https://img.shields.io/pypi/dm/coding-agent-plugin" alt="Downloads"></a>
  <a href="https://github.com/abuabbasit/coding-agent-plugin/blob/main/LICENSE"><img src="https://img.shields.io/github/license/abuabbasit/coding-agent-plugin" alt="License"></a>
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
coding-agent create "FastAPI backend with JWT auth, PostgreSQL, and OAuth"
```

### 🔄 Iterative Improvement
Continuously improve your project with natural language requests.

```bash
coding-agent improve "add email verification"
coding-agent improve "add comprehensive tests"
coding-agent improve "optimize database queries"
```

### 🎨 Interactive Planning
Review and approve plans before generation. See what will be built before committing.

```bash
coding-agent create "My App" --interactive
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
pip install coding-agent-plugin
```

Or install from source:

```bash
git clone https://github.com/abuabbasit/coding-agent-plugin.git
cd coding-agent-plugin
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
coding-agent create "FastAPI Todo App with SQLite"

# With interactive planning
coding-agent create "React Dashboard" --interactive

# Using specific model
coding-agent create "Django Blog" --model gpt-3.5-turbo
```

### Improve Existing Project

```bash
# Navigate to your project
cd projects/my_project/

# Make improvements
coding-agent improve "add authentication"
coding-agent improve "add comprehensive logging"

# Interactive mode
coding-agent improve --interactive
```

## 📚 Usage Examples

### Example 1: Create a Complete Backend

```bash
coding-agent create "FastAPI backend with:
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
coding-agent create "Simple Flask API"

# Navigate to project
cd projects/simple_flask_api/

# Add features incrementally
coding-agent improve "add user registration endpoint"
coding-agent improve "add email validation"
coding-agent improve "add rate limiting"
coding-agent improve "add comprehensive error handling"

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
git clone https://github.com/abuabbasit/coding-agent-plugin.git
cd coding-agent-plugin

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

- 🐛 [Report a bug](https://github.com/abuabbasit/coding-agent-plugin/issues)
- 💡 [Request a feature](https://github.com/abuabbasit/coding-agent-plugin/issues)
- 💬 [Join discussions](https://github.com/abuabbasit/coding-agent-plugin/discussions)

## 🎯 Roadmap

See our [Roadmap](ROADMAP.md) for upcoming features including:
- 📦 Built-in project templates
- 🧪 Automatic test generation
- 📊 Cost tracking and budgets
- 🔌 Plugin system
- 🌐 Web UI
- And much more!

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/abuabbasit">Mohamed Abu Basith</a>
</p>

<p align="center">
  <a href="https://github.com/abuabbasit/coding-agent-plugin">⭐ Star us on GitHub</a> • 
  <a href="https://pypi.org/project/coding-agent-plugin/">📦 Install from PyPI</a>
</p>
