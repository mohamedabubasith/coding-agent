# Coding Agent Plugin - Product Roadmap

## Current State ✅
- ✅ Autonomous project creation (Planning → Coding → Verification)
- ✅ Multi-agent orchestration
- ✅ Error handling and retry logic
- ✅ Support for multiple LLM providers (OpenAI, NVIDIA, etc.)
- ✅ Context-aware coding
- ✅ Hidden internal files
- ✅ CLI Interface (init, project create, project run)
- ✅ Git Integration (Auto-init)
- ✅ Iterative Development (Follow-up tasks)

## User Experience Improvements

### 🎯 Priority 1: CLI Interface (Critical)
**Why:** Users expect a simple `npx create-react-app` style experience, not Python imports.

**Features:**
```bash
# Install globally
pip install agentic-coder

# Simple usage
agentic-coder create "FastAPI login backend" --output ./my-project

# Interactive mode
agentic-coder init  # Asks questions, then creates project

# With options
agentic-coder create "React Todo App" \
  --framework react \
  --backend fastapi \
  --db postgresql \
  --interactive  # Show plan, ask for approval
```

**Implementation:**
- Create `src/coding_agent_plugin/cli.py` with Click or Typer
- Add `console_scripts` entry point in `pyproject.toml`
- Support `--verbose`, `--model`, `--provider` flags

---

### 🎯 Priority 2: Interactive Planning Review
**Why:** Users want to see and approve the plan before code generation starts.

**Features:**
- Show the generated plan in a nice table format
- Allow users to:
  - ✅ Approve and continue
  - ✏️ Edit specific tasks
  - ➕ Add new tasks
  - 🗑️ Remove tasks
  - 🔄 Regenerate plan

**Example:**
```
📋 Generated Plan for "FastAPI Login Backend"

Architecture:
  ├── app/
  │   ├── main.py
  │   ├── models.py
  │   ├── auth.py
  │   └── database.py
  └── requirements.txt

Tasks:
  1. [scaffold] Create app/ directory
  2. [coding] Generate requirements.txt
  3. [coding] Create database.py with SQLAlchemy setup
  4. [coding] Create User model in models.py
  5. [coding] Implement auth.py with JWT
  6. [coding] Create FastAPI app in main.py
  7. [verify] Install dependencies
  8. [verify] Run API server

Do you want to proceed? [Y/n/edit]: 
```

---

### 🎯 Priority 3: Real-time Progress UI
**Why:** Users need visual feedback on long-running operations.

**Features:**
- Progress bar for overall completion
- Spinner for current task
- Estimated time remaining
- Token usage tracking

**Libraries:**
- `rich` for beautiful terminal UI
- `tqdm` for progress bars

**Example:**
```
Creating Project: my-fastapi-app
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 60% 
Current: Creating auth.py [⠹] 
Completed: 6/10 tasks
Time: 45s | Est. remaining: 30s
Tokens: 2,450 | Cost: $0.03
```

---

### 🎯 Priority 4: Project Templates
**Why:** Users want quick-start options for common project types.

**Features:**
```bash
# List templates
agentic-coder templates

# Use template
agentic-coder create --template nextjs-auth my-app
agentic-coder create --template fastapi-crud my-api
agentic-coder create --template django-blog my-blog
```

**Built-in Templates:**
1. `nextjs-auth` - Next.js with authentication
2. `fastapi-crud` - FastAPI with CRUD operations
3. `react-dashboard` - React admin dashboard
4. `django-rest` - Django REST API
5. `express-graphql` - Express + GraphQL
6. `flask-api` - Flask REST API

**Implementation:**
- Store templates in `src/coding_agent_plugin/templates/`
- Templates are just prompt configurations with predefined architecture

---

### 🎯 Priority 5: Git Integration
**Why:** Users want version control built-in for safety and collaboration.

**Features:**
```bash
agentic-coder create "My App" --git  # Auto-init git repo
```

**Auto-commits:**
- After planning: "chore: initialize project structure"
- After each file: "feat: add {filename}"
- After verification: "test: verify project setup"
- After error fix: "fix: resolve {error}"

**Implementation:**
- Use `gitpython` library
- Add `--no-git` flag to disable

---

### 🎯 Priority 6: Automatic Testing
**Why:** Users expect tests to be generated automatically.

**Features:**
- Generate unit tests for each module
- Generate integration tests for APIs
- Generate E2E tests for full flows
- Run tests automatically in verification phase

**Example:**
```
Testing Phase:
  ✓ Unit tests for models.py (5 tests passed)
  ✓ Unit tests for auth.py (8 tests passed)
  ✓ Integration tests for /login endpoint (2 tests passed)
  ⚠ E2E test failed: /register endpoint (1 test failed)
  
  Running ErrorAgent to fix test failures...
```

---

### 🎯 Priority 7: Documentation Generation
**Why:** Users need documentation for their generated projects.

**Features:**
- Auto-generate `README.md` with:
  - Project overview
  - Installation instructions
  - API documentation
  - Usage examples
  - Architecture diagram (Mermaid)
- Auto-generate API docs (Swagger/OpenAPI for APIs)
- Generate inline code comments

