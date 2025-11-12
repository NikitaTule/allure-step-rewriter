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

```python
from allure_step_rewriter import rewrite_step
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
- allure-pytest >= 2.9.0

**Important:** `allure-pytest` is a **peer dependency** and must be installed separately. This allows you to manage the allure-pytest version yourself without conflicts.

## 🚀 Installation

### Option 1: Install with allure-pytest automatically

```bash
pip install allure-step-rewriter[allure]
```

### Option 2: Install separately (recommended)

```bash
# First, install allure-pytest (if not already installed)
pip install allure-pytest>=2.9.0

# Then install allure-step-rewriter
pip install allure-step-rewriter
```

### Option 3: For development

```bash
pip install allure-step-rewriter[dev]
```

**Note:** If you already have `allure-pytest` installed, just install `allure-step-rewriter` without extras.
## 📖 Quick Start

### Basic Usage

```python
from allure_step_rewriter import rewrite_step

# As a decorator
@rewrite_step("Get user data")
def get_user_data(user_id):
    return api.get(f"/users/{user_id}")

# In your test
def test_user():
    # Call with default title
    data = get_user_data(123)

    # Or override the title
    data = get_user_data(123, step_title="Fetch admin user")
```

### Multiple Overrides

You can override **multiple steps** within a single context:

```python
@rewrite_step("Login")
def login(username):
    pass

@rewrite_step("Get data")
def get_data():
    pass

@rewrite_step("Logout")
def logout():
    pass

# All three functions will be overridden to "User Flow"
with rewrite_step("User Flow"):
    login("admin")
    get_data()
    logout()

# Result in Allure: Only one step "User Flow" (no nesting!)
```

### Combining with Nested Steps

When you need **hierarchical structure**, combine `rewrite_step` with standard `allure.step`:

```python
import allure
from allure_step_rewriter import rewrite_step

@rewrite_step("API call")
def api_call():
    pass

with rewrite_step("Test Scenario"):
    api_call()  # Overridden to "Test Scenario"

    # Create nested step using allure.step
    with allure.step("Validation"):
        assert True

    api_call()  # Overridden to "Test Scenario" again

# Result in Allure:
# ✓ Test Scenario
#   ✓ Validation
```

## ⚠️ Important Behavior

### How rewrite_step Works

`rewrite_step` **does not create nested steps** for decorated functions within its context. Instead, it **skips creating new steps** and uses the existing context:

```python
with rewrite_step("Parent"):
    func_a()  # No step created
    func_b()  # No step created
    func_c()  # No step created
# Result: Only "Parent" step appears in Allure report
```

### When You Need Nested Steps

Use standard `allure.step` for creating nested steps:

```python
import allure

with rewrite_step("Parent"):
    func_a()  # Overridden to "Parent"

    # Need a nested step? Use allure.step
    with allure.step("Child Step"):
        func_b()  # Creates nested "Child Step"

    func_c()  # Overridden to "Parent"

# Result in Allure:
# ✓ Parent
#   ✓ Child Step
```

### Key Rules

1. **`rewrite_step` context** = Override all decorated functions (no nesting)
2. **`allure.step` inside `rewrite_step`** = Create nested steps when needed
3. **Multiple overrides** = Supported within single context
4. **Thread-safe** = Works correctly in parallel test execution

## 🔧 API Reference

### `rewrite_step(title: str)`

Can be used as both decorator and context manager.

**As decorator:**
```python
@rewrite_step("Step title")
def my_function():
    pass

# Call with default title
my_function()

# Override title dynamically
my_function(step_title="Custom title")
```

**As context manager:**
```python
with rewrite_step("Context title"):
    my_function()  # Overrides to "Context title"
```

**Decorator without parentheses:**
```python
@rewrite_step
def my_function():
    pass
# Uses function name as title
```
### 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
### 👤 Author
Nikita Tulenkov

GitHub: [@NikitaTulenkov](https://github.com/NikitaTule)

LinkedIn: [nikita-tulenkov](https://www.linkedin.com/in/nikita--tulenkov)

Email: tulenckov.nikita@gmail.com

### ⭐ Support
If this library helped you - give it a star! ⭐