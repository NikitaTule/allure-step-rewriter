# Publication Instructions for allure-step-rewriter

## ✅ Pre-publication Checklist (COMPLETED)

All preparation steps have been completed:

- [x] **Code cleanup**
  - Removed 14 test files from root
  - Removed 2 analyze scripts
  - Removed 14 allure-* directories
  - Removed unused `exceptions.py` and `rewrite_step_v2.py`

- [x] **Test coverage: 85%**
  - 49 unit tests (increased from 18)
  - Import error tests
  - Error handling tests
  - Edge case tests
  - Thread safety tests

- [x] **CI/CD Pipeline**
  - GitHub Actions workflow created
  - Tests on Ubuntu, Windows, macOS
  - Python 3.8-3.12 tested
  - Code coverage, linting, build checks

- [x] **Code Quality**
  - Pre-commit hooks configured
  - Black, Ruff, mypy, Bandit checks

- [x] **Documentation**
  - CONTRIBUTING.md created
  - CHANGELOG.md updated
  - Version bumped to 0.2.1

- [x] **Package Build**
  - Built successfully: `allure_step_rewriter-0.2.1-py3-none-any.whl`
  - Twine check: PASSED
  - Local installation: PASSED

---

## 🚀 Publication Steps

### Step 1: Commit all changes

```bash
git add .
git commit -m "chore: prepare v0.2.1 release - add CI/CD, improve tests, enhance docs"
git push origin main
```

### Step 2: Create Git Tag

```bash
git tag -a v0.2.1 -m "Release v0.2.1"
git push origin v0.2.1
```

### Step 3: Publish to Test PyPI (RECOMMENDED)

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ allure-step-rewriter

# Verify it works
python -c "from allure_step_rewriter import rewrite_step, __version__; print(__version__)"
```

**Test PyPI URL:** https://test.pypi.org/project/allure-step-rewriter/

### Step 4: Publish to PyPI (PRODUCTION)

```bash
# Upload to PyPI
twine upload dist/*
```

**PyPI URL:** https://pypi.org/project/allure-step-rewriter/

### Step 5: Create GitHub Release

1. Go to: https://github.com/NikitaTule/allure-step-rewriter/releases/new
2. Choose tag: `v0.2.1`
3. Title: `v0.2.1 - CI/CD Pipeline and Test Coverage Improvements`
4. Description:

```markdown
## 🎉 What's New in v0.2.1

### ✨ Highlights
- **CI/CD Pipeline**: Automated testing on Ubuntu, Windows, macOS with Python 3.8-3.12
- **85% Test Coverage**: Comprehensive test suite with 49 unit tests
- **Pre-commit Hooks**: Automated code quality checks
- **Contributing Guide**: Detailed documentation for contributors

### 📊 Improvements
- Increased test coverage from 43% to 85%
- Added 31 new unit tests
- Removed unused code modules
- Enhanced error handling tests
- Added thread safety tests

### 📚 Documentation
- Created CONTRIBUTING.md
- Added pre-commit configuration
- Updated CHANGELOG.md

### 🔧 Technical
- GitHub Actions CI/CD workflow
- Black, Ruff, mypy integration
- Bandit security checks
- Automated package build verification

**Full Changelog**: https://github.com/NikitaTule/allure-step-rewriter/blob/main/CHANGELOG.md
```

5. Upload build artifacts:
   - `dist/allure_step_rewriter-0.2.1-py3-none-any.whl`
   - `dist/allure_step_rewriter-0.2.1.tar.gz`

6. Click "Publish release"

---

## 📋 Post-Publication

### Update badges in README.md

Add these badges at the top:

```markdown
[![PyPI version](https://badge.fury.io/py/allure-step-rewriter.svg)](https://badge.fury.io/py/allure-step-rewriter)
[![CI](https://github.com/NikitaTule/allure-step-rewriter/actions/workflows/ci.yml/badge.svg)](https://github.com/NikitaTule/allure-step-rewriter/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/NikitaTule/allure-step-rewriter/branch/main/graph/badge.svg)](https://codecov.io/gh/NikitaTule/allure-step-rewriter)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

### Verify Installation

```bash
# Create new virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from PyPI
pip install allure-step-rewriter[allure]

# Test it
python -c "from allure_step_rewriter import rewrite_step; print('Success!')"
```

---

## 🔐 Credentials Setup (If Not Done)

### PyPI Token

1. Go to: https://pypi.org/manage/account/token/
2. Create API token
3. Configure:

```bash
# Create/edit ~/.pypirc
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE

[testpypi]
username = __token__
password = pypi-YOUR_TEST_TOKEN_HERE
```

---

## 📊 Current Package Status

```
Package: allure-step-rewriter
Version: 0.2.1
Python: 3.8+
License: MIT

Size:
- Wheel: 7.3 KB
- Source: 21 KB

Tests: 49 passing
Coverage: 85%
```

---

## 🎯 Next Steps After Publication

1. **Monitor PyPI stats**: Check download numbers
2. **Watch for issues**: Respond to GitHub issues
3. **Promote**: Share on social media, forums
4. **Iterate**: Plan next release based on feedback

---

## 📞 Support

- Issues: https://github.com/NikitaTule/allure-step-rewriter/issues
- Email: tulenckov.nikita@gmail.com

Good luck with the publication! 🚀