**Example README:**
```markdown
# My FastAPI Login Backend

Auto-generated by [Coding Agent Plugin](https://github.com/...)

## Overview
A production-ready FastAPI backend with JWT authentication...

## Installation
\`\`\`bash
cd app
pip install -r requirements.txt
\`\`\`

## API Endpoints
- POST /register - Create new user
- POST /login - Authenticate user

## Architecture
[Mermaid diagram here]
```

---

### 🎯 Priority 8: Cost Tracking & Limits
**Why:** Users are concerned about LLM costs, especially with expensive models.

**Features:**
```bash
# Set budget
agentic-coder create "My App" --max-cost 0.50  # Stop at $0.50

# Show costs
agentic-coder stats show
```

**Display:**
```
💰 Cost Summary
Project: my-fastapi-app
Total Tokens: 12,450
Total Cost: $0.15

Breakdown:
  Planning: $0.02 (1,200 tokens)
  Coding: $0.10 (8,500 tokens)
  Error Fixing: $0.03 (2,750 tokens)
```

**Implementation:**
- Track tokens per agent
- Calculate costs based on provider pricing
- Warn at 80% of budget
- Stop at 100%

---

### 🎯 Priority 9: Configuration Profiles
**Why:** Users want to save their preferences.

**Features:**
```bash
# Create profile
agentic-coder config create my-profile \
  --model qwen/qwen3-next-80b-a3b-instruct \
  --provider nvidia \
  --max-cost 1.00 \
  --framework fastapi

# Use profile
agentic-coder create "Login API" --profile my-profile

# List profiles
agentic-coder config list
```

**Stored in:** `~/.coding-agent/profiles.yml`

---

### 🎯 Priority 10: Web UI (Future)
**Why:** Non-technical users prefer visual interfaces.

**Features:**
- Web-based project creator
- Visual plan editor (drag-and-drop tasks)
- Live code preview
- Project gallery (showcase community projects)

**Tech Stack:**
- FastAPI backend
- React frontend
- WebSocket for real-time updates

---

## Developer Experience Improvements

### 🔧 Plugin System
**Why:** Developers want to extend functionality.

**Features:**
```python
# Custom agent
class MyCustomAgent(BaseAgent):
    async def execute(self, task):
        # Custom logic
        pass

# Register
orchestrator.register_agent("custom", MyCustomAgent())

# Use in plan
{
  "agent": "custom",
  "details": {...}
}
```

---

### 🔧 Streaming Output
**Why:** Users want to see code being generated in real-time.

**Features:**
- Stream LLM responses token-by-token
- Show thinking process
- Allow early cancellation

---

### 🔧 Multi-language Support
**Why:** Not everyone builds Python backends.

**Support:**
- Python (FastAPI, Django, Flask)
- JavaScript/TypeScript (Node.js, Next.js, Express)
- Go
- Rust
- Java (Spring Boot)

---

## Quality & Safety Improvements

### 🛡️ Rollback & Undo
**Why:** Users need safety nets.

**Features:**
```bash
# Undo last operation
agentic-coder undo

# Rollback to checkpoint
agentic-coder rollback --to planning

# Show history
agentic-coder history
```

---

### 🛡️ Code Quality Checks
**Why:** Users expect production-ready code.

**Features:**
- Run linters (eslint, pylint, etc.)
- Run formatters (prettier, black, etc.)
- Security scanning (bandit, snyk)
- Dependency vulnerability check

---

### 🛡️ Dry Run Mode
**Why:** Users want to preview without executing.

**Features:**
```bash
agentic-coder create "My App" --dry-run
# Shows plan, estimated cost, estimated time
# No actual code generation
```

---

## Implementation Priority

### Phase 1 (MVP+)
1. CLI Interface ⭐⭐⭐
2. Interactive Planning Review ⭐⭐⭐
3. Rich Progress UI ⭐⭐
4. Git Integration ⭐⭐

### Phase 2 (Enhanced)
5. Project Templates ⭐⭐⭐
6. Automatic Testing ⭐⭐⭐
7. Documentation Generation ⭐⭐
8. Cost Tracking ⭐⭐

### Phase 3 (Advanced)
9. Configuration Profiles ⭐
10. Plugin System ⭐⭐
11. Multi-language Support ⭐⭐⭐

### Phase 4 (Future)
12. Web UI ⭐⭐
13. Code Quality Checks ⭐
14. Rollback System ⭐

---

## Quick Wins (Do Now)

1. **Add CLI** - Use Click/Typer (2-3 hours)
2. **Use Rich for UI** - Better terminal output (1 hour)
3. **Add templates.yml** - Define 3-5 common templates (2 hours)
4. **Cost tracking** - Display token count (1 hour)
5. **Better README** - Add GIFs/demos (1 hour)

---

## Marketing & Community

### Documentation
- Comprehensive docs site (Docusaurus or MkDocs)
- Video tutorials
- Blog posts with examples

### Community
- GitHub Discussions
- Discord server
- Showcase gallery
- Contributor guide
- Bounty program for features

### Branding
- Logo and consistent design
- Social media presence
- Comparison with competitors (Devin, v0, Bolt.new)
