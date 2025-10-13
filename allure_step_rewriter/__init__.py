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