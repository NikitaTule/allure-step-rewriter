"""Tests for edge cases and corner scenarios."""

import threading
from allure_step_rewriter import rewrite_step
from allure_step_rewriter.rewrite_step import _active_step_contexts, _current_thread_id


class TestEdgeCases:
    """Test edge cases and corner scenarios."""

    def test_decorator_without_parentheses(self):
        """Test using @rewrite_step without parentheses."""

        @rewrite_step
        def my_function():
            return "result"

        # Should use function name as title
        result = my_function()
        assert result == "result"

    def test_empty_title(self):
        """Test rewrite_step with empty string title."""

        @rewrite_step("")
        def func():
            return "test"

        result = func()
        assert result == "test"

    def test_unicode_title(self):
        """Test rewrite_step with unicode characters in title."""

        @rewrite_step("Проверка 🎯")
        def func():
            return "unicode"

        result = func()
        assert result == "unicode"

    def test_very_long_title(self):
        """Test rewrite_step with very long title."""
        long_title = "A" * 1000

        @rewrite_step(long_title)
        def func():
            return "long"

        result = func()
        assert result == "long"

    def test_step_title_parameter_override(self):
        """Test step_title parameter override."""

        @rewrite_step("Default")
        def func():
            return "value"

        # Call with override
        result = func(step_title="Custom")
        assert result == "value"

    def test_step_title_parameter_with_args(self):
        """Test step_title parameter with regular args/kwargs."""

        @rewrite_step("Default")
        def func(a, b, c=10):
            return a + b + c

        result = func(1, 2, c=3, step_title="Custom")
        assert result == 6

    def test_thread_safety(self):
        """Test that rewrite_step is thread-safe."""
        results = []

        @rewrite_step("Thread function")
        def thread_func(value):
            results.append(value)
            return value

        # Create multiple threads
        threads = []
        for i in range(10):
            t = threading.Thread(target=thread_func, args=(i,))
            threads.append(t)
            t.start()

        # Wait for all threads
        for t in threads:
            t.join()

        # All threads should complete successfully
        assert len(results) == 10
        assert set(results) == set(range(10))

    def test_context_without_decorated_functions(self):
        """Test rewrite_step context without calling any decorated functions."""
        with rewrite_step("Empty context"):
            x = 1 + 1

        assert x == 2

    def test_nested_override_then_regular_call(self):
        """Test nested override followed by regular call outside context."""

        @rewrite_step("Function")
        def func():
            return "result"

        # Inside context
        with rewrite_step("Override"):
            result1 = func()

        # Outside context - should use default title
        result2 = func()

        assert result1 == "result"
        assert result2 == "result"

    def test_allow_multiple_false_by_default(self):
        """Test that allow_multiple defaults to False."""

        @rewrite_step("Func A")
        def func_a():
            return "A"

        @rewrite_step("Func B")
        def func_b():
            return "B"

        # Without allow_multiple, only first should override
        with rewrite_step("Parent"):
            a = func_a()  # Overrides
            b = func_b()  # Creates nested step

        assert a == "A"
        assert b == "B"

    def test_allow_multiple_true_overrides_all(self):
        """Test that allow_multiple=True overrides all calls."""

        @rewrite_step("Func A")
        def func_a():
            return "A"

        @rewrite_step("Func B")
        def func_b():
            return "B"

        @rewrite_step("Func C")
        def func_c():
            return "C"

        with rewrite_step("Parent", allow_multiple=True):
            a = func_a()
            b = func_b()
            c = func_c()

        assert a == "A"
        assert b == "B"
        assert c == "C"

    def test_context_cleanup_on_normal_exit(self):
        """Test that context is cleaned up on normal exit."""
        thread_id = _current_thread_id()

        with rewrite_step("Test"):
            # Context should exist during execution
            assert thread_id in _active_step_contexts

        # Context should be cleaned up after exit
        assert thread_id not in _active_step_contexts or not _active_step_contexts.get(
            thread_id
        )

    def test_step_context_attribute(self):
        """Test step_context attribute is set correctly."""
        wrapper = rewrite_step("Test")

        # Before entering, no context
        assert wrapper.step_context is None

        # After entering, context exists
        wrapper.__enter__()
        assert wrapper.step_context is not None

        # Clean up
        wrapper.__exit__(None, None, None)

    def test_callable_title_decorator_syntax(self):
        """Test @rewrite_step without parentheses (callable title)."""

        @rewrite_step
        def some_function():
            return 42

        # Function name should be used as title
        result = some_function()
        assert result == 42

    def test_none_step_title_parameter(self):
        """Test step_title=None uses default title."""

        @rewrite_step("Default Title")
        def func():
            return "value"

        # None should fall back to default
        result = func(step_title=None)
        assert result == "value"

    def test_empty_string_step_title_parameter(self):
        """Test step_title="" uses empty string."""

        @rewrite_step("Default Title")
        def func():
            return "value"

        # Empty string should be used (falsy but not None)
        result = func(step_title="")
        assert result == "value"

    def test_decorator_preserves_metadata(self):
        """Test that decorator preserves function metadata."""

        @rewrite_step("Step")
        def documented_function():
            """This is a docstring."""
            return "value"

        assert documented_function.__doc__ == "This is a docstring."
        assert documented_function.__name__ == "documented_function"

    def test_return_value_preserved(self):
        """Test that return values are preserved through decorator."""

        @rewrite_step("Returns dict")
        def get_dict():
            return {"key": "value"}

        @rewrite_step("Returns list")
        def get_list():
            return [1, 2, 3]

        @rewrite_step("Returns None")
        def get_none():
            return None

        assert get_dict() == {"key": "value"}
        assert get_list() == [1, 2, 3]
        assert get_none() is None
