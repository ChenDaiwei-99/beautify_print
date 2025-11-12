
# Beautify Print

Beautify Print is a lightweight Python package that makes it easy to beautifully format and display any output—such as LLM API responses or nested Python objects—directly in your terminal. Powered by the [Rich](https://github.com/Textualize/rich) library, it offers convenient functions, decorators, and context managers for effortless pretty printing and visually appealing output, saving you from manual setup and repetitive code.

## Features

- 🎨 Easy-to-use pretty printing for any Python object (including API responses and nested data)
- 🖼️ Print with stylish titles or panels
- 📜 Format and display Markdown
- 👩‍💻 Decorator and context manager support for seamless integration
- 🔄 Globally or temporarily beautify the `print()` function

## Installation

First, make sure you have the [`rich`](https://pypi.org/project/rich/) library installed:
```bash
uv add rich
```

Then, install this package (from the project directory):
```bash
uv pip install .
```

or install directly from Github:
```bash
uv pip install git+https://github.com/ChenDaiwei-99/beautify_print.git
```

_You can also use `pip install .` if you don't use [uv](https://github.com/astral-sh/uv)._

## Common Patterns
```python
from beautify_print import bprint, BPrint

# Your use case - simplified!
bprint(data, title="[adapter.base.py] processed_signature")

# Debug output
BPrint.debug(result, "Query Result")

# Markdown
bprint("# Title\n- Item", markdown=True)

# Code highlighting
bprint(code_string, code=True, language="python")

# Table
bprint(list_of_dicts, table=True)

```
## License
Open-source and free to use for any purpose. Feel free to fork or modify!
