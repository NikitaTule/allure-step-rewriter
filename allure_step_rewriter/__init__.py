"""
Allure Step Rewriter
====================

A library for rewriting Allure step titles without creating nested steps.

Basic usage:
    >>> from allure_step_rewriter import rewrite_step
    >>>
    >>> @rewrite_step("Default step title")
    >>> def my_function():
    >>>     pass
    >>>
    >>> with rewrite_step("Custom step title"):
    >>>     my_function()

For more information, see: https://github.com/NikitaTule/allure-step-rewriter
"""

# Check that allure-pytest is installed
try:
    import allure
except ImportError as e:
    raise ImportError(
        "allure-step-rewriter requires 'allure-pytest' to be installed.\n\n"
        "Install it with one of the following commands:\n"
        "  pip install allure-pytest>=2.9.0\n"
        "  pip install allure-step-rewriter[allure]\n"
        "  pip install allure-step-rewriter[all]\n\n"
        "For more information, see: https://github.com/NikitaTule/allure-step-rewriter#installation"
    ) from e

# Check allure-pytest version
try:
    from packaging import version
    import allure_pytest

    # Get version from allure_pytest module
    if hasattr(allure_pytest, "__version__"):
        allure_version = allure_pytest.__version__
        MIN_ALLURE_VERSION = "2.9.0"

        if version.parse(allure_version) < version.parse(MIN_ALLURE_VERSION):
            raise ImportError(
                f"allure-step-rewriter requires allure-pytest>={MIN_ALLURE_VERSION}, "
                f"but found {allure_version}.\n\n"
                f"Upgrade with: pip install --upgrade allure-pytest>={MIN_ALLURE_VERSION}"
            )
except ImportError:
    # packaging not available or allure_pytest doesn't have __version__
    # Skip version check
    pass

from allure_step_rewriter.rewrite_step import (
    rewrite_step,
    AllureStepWrapper,
)
from allure_step_rewriter.version import __version__

__all__ = [
    "rewrite_step",
    "AllureStepWrapper",
    "__version__",
]