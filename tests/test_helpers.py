"""Tests for helper functions in plumkdocs.main."""

from plumkdocs.main import get_base_docs, strip_modules, var_to_bold


class TestVarToBold:
    """Tests for var_to_bold function."""

    def test_type_annotation_context(self):
        """Test variable bolding in type annotation context."""
        input_html = '<span class="n">text</span><span class="p">:</span>'
        expected = '<span class="n"><strong>text</strong></span><span class="p">:</span>'
        assert var_to_bold(input_html) == expected

    def test_assignment_context(self):
        """Test variable bolding in assignment context."""
        input_html = '<span class="n">value</span> <span class="o">=</span>'
        expected = '<span class="n"><strong>value</strong></span> <span class="o">=</span>'
        assert var_to_bold(input_html) == expected

    def test_parameter_list_context(self):
        """Test variable bolding in parameter list context."""
        input_html = '<span class="n">param</span><span class="p">,</span>'
        expected = '<span class="n"><strong>param</strong></span><span class="p">,</span>'
        assert var_to_bold(input_html) == expected

    def test_multiple_variables(self):
        """Test bolding multiple variables in same string."""
        input_html = (
            '<span class="n">a</span><span class="p">:</span> '
            '<span class="n">b</span> <span class="o">=</span> '
            '<span class="n">c</span><span class="p">,</span>'
        )
        expected = (
            '<span class="n"><strong>a</strong></span><span class="p">:</span> '
            '<span class="n"><strong>b</strong></span> <span class="o">=</span> '
            '<span class="n"><strong>c</strong></span><span class="p">,</span>'
        )
        assert var_to_bold(input_html) == expected

    def test_no_matching_patterns(self):
        """Test that non-matching HTML is unchanged."""
        input_html = '<span class="k">def</span> <span class="nf">foo</span>'
        assert var_to_bold(input_html) == input_html

    def test_empty_string(self):
        """Test empty string input."""
        assert var_to_bold("") == ""


class TestStripModules:
    """Tests for strip_modules function."""

    def test_strip_typing_union(self):
        """Test stripping typing.Union."""
        input_str = "typing.Union[int, str]"
        expected = "Union[int, str]"
        assert strip_modules(input_str) == expected

    def test_strip_jwave_medium(self):
        """Test stripping jwave.geometry.MediumObject."""
        input_str = "jwave.geometry.MediumObject[int, str]"
        expected = "Medium[int, str]"
        assert strip_modules(input_str) == expected

    def test_strip_class_tags(self):
        """Test stripping <class > tags."""
        input_str = "<class 'int'>"
        expected = "'int'"
        assert strip_modules(input_str) == expected

    def test_strip_jaxdf_paths(self):
        """Test stripping jaxdf module paths."""
        input_str = "jaxdf.discretization.OnGrid"
        expected = "OnGrid"
        assert strip_modules(input_str) == expected

    def test_strip_jwave_paths(self):
        """Test stripping jwave module paths."""
        input_str = "jwave.geometry.Domain"
        expected = "Domain"
        assert strip_modules(input_str) == expected

    def test_strip_jaxdf_core_paths(self):
        """Test stripping jaxdf.core module paths."""
        input_str = "jaxdf.core.Field"
        expected = "Field"
        assert strip_modules(input_str) == expected

    def test_complex_nested_type(self):
        """Test stripping from complex nested type annotation."""
        input_str = (
            "typing.Union[jwave.geometry.MediumObject[<class 'object'>, "
            "<class 'object'>, <class 'jaxdf.discretization.OnGrid'>], "
            "jwave.geometry.MediumObject[<class 'object'>, "
            "<class 'jaxdf.discretization.OnGrid'>, <class 'object'>]]"
        )
        expected = (
            "Union[Medium['object', 'object', 'OnGrid'], Medium['object', 'OnGrid', 'object']]"
        )
        assert strip_modules(input_str) == expected

    def test_unrecognized_module(self):
        """Test that unrecognized modules are left unchanged."""
        input_str = "my.custom.module.Class"
        assert strip_modules(input_str) == input_str

    def test_empty_string(self):
        """Test empty string input."""
        assert strip_modules("") == ""


class TestGetBaseDocs:
    """Tests for get_base_docs function."""

    def test_get_base_docs_with_docs(self, plum_function_simple):
        """Test extracting base docs from plum function."""
        base_docs = get_base_docs([plum_function_simple])
        assert "Base documentation for simple_func" in base_docs
        assert "simple test function" in base_docs

    def test_get_base_docs_markdown(self, plum_function_markdown):
        """Test extracting base docs with markdown."""
        base_docs = get_base_docs([plum_function_markdown])
        assert "**markdown**" in base_docs
        assert "code blocks" in base_docs

    def test_get_base_docs_minimal(self, plum_function_no_docs):
        """Test extracting minimal base docs."""
        base_docs = get_base_docs([plum_function_no_docs])
        assert "Base docs only" in base_docs
