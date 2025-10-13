"""
Core functionality for rewriting Allure step titles.

This module provides the rewrite_step decorator and context manager
that allows overriding Allure step titles without creating nested steps.
"""

import threading
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Dict, Optional

import allure


# Thread-local storage for step contexts
_active_step_contexts: Dict[int, Dict[str, Any]] = {}


def _current_thread_id() -> int:
    """Get current thread ID."""
    return threading.get_ident()


def rewrite_step(title: str = "") -> "AllureStepWrapper":
    """
    Create a step with the ability to override nested step titles.

    Can be used as a decorator or context manager.

    Args:
        title: Step title (optional)

    Returns:
        AllureStepWrapper instance

    Examples:
        As a decorator:
            >>> @rewrite_step("Default title")
            >>> def my_function():
            >>>     pass

        As a context manager:
            >>> with rewrite_step("Custom title"):
            >>>     my_function()

        With step_title parameter:
            >>> @rewrite_step()
            >>> def my_function():
            >>>     pass
            >>> my_function(step_title="Custom title")
    """
    if callable(title):
        # Called as @rewrite_step without parentheses
        return AllureStepWrapper(title.__name__)(title)
    else:
        return AllureStepWrapper(title)


class AllureStepWrapper:
    """
    Wrapper for Allure steps with override support.

    This class allows rewriting step titles without creating nested steps.
    When used as a context manager, it can override the title of steps
    created inside its context.
    """

    def __init__(self, title: str) -> None:
        """
        Initialize the wrapper.

        Args:
            title: Step title
        """
        self.desc = title
        self.step_context = None

    def __call__(self, func: Callable) -> Callable:
        """
        Decorator for wrapping a function in an Allure step.

        Args:
            func: Function to wrap

        Returns:
            Wrapped function
        """

        @wraps(func)
        def impl(*args, **kwargs) -> Any:
            step_title = kwargs.pop("step_title", None) or self.desc
            thread_id = _current_thread_id()

            # Check if we can override the step
            if self._can_override_step(thread_id, step_title):
                return func(*args, **kwargs)

            # Create a new step
            with allure.step(step_title):
                return func(*args, **kwargs)

        return impl

    def _can_override_step(self, thread_id: int, step_title: str) -> bool:
        """
        Check if step can be overridden.

        Args:
            thread_id: Current thread ID
            step_title: New step title

        Returns:
            True if step was overridden, False otherwise
        """
        if thread_id not in _active_step_contexts:
            return False

        external_context = _active_step_contexts[thread_id]
        if not external_context or not external_context.get("can_override"):
            return False

        # Override the step title
        external_context["title"] = step_title
        external_context["can_override"] = False
        return True

    def __enter__(self) -> Any:
        """
        Enter step context.

        Returns:
            Allure step context or None if overridden
        """
        thread_id = _current_thread_id()

        # Check if we can override an existing step
        if self._can_override_step_context(thread_id):
            return None

        # Create a new step context
        _active_step_contexts[thread_id] = {
            "title": self.desc,
            "can_override": True,
            "context": None,
        }

        self.step_context = allure.step(self.desc)
        _active_step_contexts[thread_id]["context"] = self.step_context

        return self.step_context.__enter__()

    def _can_override_step_context(self, thread_id: int) -> bool:
        """
        Check if context manager can override an existing step.

        Args:
            thread_id: Current thread ID

        Returns:
            True if step was overridden, False otherwise
        """
        if thread_id not in _active_step_contexts:
            return False

        external_context = _active_step_contexts[thread_id]
        if not external_context or not external_context.get("can_override"):
            return False

        # Override the title of the existing context
        external_context["title"] = self.desc
        external_context["can_override"] = False

        # Store reference to the external context
        self.step_context = external_context["context"]
        return True

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit step context.

        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        thread_id = _current_thread_id()

        # If this is an overridden context, don't close it
        if not hasattr(self, "step_context") or self.step_context is None:
            return

        # If we own the context, close it
        if thread_id in _active_step_contexts:
            try:
                if self.step_context:
                    self.step_context.__exit__(exc_type, exc_val, exc_tb)
            except Exception:
                # Force close on error
                try:
                    if self.step_context:
                        self.step_context.__exit__(exc_type, exc_val, exc_tb)
                except Exception:
                    pass
            finally:
                _active_step_contexts.pop(thread_id, None)
        else:
            # Just close the step without removing context
            try:
                if self.step_context:
                    self.step_context.__exit__(exc_type, exc_val, exc_tb)
            except Exception:
                pass