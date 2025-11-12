# Examples - allure-step-rewriter

This directory contains usage examples for `allure-step-rewriter`.

## Running Examples

### Install Dependencies

```bash
pip install allure-step-rewriter[allure]
pip install pytest
```

### Run Examples

```bash
# Run all examples
pytest examples/ -v

# Run specific example
pytest examples/basic_usage.py -v

# Generate Allure report
pytest examples/ --alluredir=allure-results
allure serve allure-results
```

## Examples Description

### 1. `basic_usage.py` - Basic Usage

**Demonstrates:**
- Using `@rewrite_step` as a decorator
- Dynamic title override with `step_title`
- Using `with rewrite_step()` as a context manager
- Decorator without parentheses (uses function name)
- Grouping multiple actions into one step

**Key Examples:**
```python
@rewrite_step("Get user data")
def get_user_data(user_id):
    return {"id": user_id}

# Override title dynamically
data = get_user_data(123, step_title="Fetch admin user")

# Use as context manager
with rewrite_step("Custom step"):
    get_user_data(456)
```

---

### 2. `multiple_overrides.py` - Multiple Overrides

**Demonstrates:**
- Overriding **unlimited number** of steps in single context
- Grouping complex flows into one logical step
- Practical E2E test examples
- API testing with multiple requests

**Key Examples:**
```python
with rewrite_step("User Registration Flow", allow_multiple=True):
    open_browser()
    navigate("https://example.com/register")
    fill_field("username", "john")
    fill_field("email", "john@example.com")
    click_button("Register")
    close_browser()
# Result: ONLY ONE step "User Registration Flow"
```

**Important:** All nested calls to decorated functions are "collapsed" into one step.

---

### 3. `nested_steps.py` - Nested Steps

**Demonstrates:**
- Combining `rewrite_step` and `allure.step`
- Creating hierarchical step structure
- When to use `rewrite_step` vs `allure.step`
- Complex multi-level structures

**Key Examples:**
```python
with rewrite_step("Test Scenario"):
    api_call("/setup")  # Gets overridden

    # Create nested step
    with allure.step("Preparation"):
        api_call("/init")

    with allure.step("Execution"):
        api_call("/execute")

# Result:
# ✓ Test Scenario
#   ✓ Preparation
#   ✓ Execution
```

**Rules:**
- `rewrite_step` context = collapses decorated functions
- `allure.step` inside `rewrite_step` = creates nested step
- `rewrite_step` inside `rewrite_step` = **DOES NOT create** nested step!

---

### 4. `pytest_integration.py` - Pytest Integration

**Demonstrates:**
- Using with pytest fixtures
- Parametrized tests (`@pytest.mark.parametrize`)
- Pytest markers and Allure decorators
- Session-scoped fixtures
- Exception handling (`pytest.raises`)
- Test classes and methods
- Real-world usage scenarios

**Key Examples:**
```python
@pytest.fixture
def browser():
    with rewrite_step("Initialize browser"):
        browser_instance = setup_browser()
    yield browser_instance
    with rewrite_step("Close browser"):
        teardown_browser()

@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user(user_id):
    with rewrite_step(f"Test GET /users/{user_id}"):
        response = get_user(user_id)
        assert validate(response)
```

---

## General Principles

### When to Use `rewrite_step`

✅ **Use `rewrite_step` when:**
- Need to group multiple low-level operations into one logical step
- Want to avoid deep nesting in Allure report
- Need to dynamically change step title
- Multiple similar operations should be represented as one action

❌ **DON'T use `rewrite_step` when:**
- Need hierarchical step structure (use `allure.step`)
- Each step is important and should be visible separately
- Nested `with rewrite_step()` (doesn't work as override!)

### When to Use `allure.step`

✅ **Use `allure.step` when:**
- Need to create nested steps inside `rewrite_step` context
- Hierarchical structure is important (Given/When/Then)
- Each step should be visible separately in report

### Combining Both

**Best Practice:**
```python
with rewrite_step("Test Case"):
    # Multiple low-level operations
    setup_operation_1()
    setup_operation_2()

    # Important block - nested step
    with allure.step("Critical Section"):
        critical_operation()

    # More low-level operations
    cleanup_operation_1()
    cleanup_operation_2()
```

---

## Allure Report Structure

### Example 1: Only `rewrite_step`
```python
with rewrite_step("Parent"):
    func_a()
    func_b()
    func_c()
```
**Result:**
```
✓ Parent
```

### Example 2: `rewrite_step` + `allure.step`
```python
with rewrite_step("Parent"):
    func_a()
    with allure.step("Child"):
        func_b()
    func_c()
```
**Result:**
```
✓ Parent
  ✓ Child
```

### Example 3: Nested `rewrite_step` (DOESN'T WORK!)
```python
with rewrite_step("Level 1"):
    with rewrite_step("Level 2"):
        func_a()
```
**Result:**
```
✓ Level 1
(Level 2 does NOT appear!)
```

---

## Debugging Tips

1. **Enable verbose pytest output:**
   ```bash
   pytest examples/basic_usage.py -v -s
   ```

2. **Check Allure report:**
   ```bash
   pytest examples/ --alluredir=allure-results
   allure serve allure-results
   ```

3. **Use print for debugging:**
   ```python
   @rewrite_step("My step")
   def my_func():
       print("DEBUG: function called")
       return "result"
   ```

---

## Additional Resources

- [Main README](../README.md)
- [GitHub Repository](https://github.com/NikitaTule/allure-step-rewriter)
- [Allure Documentation](https://docs.qameta.io/allure/)
- [Pytest Documentation](https://docs.pytest.org/)

---

## Contact

If you have questions or suggestions about examples:
- GitHub Issues: https://github.com/NikitaTule/allure-step-rewriter/issues
- Email: tulenckov.nikita@gmail.com
