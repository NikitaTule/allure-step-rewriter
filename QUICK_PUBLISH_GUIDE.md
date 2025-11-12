# Quick Publishing Guide

## Step 1: Register on PyPI

### 1.1 Register on Test PyPI (for testing)
1. Go to: https://test.pypi.org/account/register/
2. Fill in the form:
   - Username: (choose unique username)
   - Email: your email
   - Password: (secure password)
3. Verify email
4. Enable 2FA (recommended)

### 1.2 Register on Production PyPI
1. Go to: https://pypi.org/account/register/
2. Same process as Test PyPI
3. Verify email
4. Enable 2FA (recommended)

---

## Step 2: Create API Tokens

### 2.1 Test PyPI Token
1. Login to: https://test.pypi.org/
2. Go to: Account Settings → API tokens
3. Click "Add API token"
4. Token name: `allure-step-rewriter`
5. Scope: "Entire account" (for first upload)
6. Copy the token (starts with `pypi-`)
7. Save it securely!

### 2.2 Production PyPI Token
1. Login to: https://pypi.org/
2. Go to: Account Settings → API tokens
3. Click "Add API token"
4. Token name: `allure-step-rewriter`
5. Scope: "Entire account" (for first upload)
6. Copy the token
7. Save it securely!

---

## Step 3: Configure Credentials

### Option A: Using .pypirc file (Recommended)

Create file: `~/.pypirc` (Windows: `C:\Users\YourName\.pypirc`)

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PRODUCTION_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TEST_TOKEN_HERE
```

**Replace:**
- `pypi-YOUR_PRODUCTION_TOKEN_HERE` with your PyPI token
- `pypi-YOUR_TEST_TOKEN_HERE` with your Test PyPI token

### Option B: Using environment variables

```bash
# Windows PowerShell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-YOUR_TOKEN_HERE"

# Windows CMD
set TWINE_USERNAME=__token__
set TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE

# Linux/macOS
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE
```

---

## Step 4: Publish to Test PyPI (Testing)

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# You'll see output like:
# Uploading distributions to https://test.pypi.org/legacy/
# Uploading allure_step_rewriter-0.2.1-py3-none-any.whl
# Uploading allure_step_rewriter-0.2.1.tar.gz
```

### Verify on Test PyPI:
- URL: https://test.pypi.org/project/allure-step-rewriter/

### Test installation from Test PyPI:

```bash
# Create test environment
python -m venv test_env
test_env\Scripts\activate  # Windows
# source test_env/bin/activate  # Linux/macOS

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ allure-step-rewriter

# Test it works
python -c "from allure_step_rewriter import rewrite_step, __version__; print(f'Version: {__version__}')"

# Clean up
deactivate
```

---

## Step 5: Publish to Production PyPI

**⚠️ IMPORTANT: Once published, you CANNOT delete or re-upload the same version!**

```bash
# Upload to Production PyPI
twine upload dist/*

# You'll see:
# Uploading distributions to https://upload.pypi.org/legacy/
# Uploading allure_step_rewriter-0.2.1-py3-none-any.whl
# Uploading allure_step_rewriter-0.2.1.tar.gz
```

### Verify on PyPI:
- URL: https://pypi.org/project/allure-step-rewriter/

### Test installation:

```bash
pip install allure-step-rewriter[allure]

python -c "from allure_step_rewriter import rewrite_step; print('Success!')"
```

---

## Step 6: Git Commit and Tag

```bash
# Commit all changes
git add .
git commit -m "chore: prepare v0.2.1 release"
git push origin main

# Create and push tag
git tag -a v0.2.1 -m "Release v0.2.1 - CI/CD and test improvements"
git push origin v0.2.1
```

---

## Step 7: Create GitHub Release

1. Go to: https://github.com/NikitaTule/allure-step-rewriter/releases/new
2. Choose tag: `v0.2.1`
3. Release title: `v0.2.1 - CI/CD Pipeline and Test Coverage Improvements`
4. Description:

```markdown
## 🎉 What's New in v0.2.1

### ✨ Highlights
- **CI/CD Pipeline**: Automated testing on Ubuntu, Windows, macOS
- **85% Test Coverage**: 49 unit tests (was 18)
- **Pre-commit Hooks**: Automated code quality
- **Contributing Guide**: Full documentation

### 📊 Stats
- Tests: 18 → 49 (+172%)
- Coverage: 43% → 85% (+97%)
- Python: 3.8, 3.9, 3.10, 3.11, 3.12

### 📦 Installation
pip install allure-step-rewriter[allure]

**Full Changelog**: https://github.com/NikitaTule/allure-step-rewriter/blob/main/CHANGELOG.md
```

5. Attach files:
   - `dist/allure_step_rewriter-0.2.1-py3-none-any.whl`
   - `dist/allure_step_rewriter-0.2.1.tar.gz`

6. Click **"Publish release"**

---

## 🎯 Quick Commands Summary

```bash
# 1. Upload to Test PyPI (testing)
twine upload --repository testpypi dist/*

# 2. Test installation
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ allure-step-rewriter

# 3. Upload to Production PyPI
twine upload dist/*

# 4. Git tag
git tag -a v0.2.1 -m "Release v0.2.1"
git push origin v0.2.1
```

---

## ❓ Troubleshooting

### Error: "Invalid or non-existent authentication information"
- Check your API token is correct
- Ensure token starts with `pypi-`
- Check `.pypirc` file format

### Error: "File already exists"
- Version already published on PyPI
- Bump version in `pyproject.toml` and `version.py`
- Rebuild: `python -m build`

### Error: "Package name already taken"
- Your package name exists
- Check: https://pypi.org/project/allure-step-rewriter/
- If it's yours, use project-scoped token

### Error: 403 Forbidden
- Enable 2FA on PyPI account
- Create new API token
- Update `.pypirc`

---

## ✅ Post-Publication Checklist

- [ ] Package visible on PyPI: https://pypi.org/project/allure-step-rewriter/
- [ ] Installation works: `pip install allure-step-rewriter`
- [ ] GitHub Release created
- [ ] Git tag pushed
- [ ] Documentation updated
- [ ] Announce on social media (optional)

---

## 📞 Need Help?

- PyPI Help: https://pypi.org/help/
- Packaging Guide: https://packaging.python.org/
- Twine Docs: https://twine.readthedocs.io/

Good luck! 🚀
