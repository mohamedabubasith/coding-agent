# Agentic Coder 🤖

<p align="center">
  <img src="banner.png" alt="Agentic Coder Banner" width="100%"/>
</p>

<p align="center">
  <img src="logo.png" alt="Agentic Coder Logo" width="200"/>
</p>

<p align="center">
  <a href="https://pypi.org/project/agentic-coder/">
    <img src="https://img.shields.io/pypi/v/agentic-coder?color=blue&style=for-the-badge" alt="PyPI version"/>
  </a>
  <a href="https://github.com/mohamedabubasith/coding-agent/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/mohamedabubasith/coding-agent?style=for-the-badge" alt="License"/>
  </a>
</p>

<p align="center">
  <strong>Your AI-Powered Project Creator & Iterative Developer</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/agentic-coder/"><img src="https://img.shields.io/pypi/v/agentic-coder" alt="PyPI version"></a>
  <a href="https://pypi.org/project/agentic-coder/"><img src="https://img.shields.io/pypi/dm/agentic-coder" alt="Downloads"></a>
  <a href="https://github.com/mohamedabubasith/coding-agent/blob/main/LICENSE"><img src="https://img.shields.io/github/license/mohamedabubasith/coding-agent" alt="License"></a>
</p>

---

## What is Agentic Coder?

**Agentic Coder** creates complete, production-ready projects from natural language descriptions. It thinks, plans, codes, tests, and iteratively improves your projects.

## ✨ Features

- **🤖 Two Powerful Modes**:
    - **Direct Mode**: Quick, single-file code generation and modification.
    - **Autonomous Mode**: Full project orchestration with planning, execution, and task tracking.
- **🧠 Intelligent Planning**: Break down complex requirements into actionable steps.
- **📋 Live Task Tracking**: Real-time progress updates via `tasks.md` checklist.
- **💾 Organized Workspace**: Projects are stored cleanly with hidden artifacts (`.agentic/`) keeping your code clutter-free.
- **🔌 Extensible**: Use as a CLI tool or import as a Python package.
- **🛠️ Configurable**: Customize storage location, LLM providers, and more.

## 🚀 Installation

```bash
pip install agentic-coder
```

## ⚙️ Configuration

Create a `.env` file or set environment variables:

```bash
# Required
OPENAI_API_KEY=sk-...

# Optional
AGENTIC_PROJECTS_DIR=~/.agentic-coder/projects  # Custom storage location
LLM_MODEL=gpt-4o                                # Default model
```

### Usage

**1. Initialize Environment:**
```bash
agentic-coder init
```

**2. Create a Project:**
```bash
agentic-coder project create my-app
```

**3. Run the Agent:**
```bash
agentic-coder project run "Build a FastAPI backend with JWT auth"
```

**4. Manage Projects:**
```bash
agentic-coder project list
agentic-coder project switch my-app
agentic-coder project info
```

**Quick Start (Legacy):**
```bash
agentic-coder create "FastAPI backend" --mode autonomous
```

## Examples

### Create a Full-Stack Project
```bash
agentic-coder create "FastAPI backend with:
- User authentication (JWT)
- CRUD operations for todos
- PostgreSQL database
- Comprehensive tests" --mode autonomous
```

### Iteratively Improve
```bash
cd projects/my_app/
agentic-coder improve "add rate limiting"
agentic-coder improve "add logging"
agentic-coder improve "optimize database queries"
```

### 📦 Python Package

Integrate `agentic-coder` into your own tools:

```python
import asyncio
from coding_agent_plugin.managers import ProjectManager
from coding_agent_plugin.agents import OrchestratorAgent, CodingAgent

async def main():
    pm = ProjectManager()
    
    # 1. Direct Mode (Single File Generation)
    # Best for quick scripts or specific file creation
    project = pm.create_project("MyScript", "Simple Script")
    coder = CodingAgent()
    await coder.execute({
        "user_prompt": "Create hello.py",
        "project_id": project['id']
    })
    
    # 2. Autonomous Mode (Full Project Orchestration)
    # Best for complex applications requiring planning and multiple files
    auto_project = pm.create_project("MyApp", "Complex App")
    orchestrator = OrchestratorAgent()
    await orchestrator.run_project(
        user_prompt="Build a calculator app with tests",
        project_id=auto_project['id']
    })

if __name__ == "__main__":
    asyncio.run(main())
```

## Supported LLM Providers

**OpenAI:**
```env
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4o
```

**NVIDIA:**
```env
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_API_KEY=nvapi-...
LLM_MODEL=qwen/qwen3-next-80b-a3b-instruct
```

**Groq:**
```env
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_API_KEY=gsk_...
LLM_MODEL=llama-3.3-70b-versatile
```

## Documentation

- [User Guide](USER_GUIDE.md) - Complete walkthrough
- [Roadmap](ROADMAP.md) - Upcoming features
- [Contributing](CONTRIBUTING.md) - How to contribute
- [Publishing Guide](PUBLISHING.md) - PyPI deployment

## Roadmap

### Upcoming Features
- 🔌 **MCP Server Integration** - Connect custom tools and context
- 📦 **Project Templates** - Pre-built templates (FastAPI, Next.js, React, etc.)
- 📊 **Cost Tracking** - Monitor and control LLM costs
- 🔄 **Undo/Redo** - Easy change rollback

[See full roadmap](ROADMAP.md)

## Support

- 🐛 [Report a bug](https://github.com/mohamedabubasith/coding-agent/issues)
- 💡 [Request a feature](https://github.com/mohamedabubasith/coding-agent/issues)
- 💬 [Discussions](https://github.com/mohamedabubasith/coding-agent/discussions)

## License

This project is licensed under the **MIT License**.

**What this means:**
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ⚠️ Provided "as is" without warranty

See the [LICENSE](LICENSE) file for full details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/mohamedabubasith">Mohamed Abu Basith</a>
</p>

<p align="center">
  <a href="https://github.com/mohamedabubasith/coding-agent">⭐ Star us on GitHub</a> • 
  <a href="https://pypi.org/project/agentic-coder/">📦 Install from PyPI</a>
</p>
