"""Tests for error handling in rewrite_step."""

import pytest
from unittest import mock
from allure_step_rewriter import rewrite_step


class TestErrorHandling:
    """Test error handling in various scenarios."""

    def test_context_manager_with_exception_inside(self):
        """Test that exceptions inside context are properly propagated."""

        @rewrite_step("Test step")
        def failing_function():
            raise ValueError("Test error")

        # Exception should be propagated
        with pytest.raises(ValueError, match="Test error"):
            with rewrite_step("Outer step"):
                failing_function()

    def test_context_manager_exit_with_exception_cleanup(self):
        """Test that context cleanup happens even with exceptions."""
        exception_raised = False

        @rewrite_step("Test step")
        def sample_func():
            nonlocal exception_raised
            exception_raised = True
            raise RuntimeError("Intentional error")

        with pytest.raises(RuntimeError, match="Intentional error"):
            with rewrite_step("Parent step"):
                sample_func()

        assert exception_raised

    def test_multiple_exit_calls_do_not_fail(self):
        """Test that multiple __exit__ calls don't cause errors."""
        wrapper = rewrite_step("Test")

        # Enter and exit normally
        wrapper.__enter__()
        wrapper.__exit__(None, None, None)

        # Second exit should not fail (defensive programming)
        try:
            wrapper.__exit__(None, None, None)
        except Exception as e:
            pytest.fail(f"Second __exit__ call raised exception: {e}")

    def test_nested_contexts_with_exception(self):
        """Test nested contexts handle exceptions properly."""

        @rewrite_step("Inner function")
        def inner_func():
            raise ValueError("Inner error")

        with pytest.raises(ValueError, match="Inner error"):
            with rewrite_step("Outer"):
                with rewrite_step("Middle"):
                    inner_func()

    def test_exception_during_step_creation(self):
        """Test handling of exceptions during step creation."""

        @rewrite_step("Normal step")
        def normal_func():
            return "success"

        # Mock allure.step to raise an exception
        with mock.patch("allure.step") as mock_step:
            mock_step.side_effect = RuntimeError("Step creation failed")

            # Should propagate the exception
            with pytest.raises(RuntimeError, match="Step creation failed"):
                with rewrite_step("Test"):
                    pass

    def test_context_override_with_exception(self):
        """Test that override works correctly when exception occurs."""

        @rewrite_step("Function A")
        def func_a():
            return "A"

        @rewrite_step("Function B")
        def func_b():
            raise ValueError("Error in B")

        with pytest.raises(ValueError, match="Error in B"):
            with rewrite_step("Parent", allow_multiple=True):
                result = func_a()
                assert result == "A"
                func_b()  # This will raise

    def test_step_context_cleanup_after_error(self):
        """Test that thread-local context is cleaned up after error."""
        from allure_step_rewriter.rewrite_step import (
            _active_step_contexts,
            _current_thread_id,
        )

        @rewrite_step("Test")
        def failing():
            raise ValueError("Test")

        thread_id = _current_thread_id()

        # Clean up any leftover context from previous tests
        _active_step_contexts.pop(thread_id, None)

        # Run context with exception
        with pytest.raises(ValueError):
            with rewrite_step("Outer"):
                failing()

        # After exception, context should be cleaned up
        assert thread_id not in _active_step_contexts or not _active_step_contexts.get(
            thread_id
        )

    def test_decorator_with_exception_in_function(self):
        """Test that decorator properly handles exceptions in wrapped function."""

        @rewrite_step("Decorated function")
        def failing_func(should_fail: bool):
            if should_fail:
                raise ValueError("Function failed")
            return "success"

        # Should work normally
        assert failing_func(False) == "success"

        # Should propagate exception
        with pytest.raises(ValueError, match="Function failed"):
            failing_func(True)

    def test_exit_with_exception_info(self):
        """Test __exit__ receives exception information correctly."""

        class CustomError(Exception):
            pass

        @rewrite_step("Test")
        def raising_func():
            raise CustomError("Custom error")

        with pytest.raises(CustomError, match="Custom error"):
            with rewrite_step("Parent"):
                raising_func()
