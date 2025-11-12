"""
Basic usage examples for allure-step-rewriter

Run with: pytest examples/basic_usage.py --alluredir=allure-results
View report: allure serve allure-results
"""

import pytest
from allure_step_rewriter import rewrite_step


# Example 1: Using as decorator
@rewrite_step("Get user data from API")
def get_user_data(user_id: int):
    """Function with default step title."""
    print(f"Getting data for user {user_id}")
    return {"id": user_id, "name": f"User {user_id}"}


def test_basic_decorator():
    """Test using rewrite_step as decorator."""
    # This will create step with title "Get user data from API"
    data = get_user_data(123)
    assert data["id"] == 123


# Example 2: Override step title dynamically
@rewrite_step("Default: Fetch data")
def fetch_data(endpoint: str):
    """Function with overridable step title."""
    print(f"Fetching from {endpoint}")
    return {"endpoint": endpoint, "data": "response"}


def test_dynamic_title_override():
    """Test overriding step title dynamically."""
    # Use default title
    result1 = fetch_data("/api/users")

    # Override title using step_title parameter
    result2 = fetch_data("/api/posts", step_title="Fetch posts from API")

    assert result1["endpoint"] == "/api/users"
    assert result2["endpoint"] == "/api/posts"


# Example 3: Using as context manager
@rewrite_step("Default action")
def perform_action():
    """Function to be called inside context."""
    print("Performing action")
    return "done"


def test_context_manager():
    """Test using rewrite_step as context manager."""
    # Create a step that overrides the function's default title
    with rewrite_step("Custom step title"):
        result = perform_action()  # Will not create nested step

    assert result == "done"


# Example 4: Decorator without parentheses
@rewrite_step
def calculate_sum(a: int, b: int):
    """Function decorated without parentheses - uses function name as title."""
    return a + b


def test_decorator_without_parentheses():
    """Test decorator without parentheses."""
    # Step title will be "calculate_sum" (function name)
    result = calculate_sum(5, 3)
    assert result == 8


# Example 5: Combining decorators and context managers
@rewrite_step("Login to system")
def login(username: str):
    print(f"Logging in as {username}")
    return True


@rewrite_step("Get dashboard data")
def get_dashboard():
    print("Loading dashboard")
    return {"widgets": 5}


@rewrite_step("Logout from system")
def logout():
    print("Logging out")
    return True


def test_user_workflow():
    """Test complete user workflow."""
    # Group multiple actions under one step
    with rewrite_step("Complete user session"):
        assert login("admin")
        dashboard = get_dashboard()
        assert dashboard["widgets"] == 5
        assert logout()

    # Result: Only one step "Complete user session" in Allure report


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])
