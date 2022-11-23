# pluMkdocs

A very, very hacky way to document multiple dispatch function implemented using the wonderful [plum](https://github.com/wesselb/plum) package

## Desclaimer

Have I mentioned that this is very hacky? It raises a whole lot of warnings, the vast majority of which I don't understand. Also, it is not heavly tested and only checked against mkdocs-material. It contains a lot of hard coded stuff and is not very flexible. It is also not very well documented.

I'm uploading this with the hope that someone will find it useful and will improve it. Contributions welcome :)

Also, I need this as a dependency for other projects, so I will probably not be able to maintain this very well.

## How to use

This package exposes an `implementations` macro that can be used to list the dispatched implementations of a function in your mkdocs.

To use it, in your `mkdocs.yml` file, make sure to load the `mkdocs-macros` plugin using

```yaml
plugins:
  macros:
    module_name: docs/macros
```

where `docs/macros` can be any path to a module that contains the macros. Then, in your `docs/macros.py` file, you can define the macros you want to use. If you don't have any other macro, you simply need to expose the function `define_env` from the `plumkdocs` module, like so:

```python
from plumkdocs import define_env

__all__ = ['define_env']
```

If you have other macros, you can simply add the macro to your `define_env` function, like so:

```python
from plumkdocs import mod_to_string

def define_env(env):
    @env.macro
    def implementations(module: str, function=None):
        return mod_to_string(module, function)
```

In both cases, you can then use the `implementations` macro in your markdown files, like so:

```markdown
## My awesome function

Following are all the implementations for my awesome `foo` function in the package `my_package`:


{{ implementations('my_package', 'foo') }}
```

This will list all the implementations of the `foo` function in the `my_package` module. The docstrings will be (hopefully) correctly formatted, and the code will be highlighted using the `pygments` syntax highlighter. The signature of each method will also be displayed.

To see a working example, check out the [`jaxdf`](https://ucl-bug.github.io/jaxdf/) and [`jwave`](https://ucl-bug.github.io/jwave/) documentation.
