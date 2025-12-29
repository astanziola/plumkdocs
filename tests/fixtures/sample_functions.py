"""Sample plum dispatch functions for testing."""

from plum import dispatch


@dispatch.abstract
def simple_func(a, b):
    """Base documentation for simple_func.

    This is a simple test function with multiple implementations.
    """
    pass


@dispatch
def simple_func(a: int, b: int):
    """Add two integers.

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        int: Sum of a and b.
    """
    return a + b


@dispatch
def simple_func(a: str, b: str):
    """Concatenate two strings.

    Args:
        a (str): First string.
        b (str): Second string.

    Returns:
        str: Concatenation of a and b.
    """
    return a + b


@dispatch.abstract
def func_with_defaults(x, y=10):
    """Function with default parameters."""
    pass


@dispatch
def func_with_defaults(x: int, y: int = 10):
    """Multiply two numbers.

    Args:
        x (int): First number.
        y (int): Second number (default: 10).

    Returns:
        int: Product of x and y.
    """
    return x * y


@dispatch.abstract
def func_with_kwonly(a, *, b):
    """Function with keyword-only arguments."""
    pass


@dispatch
def func_with_kwonly(a: int, *, b: int):
    """Subtract b from a.

    Args:
        a (int): First number.
        b (int): Second number (keyword-only).

    Returns:
        int: Difference a - b.
    """
    return a - b


@dispatch.abstract
def func_no_docs(x):
    """Base docs only."""
    pass


@dispatch
def func_no_docs(x: int):
    return x * 2


@dispatch.abstract
def func_markdown_docs(text):
    """Function with **markdown** in docs.

    This supports `code blocks`:

    ```python
    >>> func_markdown_docs("hello")
    'HELLO'
    ```

    And even lists:
    - Item 1
    - Item 2
    """
    pass


@dispatch
def func_markdown_docs(text: str):
    """Convert text to uppercase.

    Args:
        text (str): Input text with *markdown* support.

    Returns:
        str: Uppercase text.
    """
    return text.upper()
