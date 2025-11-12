"""
Multiple overrides example - demonstrating allow_multiple=True for unlimited overrides

With allow_multiple=True, all decorated functions inside the context will be
overridden to the context title, creating a single step in Allure report.

Run with: pytest examples/multiple_overrides.py --alluredir=allure-results
View report: allure serve allure-results
"""

import pytest
from allure_step_rewriter import rewrite_step


# Define several functions with default titles
@rewrite_step("Open browser")
def open_browser():
    print("Opening browser")
    return "browser_instance"


@rewrite_step("Navigate to URL")
def navigate(url: str):
    print(f"Navigating to {url}")
    return url


@rewrite_step("Fill form field")
def fill_field(field: str, value: str):
    print(f"Filling {field} with {value}")
    return True


@rewrite_step("Click button")
def click_button(button: str):
    print(f"Clicking {button}")
    return True


@rewrite_step("Verify result")
def verify(expected: str):
    print(f"Verifying {expected}")
    return True


@rewrite_step("Close browser")
def close_browser():
    print("Closing browser")
    return True


def test_multiple_overrides_single_context():
    """
    Test that multiple decorated functions can be overridden in single context.

    Using allow_multiple=True allows overriding all functions.
    Result: Only ONE step "User Registration Flow" in Allure report.
    All function calls are "collapsed" into this single step.
    """
    with rewrite_step("User Registration Flow", allow_multiple=True):
        open_browser()
        navigate("https://example.com/register")
        fill_field("username", "john_doe")
        fill_field("email", "john@example.com")
        fill_field("password", "secret123")
        click_button("Register")
        verify("Registration successful")
        close_browser()


def test_api_test_scenario():
    """
    Another example: API testing scenario with multiple operations.
    """

    @rewrite_step("Send GET request")
    def get_request(endpoint: str):
        print(f"GET {endpoint}")
        return {"status": 200}

    @rewrite_step("Send POST request")
    def post_request(endpoint: str, data: dict):
        print(f"POST {endpoint}: {data}")
        return {"status": 201}

    @rewrite_step("Validate response")
    def validate(response: dict):
        print(f"Validating: {response}")
        return response["status"] < 400

    # All API calls collapsed into one step (allow_multiple=True)
    with rewrite_step("API Test: Create and retrieve user", allow_multiple=True):
        response1 = post_request("/api/users", {"name": "John"})
        assert validate(response1)

        response2 = get_request("/api/users/1")
        assert validate(response2)

        response3 = get_request("/api/users/1/profile")
        assert validate(response3)


def test_sequential_contexts_with_overrides():
    """
    Test multiple sequential contexts, each with multiple overrides.
    """

    @rewrite_step("Setup action")
    def setup():
        print("Setup")
        return True

    @rewrite_step("Execute action")
    def execute():
        print("Execute")
        return True

    @rewrite_step("Teardown action")
    def teardown():
        print("Teardown")
        return True

    # First context (allow_multiple=True for multiple overrides)
    with rewrite_step("Test Case 1", allow_multiple=True):
        setup()
        execute()
        teardown()

    # Second context
    with rewrite_step("Test Case 2", allow_multiple=True):
        setup()
        execute()
        teardown()

    # Result: 2 steps in Allure report: "Test Case 1" and "Test Case 2"


def test_real_world_example_e2e():
    """
    Real-world E2E test scenario with many steps collapsed into logical groups.
    """

    @rewrite_step("Init WebDriver")
    def init_driver():
        return "driver"

    @rewrite_step("Login with credentials")
    def login(username: str, password: str):
        print(f"Login: {username}")
        return True

    @rewrite_step("Navigate to page")
    def goto(page: str):
        print(f"Going to {page}")
        return True

    @rewrite_step("Perform action")
    def action(what: str):
        print(f"Action: {what}")
        return True

    @rewrite_step("Assert condition")
    def assert_that(condition: str):
        print(f"Assert: {condition}")
        return True

    # Setup (allow_multiple=True)
    with rewrite_step("Setup Test Environment", allow_multiple=True):
        init_driver()
        assert login("admin", "password")
        goto("dashboard")

    # Test execution
    with rewrite_step("Execute Test Steps", allow_multiple=True):
        goto("users")
        action("Create new user")
        action("Assign role")
        action("Save changes")

    # Verification
    with rewrite_step("Verify Results", allow_multiple=True):
        goto("users/list")
        assert_that("User appears in list")
        assert_that("Role is correct")

    # Result: 3 steps in Allure report:
    # 1. Setup Test Environment
    # 2. Execute Test Steps
    # 3. Verify Results


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
