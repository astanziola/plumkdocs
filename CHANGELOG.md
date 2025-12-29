# CHANGELOG

## Unreleased

### Changed
- **BREAKING**: Minimum Python version is now 3.11
- Migrated from setup.py to pyproject.toml with hatchling build backend
- Updated dependencies to latest versions (griffe 1.x, mkdocstrings-python 2.0, etc.)
- Updated mkdocs configuration format for compatibility with mkdocstrings-python 2.0

## v0.0.5

### Added
- Added markdown support to base docstrings

### Changed
- Updated to plum 2.x

## v0.0.4

### Changed
- Moved dependencies to pyproject.toml

## v0.0.3

### Added
- Initial release with mkdocs plugin functionality
- Support for documenting plum-dispatch multiple dispatch functions
- Google-style docstring parsing with griffe
- Syntax highlighting for function signatures with Pygments
