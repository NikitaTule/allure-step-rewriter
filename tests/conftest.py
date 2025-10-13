"""Pytest configuration and fixtures for tests."""

import pytest


@pytest.fixture
def sample_function():
    """Sample function for testing."""
    def _func(value: str = "test"):
        return f"result: {value}"
    return _func