"""Tests for module import and dependency checks."""

import sys
import pytest
from unittest import mock


class TestImport:
    """Test import functionality and error handling."""

    def test_import_success_with_allure(self):
        """Test that import works when allure-pytest is installed."""
        # This test runs in environment with allure-pytest installed
        from allure_step_rewriter import rewrite_step, AllureStepWrapper, __version__

        assert rewrite_step is not None
        assert AllureStepWrapper is not None
        assert __version__ is not None

    def test_import_error_without_allure(self):
        """Test that import fails with helpful message when allure-pytest is not installed."""
        # Mock the allure module to simulate it not being installed
        with mock.patch.dict('sys.modules', {'allure': None}):
            # Remove the module from cache if it was already imported
            if 'allure_step_rewriter' in sys.modules:
                del sys.modules['allure_step_rewriter']
            if 'allure_step_rewriter.rewrite_step' in sys.modules:
                del sys.modules['allure_step_rewriter.rewrite_step']

            # Try to import and expect ImportError
            with pytest.raises(ImportError) as exc_info:
                # This will trigger the import error check in __init__.py
                import importlib
                importlib.import_module('allure_step_rewriter')

            # Check error message contains helpful instructions
            error_message = str(exc_info.value)
            assert "allure-pytest" in error_message.lower()
            assert "pip install" in error_message.lower()

    def test_all_exports(self):
        """Test that __all__ contains expected exports."""
        from allure_step_rewriter import __all__

        assert "rewrite_step" in __all__
        assert "AllureStepWrapper" in __all__
        assert "__version__" in __all__

    def test_version_format(self):
        """Test that version follows semantic versioning."""
        from allure_step_rewriter import __version__

        # Should be in format X.Y.Z
        parts = __version__.split('.')
        assert len(parts) == 3
        assert all(part.isdigit() for part in parts)
