"""
Pytest integration example - using rewrite_step with pytest fixtures and parametrize

Run with: pytest examples/pytest_integration.py --alluredir=allure-results
View report: allure serve allure-results
"""

import pytest
import allure
from allure_step_rewriter import rewrite_step


# ==============================================================================
# Fixtures with rewrite_step
# ==============================================================================

@pytest.fixture
def browser():
    """Fixture that uses rewrite_step."""
    with rewrite_step("Initialize browser"):
        print("Starting browser")
        browser_instance = {"type": "chrome", "session": "abc123"}

    yield browser_instance

    with rewrite_step("Close browser"):
        print("Closing browser")


@pytest.fixture
def authenticated_user(browser):
    """Fixture that depends on another fixture."""
    @rewrite_step("Login user")
    def login(username: str, password: str):
        print(f"Logging in: {username}")
        return {"username": username, "token": "xyz789"}

    user = login("test_user", "password123")
    return user


# ==============================================================================
# Test with fixtures
# ==============================================================================

def test_with_fixtures(browser, authenticated_user):
    """Test using fixtures with rewrite_step."""

    @rewrite_step("Navigate to page")
    def navigate(url: str):
        print(f"Navigating to {url}")
        return True

    @rewrite_step("Perform action")
    def action(what: str):
        print(f"Action: {what}")
        return True

    with rewrite_step("Test user actions"):
        navigate("/dashboard")
        action("click settings")
        action("update profile")


# ==============================================================================
# Parametrized tests
# ==============================================================================

@pytest.mark.parametrize("username,expected_role", [
    ("admin", "administrator"),
    ("user", "regular"),
    ("guest", "visitor"),
])
def test_parametrized_with_rewrite_step(username, expected_role):
    """Parametrized test with rewrite_step."""

    @rewrite_step("Fetch user role")
    def get_user_role(user: str):
        roles = {"admin": "administrator", "user": "regular", "guest": "visitor"}
        return roles.get(user, "unknown")

    @rewrite_step("Verify role")
    def verify_role(actual: str, expected: str):
        print(f"Checking {actual} == {expected}")
        return actual == expected

    # Use step_title parameter to make step unique for each parameter
    with rewrite_step(f"Test user: {username}"):
        role = get_user_role(username)
        assert verify_role(role, expected_role)


# ==============================================================================
# Pytest markers with rewrite_step
# ==============================================================================

@pytest.mark.smoke
@pytest.mark.critical
@allure.feature("User Management")
@allure.story("User Registration")
def test_with_markers_and_allure():
    """Test combining pytest markers, allure decorators, and rewrite_step."""

    @rewrite_step("Register new user")
    def register(username: str, email: str):
        print(f"Registering {username} with email {email}")
        return {"id": 1, "username": username, "email": email}

    @rewrite_step("Send welcome email")
    def send_email(email: str):
        print(f"Sending email to {email}")
        return True

    with rewrite_step("Complete registration flow"):
        user = register("john_doe", "john@example.com")
        assert send_email(user["email"])


# ==============================================================================
# Using rewrite_step in conftest-like setup
# ==============================================================================

@pytest.fixture(scope="session")
def test_environment():
    """Session-scoped fixture for test environment."""

    @rewrite_step("Setup test environment")
    def setup_env():
        print("Creating test database")
        print("Starting test server")
        return {"db": "test_db", "server": "localhost:8000"}

    @rewrite_step("Teardown test environment")
    def teardown_env():
        print("Stopping test server")
        print("Dropping test database")

    env = setup_env()
    yield env
    teardown_env()


def test_using_session_fixture(test_environment):
    """Test using session-scoped fixture."""

    @rewrite_step("Execute test query")
    def query_db(sql: str):
        print(f"SQL: {sql}")
        return [{"id": 1}]

    with rewrite_step("Database test"):
        result = query_db("SELECT * FROM users")
        assert len(result) > 0


# ==============================================================================
# Combining with pytest.raises
# ==============================================================================

def test_with_exception_handling():
    """Test error handling with rewrite_step."""

    @rewrite_step("Operation that may fail")
    def risky_operation():
        raise ValueError("Something went wrong")

    with pytest.raises(ValueError):
        with rewrite_step("Test error handling"):
            risky_operation()


# ==============================================================================
# Pytest xfail and skip with rewrite_step
# ==============================================================================

@pytest.mark.xfail(reason="Known bug in API")
def test_xfail_with_rewrite_step():
    """Test expected to fail."""

    @rewrite_step("Call buggy API")
    def buggy_api():
        return None  # Should return data

    with rewrite_step("Test with known bug"):
        result = buggy_api()
        assert result is not None  # This will fail


@pytest.mark.skip(reason="Not implemented yet")
def test_skip_with_rewrite_step():
    """Test that is skipped."""

    @rewrite_step("Feature not ready")
    def not_implemented():
        pass

    with rewrite_step("Future feature test"):
        not_implemented()


# ==============================================================================
# Pytest subtests (if available)
# ==============================================================================

def test_with_subtests():
    """Test using subtests pattern with rewrite_step."""

    @rewrite_step("Validate field")
    def validate_field(field: str, value: str):
        print(f"Validating {field}: {value}")
        return len(value) > 0

    test_data = [
        ("username", "john"),
        ("email", "john@example.com"),
        ("password", "secret123"),
    ]

    for field, value in test_data:
        with rewrite_step(f"Validate {field}"):
            assert validate_field(field, value)


# ==============================================================================
# Real-world pytest integration example
# ==============================================================================

class TestUserAPI:
    """Test class demonstrating real-world usage."""

    @pytest.fixture(autouse=True)
    def setup_method_fixture(self):
        """Setup for each test method."""
        with rewrite_step("Setup test data"):
            self.test_user = {"id": 1, "name": "Test User"}
            self.api_url = "https://api.example.com"

    @pytest.mark.parametrize("user_id", [1, 2, 3])
    def test_get_user(self, user_id):
        """Test GET user endpoint."""

        @rewrite_step("Send GET request")
        def get_user(uid: int):
            print(f"GET {self.api_url}/users/{uid}")
            return {"id": uid, "name": f"User {uid}"}

        @rewrite_step("Validate response")
        def validate(response: dict):
            return "id" in response and "name" in response

        with rewrite_step(f"Test GET /users/{user_id}"):
            response = get_user(user_id)
            assert validate(response)
            assert response["id"] == user_id

    def test_create_user(self):
        """Test POST user endpoint."""

        @rewrite_step("Prepare request data")
        def prepare_data():
            return {"name": "New User", "email": "new@example.com"}

        @rewrite_step("Send POST request")
        def create_user(data: dict):
            print(f"POST {self.api_url}/users")
            return {"id": 4, **data}

        with rewrite_step("Test POST /users"):
            data = prepare_data()
            response = create_user(data)
            assert response["id"] == 4
            assert response["name"] == data["name"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
