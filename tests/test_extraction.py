"""Tests for _extract_implementations function."""

from plumkdocs.main import Implementation, _extract_implementations


class TestExtractImplementations:
    """Tests for _extract_implementations function."""

    def test_extract_single_implementation(self):
        """Test extracting from function with single implementation."""
        from tests.fixtures.sample_functions import func_no_docs

        plum_func = ("func_no_docs", func_no_docs)
        implementations = _extract_implementations(plum_func)

        assert len(implementations) == 1
        assert isinstance(implementations[0], Implementation)
        assert implementations[0].name == "func_no_docs"

    def test_extract_multiple_implementations(self, plum_function_simple):
        """Test extracting from function with multiple implementations."""
        implementations = _extract_implementations(plum_function_simple)

        # simple_func has implementations for int, int and str, str
        assert len(implementations) >= 2
        assert all(isinstance(impl, Implementation) for impl in implementations)
        assert all(impl.name == "simple_func" for impl in implementations)

    def test_implementations_are_sorted(self, plum_function_simple):
        """Test that implementations are sorted by signature."""
        implementations = _extract_implementations(plum_function_simple)

        # Extract signatures for comparison
        signatures = [impl._signature for impl in implementations]

        # Signatures should be sorted (alphabetically)
        assert signatures == sorted(signatures)

    def test_deduplication_of_identical_signatures(self):
        """Test that duplicate signatures are removed."""
        from tests.fixtures.sample_functions import simple_func

        plum_func = ("simple_func", simple_func)
        implementations = _extract_implementations(plum_func)

        # Get all signatures
        signatures = [impl._signature for impl in implementations]

        # All signatures should be unique
        assert len(signatures) == len(set(signatures))

    def test_implementation_with_defaults(self, plum_function_with_defaults):
        """Test extracting implementations with default parameters."""
        implementations = _extract_implementations(plum_function_with_defaults)

        assert len(implementations) >= 1
        # Check that default values are captured
        impl = implementations[0]
        assert "10" in impl._signature or "=" in impl._signature

    def test_implementation_with_kwonly(self, plum_function_kwonly):
        """Test extracting implementations with keyword-only arguments."""
        implementations = _extract_implementations(plum_function_kwonly)

        assert len(implementations) >= 1
        # Keyword-only args should have * separator
        impl = implementations[0]
        assert "*" in impl._signature

    def test_implementation_preserves_docstrings(self, plum_function_simple):
        """Test that docstrings are preserved in implementations."""
        implementations = _extract_implementations(plum_function_simple)

        # At least some implementations should have docs
        docs_present = any(len(impl.docs) > 0 for impl in implementations)
        assert docs_present

    def test_implementation_handles_empty_docstrings(self, plum_function_no_docs):
        """Test that empty docstrings are handled gracefully."""
        implementations = _extract_implementations(plum_function_no_docs)

        assert len(implementations) >= 1
        # Should not crash with empty docs
        assert isinstance(implementations[0].docs, str)

    def test_implementation_name_matches_function_name(self, plum_function_markdown):
        """Test that implementation name matches the function name."""
        implementations = _extract_implementations(plum_function_markdown)

        assert all(impl.name == "func_markdown_docs" for impl in implementations)

    def test_implementation_params_are_captured(self, plum_function_with_defaults):
        """Test that parameter information is captured."""
        implementations = _extract_implementations(plum_function_with_defaults)

        impl = implementations[0]
        assert impl.params is not None
        assert len(impl.params) > 0
        # Check that parameter names are in the params dict
        param_names = list(impl.params.keys())
        assert len(param_names) > 0
