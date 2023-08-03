from plum import dispatch
from plumkdocs.main import _extract_implementations, var_to_bold, strip_modules

# Define some function to test
@dispatch.abstract
def foo(a, b):
    """Base description of the generic `foo` function
    
    Note that this is supporting markdown

    ```python
    >>> foo(1, 2)
    3
    ```

    as well as LaTeX

    $$
    a + b = c
    $$
    """
    pass

@dispatch
def foo(a: int, b: int):
    """Add two integers.

    Args:
        a (int): First integer.
        b (int): Second integer.
    
    Returns:
        int: Sum of a and b.
    """
    return a + b

@dispatch
def foo(a: str, b: str):
    """Concatenate two strings.

    Args:
        a (str): First string.
        b (str): Second string.
    
    Returns:
        str: Concatenation of a and b.
    """
    return a + b

## Another function
@dispatch.abstract
def bar(a, b):
    """This is yet another function"""

@dispatch
def bar(a: int, b: int):
    """Subtract two integers.   
    
    Args:
        a (int): First integer.
        b (int): Second integer.
    
    Returns:
        int: Difference between a and b.
    """
    return a - b