"""Tests for multiple step overrides in single context."""

import pytest
import allure
from allure_step_rewriter import rewrite_step


class TestMultipleOverrides:
    """Test multiple step overrides functionality."""

    def test_multiple_overrides_in_single_context(self):
        """Test that multiple decorated functions can be overridden in single context."""

        @rewrite_step("Default A")
        def func_a():
            return "A"

        @rewrite_step("Default B")
        def func_b():
            return "B"

        @rewrite_step("Default C")
        def func_c():
            return "C"

        # Use allow_multiple=True to override all three functions
        with rewrite_step("Parent Step", allow_multiple=True):
            result_a = func_a()
            result_b = func_b()
            result_c = func_c()

        assert result_a == "A"
        assert result_b == "B"
        assert result_c == "C"

    def test_rewrite_step_with_nested_allure_step(self):
        """Test combining rewrite_step with nested allure.step for hierarchical structure."""

        @rewrite_step("Function A")
        def func_a():
            return "A"

        @rewrite_step("Function B")
        def func_b():
            return "B"

        # Use allow_multiple=True to override multiple calls
        with rewrite_step("Parent Step", allow_multiple=True):
            result_a = func_a()  # Should override to "Parent Step"

            # Create nested step using allure.step
            with allure.step("Nested Step"):
                result_b = func_b()  # Inside nested step

            result_c = func_a()  # Should override to "Parent Step" again

        assert result_a == "A"
        assert result_b == "B"
        assert result_c == "A"

    def test_allure_step_with_rewrite_step_inside(self):
        """Test using rewrite_step inside allure.step context."""

        @rewrite_step("Function A")
        def func_a():
            return "A"

        @rewrite_step("Function B")
        def func_b():
            return "B"

        with allure.step("Parent Allure Step"):
            # Inside allure.step, decorated functions should create nested steps
            result_a = func_a()

            # Create rewrite_step context
            with rewrite_step("Rewrite Context"):
                result_b = func_b()  # Should override to "Rewrite Context"

        assert result_a == "A"
        assert result_b == "B"

    def test_multiple_overrides_then_nested_steps(self):
        """Test multiple overrides followed by nested steps using allure.step."""

        @rewrite_step("Function A")
        def func_a():
            return "A"

        @rewrite_step("Function B")
        def func_b():
            return "B"

        with rewrite_step("Parent"):
            result_a = func_a()  # Override
            result_b = func_b()  # Override

            # When nested step is needed, use allure.step
            with allure.step("Child Step 1"):
                result_c = func_a()

            with allure.step("Child Step 2"):
                result_d = func_b()

        assert result_a == "A"
        assert result_b == "B"
        assert result_c == "A"
        assert result_d == "B"

    def test_complex_nesting_combination(self):
        """Test complex nesting with combination of rewrite_step and allure.step."""

        @rewrite_step("Function A")
        def func_a():
            return "A"

        @rewrite_step("Function B")
        def func_b():
            return "B"

        with rewrite_step("Level 1"):
            result_1 = func_a()  # Override to "Level 1"

            with allure.step("Level 2 (allure.step)"):
                result_2 = func_b()  # Creates step "Function B"

                with rewrite_step("Level 3 (rewrite_step)"):
                    result_3 = func_a()  # Override to "Level 3"
                    result_4 = func_b()  # Override to "Level 3"

        assert result_1 == "A"
        assert result_2 == "B"
        assert result_3 == "A"
        assert result_4 == "B"

    def test_sequential_rewrite_contexts_with_overrides(self):
        """Test multiple sequential rewrite_step contexts each with multiple overrides."""

        @rewrite_step("Default")
        def sample_func():
            return "result"

        # First context with multiple overrides
        with rewrite_step("Context 1"):
            r1 = sample_func()
            r2 = sample_func()

        # Second context with multiple overrides
        with rewrite_step("Context 2"):
            r3 = sample_func()
            r4 = sample_func()

        assert r1 == "result"
        assert r2 == "result"
        assert r3 == "result"
        assert r4 == "result"
