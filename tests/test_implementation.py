"""Tests for the Implementation class."""

import inspect

from plum import dispatch

from plumkdocs.main import Implementation


class TestImplementationInit:
    """Tests for Implementation.__init__."""

    def test_init_with_full_docs(self, simple_implementation_params):
        """Test initialization with complete docstring."""
        impl = Implementation(
            simple_implementation_params["name"],
            simple_implementation_params["params"],
            simple_implementation_params["docs"],
        )
        assert impl.name == "sample"
        assert impl.params == simple_implementation_params["params"]
        assert isinstance(impl.docs, str)
        assert len(impl.docs) > 0

    def test_init_with_empty_docs(self, empty_docstring_params):
        """Test initialization with empty docstring."""
        impl = Implementation(
            empty_docstring_params["name"],
            empty_docstring_params["params"],
            empty_docstring_params["docs"],
        )
        assert impl.name == "no_docs"
        assert impl.docs == ""


class TestImplementationParseDocs:
    """Tests for Implementation.parse_docs."""

    def test_parse_empty_docstring(self):
        """Test parsing empty docstring."""

        @dispatch
        def empty_func():
            pass

        impl = Implementation("empty_func", {}, "")
        assert impl.docs == ""

    def test_parse_text_only_docstring(self):
        """Test parsing docstring with only text section."""
        docs = "Simple description without parameters or returns."
        impl = Implementation("func", {}, docs)
        assert "Simple description" in impl.docs
        assert "<table>" not in impl.docs

    def test_parse_with_parameters(self):
        """Test parsing docstring with parameters section."""

        @dispatch
        def func_with_params(a: int, b: str = "default"):
            """Function with params.

            Args:
                a (int): First parameter.
                b (str): Second parameter with default.
            """
            pass

        params = inspect.signature(func_with_params).parameters
        docs = inspect.getdoc(func_with_params)
        impl = Implementation("func_with_params", params, docs)

        # Check for parameter table
        assert "<strong>Parameters:</strong>" in impl.docs
        assert "<table>" in impl.docs
        assert "<code>a</code>" in impl.docs
        assert "<code>b</code>" in impl.docs
        assert "<em>required</em>" in impl.docs  # 'a' is required
        assert "<code>default</code>" in impl.docs  # 'b' has default

    def test_parse_with_returns(self):
        """Test parsing docstring with returns section."""
        docs = """Calculate something.

        Returns:
            int: The result value.
        """
        impl = Implementation("func", {}, docs)
        assert "<strong>Returns:</strong>" in impl.docs
        assert "<code>int</code>" in impl.docs
        assert "result value" in impl.docs

    def test_parse_with_markdown_in_description(self):
        """Test parsing docstring with markdown in descriptions."""

        @dispatch
        def func_markdown(text: str):
            """Process text.

            Args:
                text (str): Input text with *emphasis* and `code`.
            """
            pass

        params = inspect.signature(func_markdown).parameters
        docs = inspect.getdoc(func_markdown)
        impl = Implementation("func_markdown", params, docs)

        # Markdown should be converted to HTML
        assert "<em>emphasis</em>" in impl.docs or "emphasis" in impl.docs
        assert "<code>" in impl.docs


class TestImplementationParamToString:
    """Tests for Implementation.param_to_string."""

    def test_param_with_type_and_default(self):
        """Test parameter with type annotation and default value."""
        result = Implementation.param_to_string("x", int, 10)
        assert "x" in result
        assert "int" in result
        assert "10" in result

    def test_param_with_type_no_default(self):
        """Test parameter with type annotation but no default."""
        result = Implementation.param_to_string("y", str, inspect._empty)
        assert "y" in result
        assert "str" in result
        assert "10" not in result

    def test_param_no_type_with_default(self):
        """Test parameter without type annotation but with default."""
        result = Implementation.param_to_string("z", inspect._empty, 5)
        assert "z" in result
        assert "5" in result

    def test_param_no_type_no_default(self):
        """Test parameter without type annotation or default."""
        result = Implementation.param_to_string("w", inspect._empty, inspect._empty)
        assert "w" in result
        assert result == "w"


class TestImplementationSignature:
    """Tests for Implementation._signature property."""

    def test_signature_no_params(self):
        """Test signature generation for function with no parameters."""
        impl = Implementation("func", {}, "")
        signature = impl._signature
        assert "func" in signature
        assert "()" in signature
        assert "highlight language-python" in signature

    def test_signature_with_params(self):
        """Test signature with multiple parameters."""

        @dispatch
        def multi_param(a: int, b: str, c: float = 3.14):
            """Function with multiple params."""
            pass

        params = inspect.signature(multi_param).parameters
        impl = Implementation("multi_param", params, "")
        signature = impl._signature

        assert "multi_param" in signature
        assert "(" in signature
        assert "<strong>a</strong>" in signature
        assert "<strong>b</strong>" in signature
        assert "<strong>c</strong>" in signature
        assert "3.14" in signature

    def test_signature_keyword_only_args(self):
        """Test signature with keyword-only arguments."""

        @dispatch
        def kwonly_func(a: int, *, b: str):
            """Function with keyword-only arg."""
            pass

        params = inspect.signature(kwonly_func).parameters
        impl = Implementation("kwonly_func", params, "")
        signature = impl._signature

        assert "*" in signature  # Should have * separator
        assert "<strong>a</strong>" in signature
        assert "<strong>b</strong>" in signature

    def test_signature_html_structure(self):
        """Test that signature has correct HTML structure."""
        impl = Implementation("test_func", {}, "")
        signature = impl._signature

        # Should be wrapped in proper HTML tags
        assert signature.startswith('<h3 class="doc doc-heading">')
        assert signature.endswith("</h3>")
        assert "highlight language-python" in signature


class TestImplementationRepr:
    """Tests for Implementation.__repr__ and __str__."""

    def test_repr_contains_signature(self, simple_implementation_params):
        """Test that __repr__ contains the signature."""
        impl = Implementation(
            simple_implementation_params["name"],
            simple_implementation_params["params"],
            simple_implementation_params["docs"],
        )
        repr_str = repr(impl)
        assert "sample(" in repr_str

    def test_repr_contains_docs(self, simple_implementation_params):
        """Test that __repr__ contains documentation."""
        impl = Implementation(
            simple_implementation_params["name"],
            simple_implementation_params["params"],
            simple_implementation_params["docs"],
        )
        repr_str = repr(impl)
        # Should contain either the parsed docs or parameters table
        assert len(repr_str) > 50  # Non-trivial output

    def test_str_equals_repr(self, simple_implementation_params):
        """Test that __str__ equals __repr__."""
        impl = Implementation(
            simple_implementation_params["name"],
            simple_implementation_params["params"],
            simple_implementation_params["docs"],
        )
        assert str(impl) == repr(impl)
