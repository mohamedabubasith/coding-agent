# Publishing to PyPI - Step by Step Guide

## Pre-requisites

1. ✅ PyPI account created at https://pypi.org/account/register/
2. ✅ TestPyPI account (for testing) at https://test.pypi.org/account/register/
3. ✅ API tokens generated for both PyPI and TestPyPI

## Step 1: Prepare Your Package

### 1.1 Update `pyproject.toml`

Ensure all metadata is correct:

```toml
[project]
name = "agentic-coder"
version = "0.1.0"  # Update this for each release
description = "AI-powered project creator and iterative developer"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [
    { name = "Mohamed Abu Basith", email = "your.actual.email@example.com" }
]
keywords = ["ai", "coding-agent", "llm", "autonomous-agent", "code-generation"]

# Update URLs
[project.urls]
Homepage = "https://github.com/mohamedabubasith/coding-agent"
Repository = "https://github.com/mohamedabubasith/coding-agent"
Issues = "https://github.com/mohamedabubasith/coding-agent/issues"
```

### 1.2 Create Required Files

Ensure these files exist:
- ✅ `README.md` - Project description
- ✅ `LICENSE` - MIT license
- ✅ `CHANGELOG.md` - Version history
- ✅ `.gitignore` - Exclude build files

### 1.3 Update CHANGELOG.md

```markdown
# Changelog

## [0.1.0] - 2024-01-01

### Added
- Autonomous project creation
- Interactive planning review
- Iterative improvement system
- Multi-provider LLM support
- Git integration
- Rich CLI interface

### Features
- Create complete projects from natural language
- Make targeted improvements to existing projects
- Beautiful terminal UI with progress indicators
- Automatic error handling and retry logic
```

## Step 2: Build the Package

### 2.1 Install Build Tools

```bash
pip install --upgrade build twine
```

### 2.2 Clean Previous Builds

```bash
rm -rf dist/
```

### 2.3 Build Distribution Files

```bash
python3 -m build
```

This creates:
- `dist/agentic-coder-0.1.0.tar.gz` (source distribution)
- `dist/coding_agent_plugin-0.1.0-py3-none-any.whl` (wheel)

### 2.4 Verify the Build

```bash
twine check dist/*
```

Should output: `Checking dist/*: PASSED`

## Step 3: Test on Test PyPI (Optional but Recommended)

### 3.1 Upload to Test PyPI

```bash
twine upload dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your TestPyPI API token (starts with `pypi-`)

### 3.2 Test Installation

```bash
pip install -i https://test.pypi.org/simple/ agentic-coder
```

### 3.3 Verify it Works

```bash
agentic-coder --help
```

### 3.4 Uninstall Test Version

```bash
pip uninstall agentic-coder
```

## Step 4: Publish to PyPI

### 4.1 Upload to PyPI

```bash
twine upload dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your PyPI API token

### 4.2 Verify on PyPI

Visit: https://pypi.org/project/agentic-coder/

## Step 5: Test Real Installation

```bash
pip install agentic-coder
agentic-coder --help
```

## Step 6: Create GitHub Release

### 6.1 Tag the Release

```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

### 6.2 Create GitHub Release

1. Go to https://github.com/mohamedabubasith/coding-agent/releases/new
2. Select tag `v0.1.0`
3. Title: `v0.1.0 - Initial Release`
4. Description: Copy from CHANGELOG.md
5. Attach `dist/*.tar.gz` and `dist/*.whl` files
6. Click "Publish release"

## Automation with GitHub Actions (Recommended)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

### Setup GitHub Secrets

1. Go to repository Settings → Secrets and variables → Actions
2. Add `PYPI_API_TOKEN` with your PyPI API token

## Version Bumping Strategy

### Semantic Versioning (SemVer)

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.2.0): New features, backwards compatible
- **PATCH** (0.1.1): Bug fixes

### Before Each Release

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit changes: `git commit -m "Bump version to 0.2.0"`
4. Build and publish
5. Create Git tag

## Troubleshooting

### Issue: "File already exists"
**Solution:** You can't overwrite files on PyPI. Bump the version number.

### Issue: "Invalid distribution"
**Solution:** Check `twine check dist/*` for errors

### Issue: "403 Permission denied"
**Solution:** Ensure your API token has upload permissions

### Issue: Package installs but command not found
**Solution:** Check `[project.scripts]` in `pyproject.toml`:
```toml
[project.scripts]
agentic-coder = "coding_agent_plugin.cli.main:app"
```

## Best Practices

1. ✅ Always test on TestPyPI first
2. ✅ Use API tokens, not passwords
3. ✅ Keep CHANGELOG.md up to date
4. ✅ Tag releases in Git
5. ✅ Use GitHub Actions for automated publishing
6. ✅ Never commit API tokens to Git
7. ✅ Test installation in fresh virtual environment

## Useful Commands

```bash
# Check package metadata
python -m build --no-isolation && twine check dist/*

# View package details
pip show agentic-coder

# List files in package
tar -tzf dist/agentic-coder-*.tar.gz

# Uninstall
pip uninstall agentic-coder

# Install specific version
pip install agentic-coder==0.1.0
```

## PyPI Package Status Badges

Add to README.md:

```markdown
[![PyPI version](https://img.shields.io/pypi/v/agentic-coder)](https://pypi.org/project/agentic-coder/)
[![Downloads](https://img.shields.io/pypi/dm/agentic-coder)](https://pypi.org/project/agentic-coder/)
[![Python Versions](https://img.shields.io/pypi/pyversions/agentic-coder)](https://pypi.org/project/agentic-coder/)
```

## Maintaining the Package

### Responding to Issues
- Check GitHub issues regularly
- Label issues appropriately (bug, feature, question)
- Provide clear reproduction steps

### Releasing Updates
1. Fix bugs or add features
2. Update CHANGELOG.md
3. Bump version in pyproject.toml
4. Build and test locally
5. Publish to PyPI
6. Create GitHub release

### Monitoring Usage
- Check PyPI download statistics
- Monitor GitHub stars and forks
- Read user feedback in issues/discussions
