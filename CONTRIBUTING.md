# Contributing to Coding Agent Plugin

First off, thank you for considering contributing to Coding Agent Plugin! 🎉

## How Can I Contribute?

### Reporting Bugs 🐛

Before creating bug reports, please check existing issues. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if relevant**
- **Include your environment details** (OS, Python version, dependencies)

### Suggesting Enhancements 💡

Enhancement suggestions are welcome! Please:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any alternative solutions you've considered**

### Pull Requests 🔧

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/agentic-coder.git
cd agentic-coder

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run CLI locally
agentic-coder --help
```

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to all functions
- Keep functions focused and small
- Write clear commit messages

## Testing

- Add tests for new features
- Ensure all tests pass before submitting PR
- Aim for high code coverage

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src/coding_agent_plugin
```

## Documentation

- Update README.md if adding features
- Add docstrings to new functions
- Update USER_GUIDE.md for user-facing changes
- Keep CHANGELOG.md up to date

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
