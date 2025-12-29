"""Tests for define_env function (mkdocs-macros integration)."""

from plumkdocs.main import define_env


class TestDefineEnv:
    """Tests for define_env function."""

    def test_define_env_registers_macro(self, mock_env):
        """Test that define_env registers the implementations macro."""
        define_env(mock_env)

        # Check that the macro was registered
        assert "implementations" in mock_env.macros

    def test_implementations_macro_callable(self, mock_env):
        """Test that the registered macro is callable."""
        define_env(mock_env)

        macro_func = mock_env.macros["implementations"]
        assert callable(macro_func)

    def test_implementations_macro_with_module_only(self, mock_env):
        """Test calling macro with module name only."""
        define_env(mock_env)

        macro_func = mock_env.macros["implementations"]
        result = macro_func("tests.fixtures.sample_functions")

        assert isinstance(result, str)
        assert len(result) > 0

    def test_implementations_macro_with_function(self, mock_env):
        """Test calling macro with module and function name."""
        define_env(mock_env)

        macro_func = mock_env.macros["implementations"]
        result = macro_func("tests.fixtures.sample_functions", "simple_func")

        assert isinstance(result, str)
        assert "simple_func" in result or "Base documentation" in result

    def test_implementations_macro_returns_html(self, mock_env):
        """Test that macro returns HTML content."""
        define_env(mock_env)

        macro_func = mock_env.macros["implementations"]
        result = macro_func("tests.fixtures.sample_functions", "simple_func")

        # Should contain HTML tags
        assert "<" in result and ">" in result
        # Should contain expected HTML elements
        assert "<h3" in result or "<table>" in result or "<hr>" in result

    def test_macro_with_different_functions(self, mock_env):
        """Test macro with different function names."""
        define_env(mock_env)

        macro_func = mock_env.macros["implementations"]

        result1 = macro_func("tests.fixtures.sample_functions", "simple_func")
        result2 = macro_func("tests.fixtures.sample_functions", "func_with_defaults")

        # Results should be different
        assert result1 != result2
        assert len(result1) > 0
        assert len(result2) > 0

    def test_define_env_can_be_called_multiple_times(self, mock_env):
        """Test that define_env can be called multiple times without error."""
        define_env(mock_env)
        define_env(mock_env)  # Should not raise

        # Macro should still be registered
        assert "implementations" in mock_env.macros

    def test_macro_signature(self, mock_env):
        """Test that macro has the expected signature."""
        define_env(mock_env)

        macro_func = mock_env.macros["implementations"]

        # Should accept module and optional function parameter
        import inspect

        sig = inspect.signature(macro_func)
        params = list(sig.parameters.keys())

        assert "module" in params
        assert "function" in params
        # function parameter should have a default (it's optional)
        assert sig.parameters["function"].default is None
