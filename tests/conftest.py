"""Pytest configuration and fixtures."""

import inspect
import os
import sys

import pytest
from plum import dispatch

# Add parent directory to sys.path to allow importing tests.fixtures
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def simple_implementation_params():
    """Return sample parameters for Implementation testing."""

    @dispatch
    def sample(a: int, b: str = "default"):
        """Sample docstring.

        Args:
            a (int): First parameter.
            b (str): Second parameter.

        Returns:
            str: Result string.
        """
        return f"{a}{b}"

    return {
        "name": "sample",
        "params": inspect.signature(sample).parameters,
        "docs": inspect.getdoc(sample),
    }


@pytest.fixture
def empty_docstring_params():
    """Return parameters with empty docstring."""

    @dispatch
    def no_docs(x: int):
        return x * 2

    return {
        "name": "no_docs",
        "params": inspect.signature(no_docs).parameters,
        "docs": "",
    }


@pytest.fixture
def plum_function_simple():
    """Return a simple plum Function object."""
    from tests.fixtures.sample_functions import simple_func

    return ("simple_func", simple_func)


@pytest.fixture
def plum_function_with_defaults():
    """Return a plum Function with default parameters."""
    from tests.fixtures.sample_functions import func_with_defaults

    return ("func_with_defaults", func_with_defaults)


@pytest.fixture
def plum_function_kwonly():
    """Return a plum Function with keyword-only args."""
    from tests.fixtures.sample_functions import func_with_kwonly

    return ("func_with_kwonly", func_with_kwonly)


@pytest.fixture
def plum_function_no_docs():
    """Return a plum Function with minimal docs."""
    from tests.fixtures.sample_functions import func_no_docs

    return ("func_no_docs", func_no_docs)


@pytest.fixture
def plum_function_markdown():
    """Return a plum Function with markdown in docs."""
    from tests.fixtures.sample_functions import func_markdown_docs

    return ("func_markdown_docs", func_markdown_docs)


@pytest.fixture
def mock_env():
    """Return a mock mkdocs-macros environment."""

    class MockEnv:
        def __init__(self):
            self.macros = {}

        def macro(self, func):
            """Decorator to register a macro."""
            self.macros[func.__name__] = func
            return func

    return MockEnv()
