"""Tests for rewrite_step used as a decorator."""

from allure_step_rewriter import rewrite_step


class TestRewriteStepDecorator:
    """Test rewrite_step decorator functionality."""

    def test_decorator_with_default_title(self):
        """Test decorator with default title."""

        @rewrite_step("Default title")
        def sample_func():
            return "result"

        result = sample_func()
        assert result == "result"

    def test_decorator_without_parentheses(self):
        """Test decorator without parentheses."""

        @rewrite_step
        def sample_func():
            return "result"

        result = sample_func()
        assert result == "result"

    def test_decorator_with_step_title_parameter(self):
        """Test decorator with step_title parameter."""

        @rewrite_step("Default title")
        def sample_func():
            return "result"

        result = sample_func(step_title="Custom title")
        assert result == "result"

    def test_decorator_with_args_and_kwargs(self):
        """Test decorator with function arguments."""

        @rewrite_step("Process data")
        def process_data(value: int, multiplier: int = 2):
            return value * multiplier

        result = process_data(5, multiplier=3)
        assert result == 15

    def test_decorator_preserves_function_name(self):
        """Test that decorator preserves original function name."""

        @rewrite_step("Step title")
        def my_function():
            pass

        assert my_function.__name__ == "my_function"

    def test_nested_decorated_functions(self):
        """Test nested decorated functions."""

        @rewrite_step("Outer step")
        def outer_function():
            return inner_function()

        @rewrite_step("Inner step")
        def inner_function():
            return "inner result"

        result = outer_function()
        assert result == "inner result"
