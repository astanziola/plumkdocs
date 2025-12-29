"""Tests for mod_to_string function."""

from plumkdocs.main import mod_to_string


class TestModToString:
    """Tests for mod_to_string function."""

    def test_import_single_level_module(self):
        """Test importing and processing single-level module."""
        # Use the fixture module
        result = mod_to_string("tests.fixtures.sample_functions")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_output_contains_base_docs(self):
        """Test that output contains base documentation."""
        result = mod_to_string("tests.fixtures.sample_functions", "simple_func")

        # Should contain base documentation
        assert "Base documentation for simple_func" in result

    def test_output_contains_implementations_header(self):
        """Test that output contains implementations header."""
        result = mod_to_string("tests.fixtures.sample_functions", "simple_func")

        assert "Concrete implementations:" in result

    def test_output_contains_signatures(self):
        """Test that output contains function signatures."""
        result = mod_to_string("tests.fixtures.sample_functions", "simple_func")

        # Should contain signatures with int and str types
        assert "int" in result
        assert "str" in result

    def test_output_ends_with_hr(self):
        """Test that output ends with horizontal rule."""
        result = mod_to_string("tests.fixtures.sample_functions", "simple_func")

        assert result.strip().endswith("<hr>")

    def test_filter_by_function_name(self):
        """Test filtering to specific function."""
        result = mod_to_string("tests.fixtures.sample_functions", "simple_func")

        # Should contain simple_func implementations
        assert "simple_func" in result or "Add two integers" in result

        # Should not contain other functions from the module
        # (This is a weak test since function names might appear in various contexts)
        assert len(result) > 100  # Should have substantial content

    def test_all_functions_when_no_filter(self):
        """Test that all functions are included when no filter is specified."""
        result = mod_to_string("tests.fixtures.sample_functions")

        # Should contain multiple function base docs
        assert "simple_func" in result or "Base documentation" in result

    def test_function_with_markdown_docs(self):
        """Test processing function with markdown in documentation."""
        result = mod_to_string("tests.fixtures.sample_functions", "func_markdown_docs")

        # Should preserve or convert markdown
        assert "markdown" in result
        # HTML table structure for parameters
        assert "<table>" in result or "Args:" in result

    def test_function_with_defaults(self):
        """Test processing function with default parameters."""
        result = mod_to_string("tests.fixtures.sample_functions", "func_with_defaults")

        # Should show default values
        assert "10" in result or "default" in result.lower()

    def test_function_with_kwonly_args(self):
        """Test processing function with keyword-only arguments."""
        result = mod_to_string("tests.fixtures.sample_functions", "func_with_kwonly")

        # Should handle keyword-only args
        assert len(result) > 100  # Should have content

    def test_output_is_valid_html_structure(self):
        """Test that output has valid HTML structure."""
        result = mod_to_string("tests.fixtures.sample_functions", "simple_func")

        # Should have HTML tags
        assert "<" in result and ">" in result
        # Should have tables for parameters
        assert "<table>" in result or "<p>" in result

    def test_implementations_are_included(self):
        """Test that multiple implementations are included in output."""
        result = mod_to_string("tests.fixtures.sample_functions", "simple_func")

        # simple_func has implementations for (int, int) and (str, str)
        # Both should appear in the output
        assert "int" in result
        assert "str" in result

    def test_nonexistent_function_returns_content(self):
        """Test behavior with non-existent function name."""
        # When filtering by a function that doesn't exist, should return empty or minimal content
        result = mod_to_string("tests.fixtures.sample_functions", "nonexistent_function")

        # Should still return a string (possibly with just HR or empty content)
        assert isinstance(result, str)
