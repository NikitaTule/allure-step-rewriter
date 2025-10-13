"""Custom exceptions for allure-step-rewriter."""


class AllureStepRewriterError(Exception):
    """Base exception for allure-step-rewriter."""
    pass


class StepOverrideError(AllureStepRewriterError):
    """Raised when step override fails."""
    pass


class ContextError(AllureStepRewriterError):
    """Raised when context management fails."""
    pass