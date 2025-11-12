# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Integration tests with real Allure reports
- Full mypy compliance with strict mode

---

## [0.2.1] - 2025-11-13

### Added
- **CI/CD Pipeline**: GitHub Actions workflow for automated testing
  - Tests run on Ubuntu, Windows, and macOS
  - Python versions 3.8-3.12 tested
  - Code coverage reporting to Codecov
  - Linting and formatting checks
  - Package build verification
- **Pre-commit hooks**: Automated code quality checks
  - Black formatting
  - Ruff linting
  - Type checking with mypy
  - Security checks with Bandit
  - Docstring validation
- **Contributing Guide**: Comprehensive CONTRIBUTING.md
  - Development setup instructions
  - Code style guidelines
  - PR process documentation
  - Testing guidelines
- **Extensive test suite improvements**:
  - 49 unit tests (increased from 18)
  - 85% code coverage (increased from 43%)
  - Import error tests
  - Error handling tests
  - Edge case tests
  - Thread safety tests

### Changed
- Improved .gitignore to exclude test artifacts
- Enhanced documentation structure

### Removed
- Unused `exceptions.py` module
- Unused `rewrite_step_v2.py` draft file
- Test files from project root (moved to tests/ directory)

### Technical Details
- Coverage: 85% (improved from 43%)
- Tests: 49 passing (improved from 18)
- CI/CD: Full automation with GitHub Actions
- Code quality: Automated linting and formatting

---

## [0.2.0] - 2025-11-12

### Added
- **Multiple overrides support**: Removed artificial limitation on overriding multiple steps in single context
- **Comprehensive examples**: Added `examples/` directory with 4 detailed examples:
  - `basic_usage.py` - Basic decorator and context manager usage
  - `multiple_overrides.py` - Unlimited overrides demonstration
  - `nested_steps.py` - Combining with allure.step for hierarchy
  - `pytest_integration.py` - Pytest fixtures, parametrize, and markers
- **Examples documentation**: Detailed README in examples/ explaining when to use rewrite_step vs allure.step
- **Additional tests**: 6 new tests for multiple overrides scenarios (total: 18 tests)
- **Runtime dependency check**: Added validation in `__init__.py` to check allure-pytest installation
- **Clear error messages**: Informative ImportError with installation instructions

### Changed
- **BREAKING**: Changed dependency management to peer dependency model
  - `allure-pytest` moved from `dependencies` to `optional-dependencies`
  - Users must install `allure-pytest` separately or use `[allure]` extras
  - This prevents version conflicts with existing allure installations
- **Installation options**: Added multiple installation methods:
  - `pip install allure-step-rewriter[allure]` - with allure-pytest
  - `pip install allure-step-rewriter[all]` - with all dependencies
  - `pip install allure-step-rewriter[dev]` - for development
- **Documentation**: Completely rewritten README with:
  - Multiple installation options
  - Detailed usage examples
  - Important behavior warnings
  - API reference
  - Clear explanation of how rewrite_step works

### Fixed
- Multiple overrides now work correctly in single context
  - Removed `can_override = False` limitation in `_can_override_step()` (line 125)
  - Removed `can_override = False` limitation in `_can_override_step_context()` (line 172)
- All decorated functions inside `with rewrite_step()` now correctly override without creating nested steps

### Technical Details
- Coverage: 74% (decreased from 79% due to added error handling code)
- Tests: 18 passing (increased from 12)
- Python support: 3.8, 3.9, 3.10, 3.11, 3.12

---

## [0.1.0] - 2024-10-13

### Added
- Initial release
- Core `rewrite_step()` functionality
- Support for decorator usage: `@rewrite_step("title")`
- Support for context manager usage: `with rewrite_step("title"):`
- Dynamic title override via `step_title` parameter
- Thread-safe implementation
- Basic unit tests (12 tests)
- MIT License
- Basic documentation in README
- Project configuration (pyproject.toml)
- Development dependencies (pytest, black, ruff, mypy, pre-commit)

### Known Limitations (Fixed in 0.2.0)
- Only one function could be overridden per context
- No examples provided
- Dependency management issues with allure-pytest

---

## Project History

### Creation Date
2024-10-13

### Author
Nikita Tulenkov
- GitHub: [@NikitaTule](https://github.com/NikitaTule)
- LinkedIn: [nikita-tulenkov](https://www.linkedin.com/in/nikita--tulenkov)
- Email: tulenckov.nikita@gmail.com

### Repository
https://github.com/NikitaTule/allure-step-rewriter

---

## Version History Summary

| Version | Date       | Key Changes |
|---------|------------|-------------|
| 0.2.0   | 2025-11-12 | Multiple overrides, examples, peer dependency |
| 0.1.0   | 2024-10-13 | Initial release |

---

## Migration Guide

### Migrating from 0.1.0 to 0.2.0

#### 1. Installation Changes

**Before (0.1.0):**
```bash
pip install allure-step-rewriter
# allure-pytest installed automatically
```

**After (0.2.0):**
```bash
# Option 1: Install allure-pytest separately (recommended)
pip install allure-pytest>=2.9.0
pip install allure-step-rewriter

# Option 2: Install with extras
pip install allure-step-rewriter[allure]
```

#### 2. Behavior Changes

**Multiple overrides now work:**

```python
# This now works correctly in 0.2.0 (was limited in 0.1.0)
with rewrite_step("Parent"):
    func_a()  # ✅ Overridden
    func_b()  # ✅ Overridden (was creating nested step in 0.1.0)
    func_c()  # ✅ Overridden (was creating nested step in 0.1.0)
```

#### 3. No Breaking API Changes

All existing code using 0.1.0 API will continue to work in 0.2.0.
The only change is installation method and improved behavior.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
