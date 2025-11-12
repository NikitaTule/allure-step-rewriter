# Contributing to Allure Step Rewriter

Thank you for your interest in contributing to allure-step-rewriter! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip

### Setting Up Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/allure-step-rewriter.git
   cd allure-step-rewriter
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv

   # On Windows
   .venv\Scripts\activate

   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e .[dev]
   ```

4. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

## 🧪 Running Tests

### Run all tests:
```bash
pytest
```

### Run tests with coverage:
```bash
pytest --cov=allure_step_rewriter --cov-report=html --cov-report=term-missing
```

### Run specific test file:
```bash
pytest tests/unit/test_rewrite_step_decorator.py -v
```

### View coverage report:
```bash
# Open htmlcov/index.html in your browser
```

## 📝 Code Style

This project follows these style guidelines:

### Formatting
- **Black** for code formatting (line length: 88)
- **Ruff** for linting
- **mypy** for type checking (optional but recommended)

### Run formatters manually:
```bash
# Format code
black allure_step_rewriter tests examples

# Lint code
ruff check allure_step_rewriter tests examples --fix

# Type check
mypy allure_step_rewriter
```

### Pre-commit hooks
Pre-commit hooks will automatically run on every commit. To run manually:
```bash
pre-commit run --all-files
```

## 🔧 Development Workflow

### 1. Create a feature branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make your changes
- Write clean, readable code
- Add/update tests for your changes
- Update documentation if needed
- Follow the existing code style

### 3. Test your changes
```bash
# Run tests
pytest

# Check coverage
pytest --cov=allure_step_rewriter --cov-report=term-missing

# Ensure coverage is at least 80%
```

### 4. Commit your changes
```bash
git add .
git commit -m "feat: add new feature"
# or
git commit -m "fix: resolve bug in step override"
```

**Commit message format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Adding or updating tests
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks
- `perf:` - Performance improvements

### 5. Push and create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📋 Pull Request Guidelines

### Before submitting:
- ✅ All tests pass
- ✅ Code coverage is at least 80%
- ✅ Pre-commit hooks pass
- ✅ Documentation is updated
- ✅ CHANGELOG.md is updated (if applicable)

### PR Description should include:
1. **What** - What changes were made
2. **Why** - Why these changes are necessary
3. **How** - How the changes work
4. **Testing** - How the changes were tested

### Example PR description:
```markdown
## Changes
Added support for custom step titles via `step_title` parameter.

## Motivation
Users requested the ability to override step titles dynamically without
using context managers.

## Implementation
- Added `step_title` kwarg to decorator wrapper
- Updated tests to cover new functionality
- Added documentation to README

## Testing
- Added 5 new unit tests
- All existing tests pass
- Coverage increased from 85% to 87%
```

## 🐛 Reporting Bugs

### Before reporting:
- Check if the bug has already been reported in [Issues](https://github.com/NikitaTule/allure-step-rewriter/issues)
- Try to reproduce with the latest version

### Bug report should include:
1. **Description** - Clear description of the bug
2. **Steps to reproduce** - Minimal code example
3. **Expected behavior** - What should happen
4. **Actual behavior** - What actually happens
5. **Environment:**
   - Python version
   - allure-pytest version
   - OS and version
   - allure-step-rewriter version

## 💡 Feature Requests

We welcome feature requests! Please:
1. Check if the feature has already been requested
2. Explain the use case
3. Provide examples of how it would work
4. Consider if it fits the project scope

## 🏗️ Project Structure

```
allure-step-rewriter/
├── allure_step_rewriter/      # Main package
│   ├── __init__.py            # Package initialization
│   ├── rewrite_step.py        # Core functionality
│   └── version.py             # Version info
├── tests/                     # Test suite
│   ├── unit/                  # Unit tests
│   └── conftest.py            # Pytest fixtures
├── examples/                  # Usage examples
├── .github/workflows/         # CI/CD workflows
├── pyproject.toml             # Project configuration
└── README.md                  # Documentation
```

## 📜 Code Review Process

1. All PRs require at least one review
2. CI/CD must pass (tests, linting, build)
3. Coverage must not decrease
4. Maintainers may request changes
5. Once approved, maintainers will merge

## 🎯 Areas for Contribution

### Good first issues:
- Documentation improvements
- Adding more examples
- Writing tests for edge cases
- Fixing typos

### Advanced contributions:
- Performance optimizations
- New features
- Integration tests
- Type hints improvements

## 📚 Resources

- [Allure Framework Documentation](https://docs.qameta.io/allure/)
- [pytest Documentation](https://docs.pytest.org/)
- [Python Packaging User Guide](https://packaging.python.org/)

## ❓ Questions?

- Open a [Discussion](https://github.com/NikitaTule/allure-step-rewriter/discussions)
- Contact the maintainer: tulenckov.nikita@gmail.com

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
