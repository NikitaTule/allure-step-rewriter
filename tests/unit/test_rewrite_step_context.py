"""Tests for rewrite_step used as a context manager."""

import pytest
from allure_step_rewriter import rewrite_step


class TestRewriteStepContext:
    """Test rewrite_step context manager functionality."""

    def test_context_manager_basic(self):
        """Test basic context manager usage."""
        with rewrite_step("Test step"):
            result = "test"

        assert result == "test"

    def test_context_manager_with_function_call(self, sample_function):
        """Test context manager wrapping a function call."""
        with rewrite_step("Execute function"):
            result = sample_function("value")

        assert result == "result: value"

    def test_context_manager_overrides_decorator(self):
        """Test that context manager can override decorator title."""

        @rewrite_step("Default title")
        def sample_func():
            return "result"

        with rewrite_step("Custom title"):
            result = sample_func()

        assert result == "result"

    def test_nested_context_managers(self):
        """Test nested context managers."""
        with rewrite_step("Outer step"):
            outer_value = "outer"

            with rewrite_step("Inner step"):
                inner_value = "inner"

        assert outer_value == "outer"
        assert inner_value == "inner"

    def test_context_manager_with_exception(self):
        """Test context manager behavior with exceptions."""
        with pytest.raises(ValueError):
            with rewrite_step("Step with error"):
                raise ValueError("Test error")

    def test_multiple_sequential_contexts(self):
        """Test multiple sequential context managers."""
        with rewrite_step("Step 1"):
            result1 = "first"

        with rewrite_step("Step 2"):
            result2 = "second"

        with rewrite_step("Step 3"):
            result3 = "third"

        assert result1 == "first"
        assert result2 == "second"
        assert result3 == "third"