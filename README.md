# Allure Step Rewriter

**Python library for rewriting Allure step titles without nesting**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Problem

In Allure framework, there's no way to override an existing step title. When you try to change the title, it creates a nested step instead:
```python
@allure.step("Default title")
def get_data():
    return api.get("/data")

# In test
with allure.step("Custom title"):  # ❌ Creates nesting!
    get_data()
Result in Allure:
✓ Custom title
  ✓ Default title  # Unwanted nesting
```  
### ✅ Solution
allure-step-rewriter allows you to rewrite the step title instead of creating nesting:
pythonfrom allure_step_rewriter import rewrite_step
```python
@rewrite_step("Default title")
def get_data():
    return api.get("/data")

# In test
with rewrite_step("Custom title"):  # ✅ Rewrites!
    get_data()
Result in Allure:
✓ Custom title  # No nesting!
```
## 📋 Requirements

- Python 3.8+
- allure-pytest >= 2.9.0 (installed automatically)

**Note:** `allure-pytest` is a required dependency and will be installed automatically when you install `allure-step-rewriter`.

## 🚀 Installation
```bash
pip install allure-step-rewriter
```
### 📖 Quick Start
Coming soon...
### 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
### 👤 Author
Nikita Tulenkov

GitHub: [@NikitaTulenkov](https://github.com/NikitaTule)

LinkedIn: [nikita-tulenkov](www.linkedin.com/in/nikita--tulenkov)

Email: tulenckov.nikita@gmail.com

### ⭐ Support
If this library helped you - give it a star! ⭐