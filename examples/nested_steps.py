"""
Nested steps example - combining rewrite_step with allure.step for hierarchical structure

Run with: pytest examples/nested_steps.py --alluredir=allure-results
View report: allure serve allure-results
"""

import pytest
import allure
from allure_step_rewriter import rewrite_step


@rewrite_step("API call")
def api_call(endpoint: str):
    print(f"Calling {endpoint}")
    return {"status": "success"}


@rewrite_step("Database query")
def db_query(sql: str):
    print(f"Executing: {sql}")
    return [{"id": 1, "name": "Test"}]


@rewrite_step("Validate data")
def validate(data):
    print(f"Validating: {data}")
    return True


def test_rewrite_step_with_nested_allure_steps():
    """
    Example: Use rewrite_step for main flow, allure.step for nested structure.

    Result in Allure:
    ✓ Test Scenario
      ✓ Preparation
      ✓ Execution
      ✓ Validation
    """
    with rewrite_step("Test Scenario"):
        # These API calls are overridden - no separate steps
        api_call("/api/setup")
        api_call("/api/config")

        # Create nested step for grouped actions
        with allure.step("Preparation"):
            db_query("SELECT * FROM users")
            api_call("/api/init")

        # Another nested step
        with allure.step("Execution"):
            api_call("/api/execute")
            api_call("/api/process")

        # Another nested step
        with allure.step("Validation"):
            result = api_call("/api/status")
            validate(result)


def test_allure_step_containing_rewrite_step():
    """
    Example: Use allure.step as parent, rewrite_step inside.

    Result in Allure:
    ✓ Main Test Flow (allure.step)
      ✓ Subprocess A (rewrite_step)
      ✓ Subprocess B (rewrite_step)
    """
    with allure.step("Main Test Flow"):
        # Each rewrite_step creates a nested step
        with rewrite_step("Subprocess A"):
            api_call("/api/a1")  # Overridden to "Subprocess A"
            api_call("/api/a2")  # Overridden to "Subprocess A"

        with rewrite_step("Subprocess B"):
            api_call("/api/b1")  # Overridden to "Subprocess B"
            api_call("/api/b2")  # Overridden to "Subprocess B"


def test_complex_nesting():
    """
    Complex example with multiple levels of nesting.

    Result in Allure:
    ✓ E2E Test
      ✓ Phase 1: Initialization (allure.step)
        ✓ Background Jobs (rewrite_step)
      ✓ Phase 2: Testing (allure.step)
        ✓ Test Suite A (rewrite_step)
        ✓ Test Suite B (rewrite_step)
      ✓ Phase 3: Cleanup (allure.step)
    """
    with rewrite_step("E2E Test"):
        api_call("/api/start")

        with allure.step("Phase 1: Initialization"):
            api_call("/api/prepare")

            # Nested rewrite_step inside allure.step
            with rewrite_step("Background Jobs"):
                api_call("/api/job1")
                api_call("/api/job2")
                api_call("/api/job3")

        with allure.step("Phase 2: Testing"):
            with rewrite_step("Test Suite A"):
                api_call("/api/test/a1")
                api_call("/api/test/a2")

            with rewrite_step("Test Suite B"):
                api_call("/api/test/b1")
                api_call("/api/test/b2")

        with allure.step("Phase 3: Cleanup"):
            api_call("/api/cleanup")
            validate({"status": "clean"})


def test_when_to_use_what():
    """
    Guidelines example: When to use rewrite_step vs allure.step.
    """

    @rewrite_step("Generic action")
    def generic_action(what: str):
        print(f"Doing: {what}")
        return True

    # BAD: Trying to nest rewrite_step in rewrite_step (doesn't work as expected)
    with rewrite_step("Level 1"):
        with rewrite_step("Level 2"):  # This WON'T create nested step!
            generic_action("something")
    # Result: Only 1 step "Level 1" (Level 2 doesn't appear!)

    # GOOD: Use allure.step for hierarchy
    with rewrite_step("Parent"):
        generic_action("a")  # Overridden

        with allure.step("Child 1"):  # Creates nested step
            generic_action("b")  # Inside Child 1

        with allure.step("Child 2"):  # Creates nested step
            generic_action("c")  # Inside Child 2

        generic_action("d")  # Overridden
    # Result: Parent with 2 children


def test_best_practices():
    """
    Best practices for combining rewrite_step and allure.step.
    """

    @rewrite_step("Low-level operation")
    def low_level_op(name: str):
        print(f"Operation: {name}")
        return True

    # RULE 1: Use rewrite_step context to collapse multiple operations
    with rewrite_step("High-level business operation"):
        low_level_op("step1")
        low_level_op("step2")
        low_level_op("step3")
        # Result: 1 step

    # RULE 2: Use allure.step when you need hierarchical structure
    with rewrite_step("Test Case"):
        with allure.step("Given: Preconditions"):
            low_level_op("setup1")
            low_level_op("setup2")

        with allure.step("When: Action"):
            low_level_op("action")

        with allure.step("Then: Verification"):
            low_level_op("check1")
            low_level_op("check2")
    # Result: Test Case with 3 children (Given/When/Then)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
